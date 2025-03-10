import 'package:flutter/foundation.dart';
import '../../../core/models/capabilities_model.dart';
import '../../../services/config/config_service.dart';

class ControlState extends ChangeNotifier {
  final ConfigService _configService = ConfigService();
  bool _isInitialized = false;
  bool _isInitializing = false;
  bool _isStreamEnabled = false;
  CapabilitiesModel _capabilities = CapabilitiesModel();

  bool get isInitialized => _isInitialized;
  bool get isInitializing => _isInitializing;
  bool get isStreamEnabled => _isStreamEnabled;
  CapabilitiesModel get capabilities => _capabilities;

  void setInitializing(bool value) {
    _isInitializing = value;
    notifyListeners();
  }

  void setInitialized(bool value) {
    _isInitialized = value;
    notifyListeners();
  }

  void setStreamEnabled(bool value) {
    _isStreamEnabled = value;
    notifyListeners();
  }

  Future<void> init() async {
    await loadCapabilities();
  }

  Future<void> updateCapabilities(CapabilitiesModel capabilities) async {
    _capabilities = capabilities;
    await _configService.saveCapabilities(capabilities);
    notifyListeners();
  }

  Future<void> loadCapabilities() async {
    _capabilities = await _configService.loadCapabilities();
    notifyListeners();
  }

  Future<void> clearCapabilities() async {
    await _configService.clearCapabilities();
    _capabilities = CapabilitiesModel();
    notifyListeners();
  }
}