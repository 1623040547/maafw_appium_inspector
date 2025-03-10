import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../../core/models/capabilities_model.dart';

class ConfigService {
  static const String _capabilitiesKey = 'appium_capabilities';
  static const String _pythonVenvPathKey = 'python_venv_path';
  static const String _pythonScriptPathKey = 'python_script_path';

  static final ConfigService _instance = ConfigService._internal();
  factory ConfigService() => _instance;
  ConfigService._internal();

  Future<void> saveCapabilities(CapabilitiesModel capabilities) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_capabilitiesKey, jsonEncode(capabilities.toJson()));
  }

  Future<CapabilitiesModel> loadCapabilities() async {
    final prefs = await SharedPreferences.getInstance();
    final String? jsonStr = prefs.getString(_capabilitiesKey);
    if (jsonStr == null) {
      return CapabilitiesModel();
    }
    return CapabilitiesModel.fromJson(jsonDecode(jsonStr));
  }

  Future<String?> loadPythonVenvPath() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_pythonVenvPathKey);
  }

  Future<void> savePythonVenvPath(String path) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_pythonVenvPathKey, path);
  }

  Future<String?> loadPythonScriptPath() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_pythonScriptPathKey);
  }

  Future<void> savePythonScriptPath(String path) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_pythonScriptPathKey, path);
  }

  Future<void> clearAll() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
  }

  Future<void> clearCapabilities() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_capabilitiesKey);
  }

  Future<void> clearPythonPaths() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_pythonVenvPathKey);
    await prefs.remove(_pythonScriptPathKey);
  }
}