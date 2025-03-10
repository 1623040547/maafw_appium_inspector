import 'dart:convert';
import 'dart:async';
import 'package:maafw_appium_inspector/features/control/providers/server_state.dart';
import 'package:http/http.dart' as http;
import '../../core/models/server_status_model.dart';
import '../../core/utils/logger.dart';



  class ServerService {
    final Logger _logger;
    final ServerState _serverState;
  
    ServerStatusModel _appiumStatus = ServerStatusModel(
        isRunning: false, isExternal: true, port: 4723, type: 'appium');
    ServerStatusModel _pythonStatus = ServerStatusModel(
        isRunning: false, isExternal: true, port: 5000, type: 'python');
  
    ServerService({
      Logger? logger,
      required ServerState serverState,
    })  : _logger = logger ?? Logger(),
            _serverState = serverState;
  
    Future<bool> checkPythonServerStatus() async {
      try {
        final response = await http
            .post(
              Uri.parse('http://127.0.0.1:${_pythonStatus.port}/init'),
              headers: {'Content-Type': 'application/json'},
              body: json.encode({
                'capabilities': {},
                'server_url': 'http://127.0.0.1:${_appiumStatus.port}'
              }),
            )
            .timeout(Duration(seconds: 20));
  
        final isRunning = response.statusCode == 200;
  
        _pythonStatus = ServerStatusModel(
          isRunning: isRunning,
          isExternal: true,
          port: _pythonStatus.port,
          type: _pythonStatus.type,
        );
        _serverState.updatePythonStatus(_pythonStatus);
        return isRunning;
      } catch (e) {
        _logger.log('Python服务器检查失败: $e', LogType.error);
        return false;
      }
    }
  
    Future<bool> checkAppiumServerStatus() async {
      try {
        final response = await http
            .get(
              Uri.parse('http://127.0.0.1:${_appiumStatus.port}/status'),
            )
            .timeout(Duration(seconds: 20));
        final isRunning = response.statusCode == 200;
  
        _appiumStatus = ServerStatusModel(
          isRunning: isRunning,
          isExternal: true,
          port: _appiumStatus.port,
          type: _appiumStatus.type,
        );
        _serverState.updateAppiumStatus(_appiumStatus);
        return isRunning;
      } catch (e) {
        _logger.log('Appium服务器检查失败: $e', LogType.error);
        return false;
      }
    }
  }

