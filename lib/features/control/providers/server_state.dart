import 'package:flutter/foundation.dart';
import '../../../core/models/server_status_model.dart';

class ServerState extends ChangeNotifier {
  ServerStatusModel _appiumStatus = ServerStatusModel(
    isRunning: false,
    isExternal: false,
    port: 4723,
    type: 'appium'
  );

  ServerStatusModel _pythonStatus = ServerStatusModel(
    isRunning: false,
    isExternal: false,
    port: 5000,
    type: 'python'
  );

  ServerStatusModel get appiumStatus => _appiumStatus;
  ServerStatusModel get pythonStatus => _pythonStatus;

  void updateAppiumStatus(ServerStatusModel status) {
    _appiumStatus = status;
    notifyListeners();
  }

  void updatePythonStatus(ServerStatusModel status) {
    _pythonStatus = status;
    notifyListeners();
  }
}