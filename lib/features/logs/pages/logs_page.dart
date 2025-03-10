import 'package:flutter/material.dart';
import '../widgets/log_panel.dart';
import '../../../core/utils/logger.dart';

class LogsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('服务器日志'),
      ),
      body: Row(
        children: [
          Expanded(
            child: LogPanel(
              title: 'Appium 服务器日志',
              logType: LogType.appium,
            ),
          ),
          Expanded(
            child: LogPanel(
              title: 'Python 服务器日志',
              logType: LogType.python,
            ),
          ),
        ],
      ),
    );
  }
}