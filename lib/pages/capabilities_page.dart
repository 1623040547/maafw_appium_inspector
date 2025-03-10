import 'package:flutter/material.dart';

class CapabilitiesPage extends StatefulWidget {
  final Map<String, dynamic> initialCapabilities;

  const CapabilitiesPage({
    Key? key,
    required this.initialCapabilities,
  }) : super(key: key);

  @override
  _CapabilitiesPageState createState() => _CapabilitiesPageState();
}

class _CapabilitiesPageState extends State<CapabilitiesPage> {
  final _formKey = GlobalKey<FormState>();

  // Initialize variables with default values
  String platformName = 'iOS';
  String udid = '';
  String automationName = 'XCUITest';
  String platformVersion = '';
  String bundleId = '';
  String appPath = '';
  String newCommandTimeout = '60';
  String wdaLocalPort = '8100';
  bool useAppPath = false;

  @override
  void initState() {
    super.initState();
    // Load values from initial capabilities
    platformName = widget.initialCapabilities['platformName'] ?? platformName;
    udid = widget.initialCapabilities['appium:udid'] ?? udid;
    automationName =
        widget.initialCapabilities['appium:automationName'] ?? automationName;
    platformVersion =
        widget.initialCapabilities['appium:platformVersion'] ?? platformVersion;
    bundleId = widget.initialCapabilities['appium:bundleId'] ?? bundleId;
    appPath = widget.initialCapabilities['appium:app'] ?? appPath;
    newCommandTimeout =
        widget.initialCapabilities['appium:newCommandTimeout']?.toString() ??
            newCommandTimeout;
    wdaLocalPort =
        widget.initialCapabilities['appium:wdaLocalPort']?.toString() ??
            wdaLocalPort;
    useAppPath = widget.initialCapabilities['appium:app'] != null;
  }

  Map<String, dynamic> getCapabilities() {
    final capabilities = {
      "platformName": platformName,
      "appium:udid": udid,
      "appium:automationName": automationName,
      "appium:platformVersion": platformVersion,
      "appium:newCommandTimeout": int.parse(newCommandTimeout),
      "appium:wdaLocalPort": int.parse(wdaLocalPort),
    };

    // 根据选择添加不同的连接方式
    if (useAppPath) {
      capabilities["appium:app"] = appPath;
    } else {
      capabilities["appium:bundleId"] = bundleId;
    }

    return capabilities;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Appium 配置'),
        actions: [
          IconButton(
            icon: Icon(Icons.save),
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                _formKey.currentState!.save();
                Navigator.pop(context, getCapabilities());
              }
            },
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                initialValue: platformName,
                decoration: InputDecoration(labelText: 'Platform Name'),
                onSaved: (value) => platformName = value ?? '',
                validator: (value) => value?.isEmpty ?? true ? '不能为空' : null,
              ),
              TextFormField(
                initialValue: udid,
                decoration: InputDecoration(labelText: 'UDID'),
                onSaved: (value) => udid = value ?? '',
                validator: (value) => value?.isEmpty ?? true ? '不能为空' : null,
              ),
              TextFormField(
                initialValue: automationName,
                decoration: InputDecoration(labelText: 'Automation Name'),
                onSaved: (value) => automationName = value ?? '',
                validator: (value) => value?.isEmpty ?? true ? '不能为空' : null,
              ),
              TextFormField(
                initialValue: platformVersion,
                decoration: InputDecoration(labelText: 'Platform Version'),
                onSaved: (value) => platformVersion = value ?? '',
                validator: (value) => value?.isEmpty ?? true ? '不能为空' : null,
              ),

              // 添加连接方式切换
              SwitchListTile(
                title: Text('使用应用路径连接'),
                value: useAppPath,
                onChanged: (bool value) {
                  setState(() {
                    useAppPath = value;
                  });
                },
              ),

              // 根据选择显示不同的输入字段
              if (!useAppPath)
                TextFormField(
                  initialValue: bundleId,
                  decoration: InputDecoration(labelText: 'Bundle ID'),
                  onSaved: (value) => bundleId = value ?? '',
                  validator: (value) => useAppPath
                      ? null
                      : (value?.isEmpty ?? true ? '不能为空' : null),
                ),

              if (useAppPath)
                TextFormField(
                  initialValue: appPath,
                  decoration: InputDecoration(
                    labelText: 'App Path',
                    hintText: '例如: /path/to/your/app.app',
                  ),
                  onSaved: (value) => appPath = value ?? '',
                  validator: (value) => !useAppPath
                      ? null
                      : (value?.isEmpty ?? true ? '不能为空' : null),
                ),

              TextFormField(
                initialValue: newCommandTimeout,
                decoration: InputDecoration(labelText: 'New Command Timeout'),
                keyboardType: TextInputType.number,
                onSaved: (value) => newCommandTimeout = value ?? '60',
                validator: (value) {
                  if (value?.isEmpty ?? true) return '不能为空';
                  if (int.tryParse(value!) == null) return '必须是数字';
                  return null;
                },
              ),
              TextFormField(
                initialValue: wdaLocalPort,
                decoration: InputDecoration(labelText: 'WDA Local Port'),
                keyboardType: TextInputType.number,
                onSaved: (value) => wdaLocalPort = value ?? '8100',
                validator: (value) {
                  if (value?.isEmpty ?? true) return '不能为空';
                  if (int.tryParse(value!) == null) return '必须是数字';
                  return null;
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
