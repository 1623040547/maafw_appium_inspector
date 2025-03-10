import 'dart:async';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/control_state.dart';
import '../providers/server_state.dart';
import '../widgets/server_status_card.dart';
import '../widgets/control_panel.dart';
import '../../../shared/widgets/screen_stream.dart';
import '../../../services/server/server_service.dart';
import '../../../services/appium/appium_service.dart';
import '../../../core/models/capabilities_model.dart';
import '../../capabilities/pages/capabilities_page.dart';
import '../../logs/pages/logs_page.dart';
import '../../settings/pages/settings_page.dart';

class ControlPage extends StatefulWidget {
  @override
  _ControlPageState createState() => _ControlPageState();
}

class _ControlPageState extends State<ControlPage> {
  Timer? _checkTimer;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _initializeState();
    });
  }

  @override
  void dispose() {
    _checkTimer?.cancel();
    super.dispose();
  }

  Future<void> _initializeState() async {
    final serverState = context.read<ServerState>();
    final serverService = context.read<ServerService>();

    // 首次检查服务器状态
    await _checkServerStatus(serverService);
    
    // 启动定时检查
    _startStatusCheck(serverService);

    // 初始化控制状态
    context.read<ControlState>().init();
  }

  Future<void> _checkServerStatus(ServerService serverService) async {
    await serverService.checkAppiumServerStatus();
    await serverService.checkPythonServerStatus();
  }

  void _startStatusCheck(ServerService serverService) {
    _checkTimer?.cancel();
    _checkTimer = Timer.periodic(Duration(seconds: 5), (timer) async {
      final serverState = context.read<ServerState>();
      
      // 如果两个服务都已连接，停止检查
      if (serverState.appiumStatus.isRunning && serverState.pythonStatus.isRunning) {
        timer.cancel();
        return;
      }
      
      await _checkServerStatus(serverService);
    });
  }

    
   
  

  @override
  Widget build(BuildContext context) {
    final controlState = context.watch<ControlState>();
    final serverState = context.watch<ServerState>();
    final serverService = context.read<ServerService>();
    final appiumService = context.read<AppiumService>();

    return Scaffold(
      appBar: AppBar(
        title: Text('Appium 控制'),
        actions: _buildActions(context),
      ),
      body: Row(
        children: [
          Container(
            width: 200,
            padding: EdgeInsets.all(8.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ServerStatusCard(
                  title: 'Appium 服务器',
                  status: serverState.appiumStatus,
                 
                ),
                SizedBox(height: 8),
                ServerStatusCard(
                  title: 'Python 服务器',
                  status: serverState.pythonStatus,
                 
                ),
                SizedBox(height: 8),
                ControlPanel(
                  isInitialized: controlState.isInitialized,
                  isInitializing: controlState.isInitializing,
                  isStreamEnabled: controlState.isStreamEnabled,
                  onInitialize: () =>
                      _handleInitialize(context, appiumService, controlState),
                  onStreamToggle: (enabled) =>
                      controlState.setStreamEnabled(enabled),
                  onReset: () => controlState.setInitialized(false), // 添加重置处理
                ),
              ],
            ),
          ),
          Expanded(
            child: ScreenStream(
              serverService: serverService,
              isInitialized: controlState.isInitialized,
              isConnected: true, // 传入初始化状态
            ),
          ),
        ],
      ),
    );
  }

  List<Widget> _buildActions(BuildContext context) {
    return [
      IconButton(
        icon: Icon(Icons.terminal),
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => LogsPage()),
        ),
        tooltip: '服务器日志',
      ),
      IconButton(
        icon: Icon(Icons.build),
        onPressed: () => _showCapabilitiesPage(context),
        tooltip: '配置 Capabilities',
      ),
      IconButton(
        icon: Icon(Icons.settings),
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => SettingsPage()),
        ),
        tooltip: '系统设置',
      ),
    ];
  }

  Future<void> _showCapabilitiesPage(BuildContext context) async {
    final controlState = context.read<ControlState>();
    final result = await Navigator.push<CapabilitiesModel>(
      context,
      MaterialPageRoute(
        builder: (_) => CapabilitiesPage(
          initialCapabilities: controlState.capabilities,
        ),
      ),
    );

    if (result != null) {
      await controlState.updateCapabilities(result);
    }
  }

  Future<void> _handleInitialize(
    BuildContext context,
    AppiumService appiumService,
    ControlState controlState,
  ) async {
    controlState.setInitializing(true);
    try {
      final success = await appiumService.initController(
        capabilities: controlState.capabilities,
      );
      controlState.setInitialized(success);
      if (success) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('初始化成功')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('初始化失败: $e')),
      );
    } finally {
      controlState.setInitializing(false);
    }
  }
}
