import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:path/path.dart' as path;
import '../widgets/settings_section.dart';
import '../widgets/path_setting_item.dart';
import '../../../services/config/config_service.dart';

class SettingsPage extends StatefulWidget {
  const SettingsPage({Key? key}) : super(key: key);

  @override
  _SettingsPageState createState() => _SettingsPageState();
}

class _SettingsPageState extends State<SettingsPage> {
  final ConfigService _configService = ConfigService();
  String? _pythonVenvPath;
  String? _pythonScriptPath;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final venvPath = await _configService.loadPythonVenvPath();
    final scriptPath = await _configService.loadPythonScriptPath();
    setState(() {
      _pythonVenvPath = venvPath;
      _pythonScriptPath = scriptPath;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('系统设置'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _loadSettings,
            tooltip: '重新加载',
          ),
        ],
      ),
      body: ListView(
        padding: EdgeInsets.all(16.0),
        children: [
          SettingsSection(
            title: 'Python 环境',
            children: [
              PathSettingItem(
                label: 'Python 虚拟环境路径',
                value: _pythonVenvPath,
                onSelect: _selectVenvPath,
                onClear: () => _clearPath(true),
              ),
              SizedBox(height: 16),
              PathSettingItem(
                label: 'Python 脚本路径',
                value: _pythonScriptPath,
                onSelect: _selectScriptPath,
                onClear: () => _clearPath(false),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Future<void> _selectVenvPath() async {
    try {
      final result = await FilePicker.platform.getDirectoryPath(
        dialogTitle: '选择 Python 虚拟环境目录',
      );
      if (result != null) {
        await _configService.savePythonVenvPath(result);
        setState(() => _pythonVenvPath = result);
      }
    } catch (e) {
      _showError('选择目录失败: $e');
    }
  }

  Future<void> _selectScriptPath() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        dialogTitle: '选择 Python 脚本文件',
        type: FileType.custom,
        allowedExtensions: ['py'],
      );
      if (result != null && result.files.single.path != null) {
        await _configService.savePythonScriptPath(result.files.single.path!);
        setState(() => _pythonScriptPath = result.files.single.path!);
      }
    } catch (e) {
      _showError('选择文件失败: $e');
    }
  }

  Future<void> _clearPath(bool isVenvPath) async {
    try {
      await _configService.clearPythonPaths();
      setState(() {
        if (isVenvPath) {
          _pythonVenvPath = null;
        } else {
          _pythonScriptPath = null;
        }
      });
    } catch (e) {
      _showError('清除路径失败: $e');
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }
}