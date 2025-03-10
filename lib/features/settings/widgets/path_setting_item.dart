import 'package:flutter/material.dart';

class PathSettingItem extends StatelessWidget {
  final String label;
  final String? value;
  final VoidCallback onSelect;
  final VoidCallback onClear;

  const PathSettingItem({
    Key? key,
    required this.label,
    required this.value,
    required this.onSelect,
    required this.onClear,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.titleSmall,
        ),
        SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: Container(
                padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey.shade300),
                  borderRadius: BorderRadius.circular(4),
                ),
                child: Text(
                  value ?? '未设置',
                  style: TextStyle(
                    color: value == null ? Colors.grey : Colors.black,
                  ),
                ),
              ),
            ),
            SizedBox(width: 8),
            IconButton(
              icon: Icon(Icons.folder_open),
              onPressed: onSelect,
              tooltip: '选择路径',
            ),
            IconButton(
              icon: Icon(Icons.clear),
              onPressed: onClear,
              tooltip: '清除路径',
            ),
          ],
        ),
      ],
    );
  }
}