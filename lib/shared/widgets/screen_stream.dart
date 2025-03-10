import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../../services/server/server_service.dart';
import '../../features/control/providers/server_state.dart';
import 'package:http/http.dart' as http;

class ScreenStream extends StatefulWidget {
  final bool isConnected;
  final ServerService serverService;
  final bool isInitialized; // 添加初始化状态属性

  const ScreenStream({
    Key? key,
    required this.isConnected,
    required this.serverService,
    required this.isInitialized, // 添加参数
  }) : super(key: key);

  @override
  _ScreenStreamState createState() => _ScreenStreamState();
}

class _ScreenStreamState extends State<ScreenStream> {
  Uint8List? _imageData;
  WebSocketChannel? _channel;
  Size? _deviceSize;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0; // 添加重连次数计数
  static const int maxReconnectAttempts = 3; // 最大重连次数
  static const Duration reconnectDelay = Duration(seconds: 3); // 重连延迟

  @override
  void initState() {
    super.initState();
    if (widget.isConnected) {
      _startReconnectTimer();
    }
  }

  void _startReconnectTimer() {
    _reconnectTimer?.cancel();
    _reconnectTimer = Timer.periodic(reconnectDelay, (timer) {
      if (_channel == null &&
          widget.isConnected &&
          _reconnectAttempts < maxReconnectAttempts) {
        print(
            '尝试重新连接 WebSocket... (尝试 ${_reconnectAttempts + 1}/$maxReconnectAttempts)');
        _connectWebSocket();
      } else if (_reconnectAttempts >= maxReconnectAttempts) {
        print('达到最大重连次数，停止重连');
        timer.cancel();
      }
    });
  }

  void _connectWebSocket() {
    if (_channel != null || !widget.isConnected) {
      return;
    }

    try {
      final serverState = context.read<ServerState>();
      final port = serverState.pythonStatus.port;
      final uri = Uri.parse('ws://127.0.0.1:$port/screen');

      print('正在连接 WebSocket: $uri');
      final channel = WebSocketChannel.connect(uri);

      channel.stream.listen(
        (message) {
          _reconnectAttempts = 0; // 连接成功后重置计数
          _channel = channel;
          if (message is String) {
            try {
              final jsonData = json.decode(message);
              if (jsonData['type'] == 'screen') {
                final base64Image = jsonData['data'];
                final data = base64Decode(base64Image);
                _updateImage(data);
              }
            } catch (e) {
              print('解析图像数据失败: $e');
            }
          }
        },
        onError: (error) {
          print('WebSocket 错误: $error');
          _disconnectWebSocket();
          _reconnectAttempts++;
          if (_reconnectAttempts < maxReconnectAttempts) {
            _reconnect();
          }
        },
        onDone: () {
          print('WebSocket 连接关闭');
          _disconnectWebSocket();
          _reconnectAttempts++;
          if (_reconnectAttempts < maxReconnectAttempts) {
            _reconnect();
          }
        },
        cancelOnError: false,
      );
    } catch (e) {
      print('WebSocket 连接失败: $e');
      _disconnectWebSocket();
      _reconnectAttempts++;
    }
  }

  void _reconnect() {
    if (!mounted ||
        !widget.isConnected ||
        _reconnectAttempts >= maxReconnectAttempts) {
      return;
    }

    Future.delayed(reconnectDelay, () {
      if (mounted && widget.isConnected) {
        _connectWebSocket();
      }
    });
  }

  @override
  void didUpdateWidget(ScreenStream oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isConnected != oldWidget.isConnected) {
      if (widget.isConnected) {
        _reconnectAttempts = 0; // 重置重连次数
        _startReconnectTimer();
      } else {
        _reconnectTimer?.cancel();
        _disconnectWebSocket();
      }
    }
  }

  @override
  void dispose() {
    _reconnectTimer?.cancel();
    _disconnectWebSocket();
    super.dispose();
  }

  double get aspectRatio =>
      _deviceSize != null ? _deviceSize!.width / _deviceSize!.height : 9 / 16;

  Future<void> _fetchScreenInfo() async {
    try {
      final serverState = context.read<ServerState>();
      final port = serverState.pythonStatus.port;
      final response = await http.get(
        Uri.parse('http://127.0.0.1:$port/screen_info'),
      );

      final result = json.decode(response.body);
      if (result['status'] == 'success') {
        final data = result['data'];
        setState(() {
          _deviceSize = Size(
            data['width'].toDouble(),
            data['height'].toDouble(),
          );
        });
      }
    } catch (e) {
      print('获取屏幕信息失败: $e');
    }
  }

  void _disconnectWebSocket() {
    _channel?.sink.close();
    _channel = null;
    setState(() {
      _imageData = null;
    });
  }

  Future<void> _updateImage(Uint8List data) async {
    if (!mounted) return;
    try {
      final image = await decodeImageFromList(data);
      setState(() {
        _imageData = data;
      });
    } catch (e) {
      print('更新图像失败: $e');
    }
  }

  // 坐标转换方法
  Offset _mapToDeviceCoordinates(Offset position, BoxConstraints constraints) {
    return position;
  }

  Future<bool> _sendAction(String action, Map<String, dynamic> data) async {
    try {
      final serverState = context.read<ServerState>();
      final port = serverState.pythonStatus.port;
      final response = await http.post(
        Uri.parse('http://127.0.0.1:$port/action/$action'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );

      final result = json.decode(response.body);
      return result['status'] == 'success';
    } catch (e) {
      print('发送操作失败: $e');
      return false;
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_imageData == null) {
      // 只检查图片是否存在
      return Center(child: Text('未连接'));
    }

    return Center(
      child: SingleChildScrollView(
        child: Container(
          color: Colors.black,
          width: _deviceSize?.width,
          height: _deviceSize?.height,
          child: LayoutBuilder(
            builder: (context, constraints) {
              return GestureDetector(
                // 手势检测器需要根据连接状态禁用
                onTapUp: _channel != null
                    ? (details) async {
                        final RenderBox box =
                            context.findRenderObject() as RenderBox;
                        final localPosition =
                            box.globalToLocal(details.globalPosition);
                        final devicePosition =
                            _mapToDeviceCoordinates(localPosition, constraints);

                        await _sendAction('tap',
                            {'x': devicePosition.dx, 'y': devicePosition.dy});
                      }
                    : null,
                onLongPressStart: _channel != null
                    ? (details) async {
                        final RenderBox box =
                            context.findRenderObject() as RenderBox;
                        final localPosition =
                            box.globalToLocal(details.globalPosition);
                        final devicePosition =
                            _mapToDeviceCoordinates(localPosition, constraints);

                        await _sendAction('long_press', {
                          'x': devicePosition.dx,
                          'y': devicePosition.dy,
                          'duration': 2
                        });
                      }
                    : null,
                onPanEnd: _channel != null
                    ? (details) async {
                        if (_panStartPosition != null &&
                            _panEndPosition != null) {
                          final startPos = _mapToDeviceCoordinates(
                              _panStartPosition!, constraints);
                          final endPos = _mapToDeviceCoordinates(
                              _panEndPosition!, constraints);

                          await _sendAction('swipe', {
                            'startX': startPos.dx,
                            'startY': startPos.dy,
                            'endX': endPos.dx,
                            'endY': endPos.dy,
                            'duration': 0.5
                          });
                        }
                        _panStartPosition = null;
                        _panEndPosition = null;
                      }
                    : null,
                onPanStart: _channel != null
                    ? (details) {
                        final RenderBox box =
                            context.findRenderObject() as RenderBox;
                        _panStartPosition =
                            box.globalToLocal(details.globalPosition);
                      }
                    : null,
                onPanUpdate: _channel != null
                    ? (details) {
                        final RenderBox box =
                            context.findRenderObject() as RenderBox;
                        _panEndPosition =
                            box.globalToLocal(details.globalPosition);
                      }
                    : null,
                child: Image.memory(
                  _imageData!,
                  fit: BoxFit.fill,
                  gaplessPlayback: true,
                ),
              );
            },
          ),
        ),
      ),
    );
  }

  Offset? _panStartPosition;
  Offset? _panEndPosition;
}
