import 'package:flutter/material.dart';
import '../../../core/models/server_status_model.dart';

class ServerStatusCard extends StatelessWidget {
  final String title;
  final ServerStatusModel status;

  const ServerStatusCard({
    Key? key,
    required this.title,
    required this.status,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: Theme.of(context).textTheme.titleSmall),
            SizedBox(height: 4),
            Row(
              children: [
                Expanded(
                  child: Text(
                    status.isRunning ? '运行中' : '未运行',
                    style: TextStyle(
                      color: status.isRunning ? Colors.green : Colors.red,
                    ),
                  ),
                ),
                Container(
                  width: 8,
                  height: 8,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: status.isRunning ? Colors.green : Colors.red,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}