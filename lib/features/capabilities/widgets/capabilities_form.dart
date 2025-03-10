import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../../../core/models/capabilities_model.dart';

class CapabilitiesForm extends StatelessWidget {
  final GlobalKey<FormState> formKey;
  final CapabilitiesModel capabilities;
  final ValueChanged<CapabilitiesModel> onChanged;

  const CapabilitiesForm({
    Key? key,
    required this.formKey,
    required this.capabilities,
    required this.onChanged,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Form(
      key: formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          TextFormField(
            initialValue: capabilities.platformName,
            decoration: InputDecoration(
              labelText: '平台名称',
              helperText: '例如: iOS',
            ),
            validator: (value) => value?.isEmpty ?? true ? '请输入平台名称' : null,
            onChanged: (value) => onChanged(capabilities.copyWith(platformName: value)),
          ),
          SizedBox(height: 16),
          TextFormField(
            initialValue: capabilities.udid,
            decoration: InputDecoration(
              labelText: '设备 UDID',
              helperText: '设备唯一标识符',
            ),
            validator: (value) => value?.isEmpty ?? true ? '请输入设备 UDID' : null,
            onChanged: (value) => onChanged(capabilities.copyWith(udid: value)),
          ),
          SizedBox(height: 16),
          TextFormField(
            initialValue: capabilities.automationName,
            decoration: InputDecoration(
              labelText: '自动化引擎',
              helperText: '例如: XCUITest',
            ),
            validator: (value) => value?.isEmpty ?? true ? '请输入自动化引擎' : null,
            onChanged: (value) => onChanged(capabilities.copyWith(automationName: value)),
          ),
          SizedBox(height: 16),
          TextFormField(
            initialValue: capabilities.platformVersion,
            decoration: InputDecoration(
              labelText: '平台版本',
              helperText: '例如: 14.5',
            ),
            validator: (value) => value?.isEmpty ?? true ? '请输入平台版本' : null,
            onChanged: (value) => onChanged(capabilities.copyWith(platformVersion: value)),
          ),
          SizedBox(height: 16),
          CheckboxListTile(
            title: Text('使用应用路径'),
            value: capabilities.appPath.isNotEmpty,
            onChanged: (value) {
              if (value ?? false) {
                _selectAppPath(context);
              } else {
                onChanged(capabilities.copyWith(
                  appPath: '',
                  bundleId: '',
                ));
              }
            },
            controlAffinity: ListTileControlAffinity.leading,
            contentPadding: EdgeInsets.zero,
          ),
          SizedBox(height: 16),
          if (capabilities.appPath.isEmpty) ...[
            TextFormField(
              initialValue: capabilities.bundleId,
              decoration: InputDecoration(
                labelText: '应用包名',
                helperText: '例如: com.example.app',
              ),
              validator: (value) => capabilities.appPath.isEmpty && (value?.isEmpty ?? true) 
                  ? '请输入应用包名' : null,
              onChanged: (value) => onChanged(capabilities.copyWith(bundleId: value)),
            ),
          ] else ...[
            Row(
              children: [
                Expanded(
                  child: TextFormField(
                    initialValue: capabilities.appPath,
                    decoration: InputDecoration(
                      labelText: '应用路径',
                      helperText: '应用安装包路径',
                    ),
                    readOnly: true,
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: () => _selectAppPath(context),
                  child: Text('选择'),
                ),
              ],
            ),
          ],
          SizedBox(height: 16),
          TextFormField(
            initialValue: capabilities.newCommandTimeout.toString(),
            decoration: InputDecoration(
              labelText: '命令超时时间',
              helperText: '单位：秒',
            ),
            keyboardType: TextInputType.number,
            validator: (value) {
              if (value == null || value.isEmpty) return '请输入超时时间';
              if (int.tryParse(value) == null) return '请输入有效的数字';
              return null;
            },
            onChanged: (value) {
              final timeout = int.tryParse(value);
              if (timeout != null) {
                onChanged(capabilities.copyWith(newCommandTimeout: timeout));
              }
            },
          ),
          SizedBox(height: 16),
          TextFormField(
            initialValue: capabilities.wdaLocalPort.toString(),
            decoration: InputDecoration(
              labelText: 'WDA 本地端口',
              helperText: '例如: 8100',
            ),
            keyboardType: TextInputType.number,
            validator: (value) {
              if (value == null || value.isEmpty) return '请输入端口号';
              if (int.tryParse(value) == null) return '请输入有效的数字';
              return null;
            },
            onChanged: (value) {
              final port = int.tryParse(value);
              if (port != null) {
                onChanged(capabilities.copyWith(wdaLocalPort: port));
              }
            },
          ),
        ],
      ),
    );
  }

  Future<void> _selectAppPath(BuildContext context) async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['ipa', 'app'],
    );
    
    if (result != null) {
      onChanged(capabilities.copyWith(appPath: result.files.single.path));
    }
  }
}