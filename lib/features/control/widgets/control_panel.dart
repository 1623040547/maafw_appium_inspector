import 'package:flutter/material.dart';

class ControlPanel extends StatelessWidget {
  final bool isInitialized;
  final bool isInitializing;
  final bool isStreamEnabled;
  final VoidCallback onInitialize;
  final ValueChanged<bool> onStreamToggle;
  final VoidCallback onReset;  // 添加重置回调

  const ControlPanel({
    Key? key,
    required this.isInitialized,
    required this.isInitializing,
    required this.isStreamEnabled,
    required this.onInitialize,
    required this.onStreamToggle,
    required this.onReset,  // 添加参数
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: isInitializing ? null : onInitialize,
                    child: Text(isInitializing ? '初始化中...' : '初始化'),
                  ),
                ),
                SizedBox(width: 8),
                IconButton(
                  icon: Icon(Icons.refresh),
                  onPressed: isInitializing ? null : onReset,
                  tooltip: '重置初始化状态',
                ),
              ],
            ),
            SizedBox(height: 8),
            SwitchListTile(
              title: Text('屏幕流'),
              value: isStreamEnabled,
              onChanged: isInitialized ? onStreamToggle : null,
            ),
          ],
        ),
      ),
    );
  }
}