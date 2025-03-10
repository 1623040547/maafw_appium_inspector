import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/models/capabilities_model.dart';
import '../../core/utils/logger.dart';

class AppiumService {
  final Logger _logger = Logger();
  final String _baseUrl;
  
  AppiumService({required String baseUrl}) : _baseUrl = baseUrl;

  Future<bool> initController({
    required CapabilitiesModel capabilities,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/init'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'capabilities': capabilities.toJson(),
        }),
      );

      final data = jsonDecode(response.body);
      return data['status'] == 'success';
    } catch (e) {
      _logger.log('初始化控制器失败: $e', LogType.error);
      return false;
    }
  }

  Future<bool> runPipeline({
    required Map<String, dynamic> pipeline,
    required String resourcePath,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/pipeline'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'pipeline': pipeline,
          'resourcePath': resourcePath,
        }),
      );

      final data = jsonDecode(response.body);
      return data['status'] == 'success';
    } catch (e) {
      _logger.log('执行 Pipeline 失败: $e', LogType.error);
      return false;
    }
  }
}