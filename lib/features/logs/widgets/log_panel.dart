import 'package:flutter/material.dart';
import '../../../core/utils/logger.dart';

class LogPanel extends StatefulWidget {
  final String title;
  final LogType logType;

  const LogPanel({
    Key? key,
    required this.title,
    required this.logType,
  }) : super(key: key);

  @override
  _LogPanelState createState() => _LogPanelState();
}

class _LogPanelState extends State<LogPanel> {
  final List<LogMessage> _logs = [];
  final Logger _logger = Logger();
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _logger.logStream.listen((log) {
      if (log.type == widget.logType) {
        setState(() {
          _logs.add(log);
        });
        _scrollToBottom();
      }
    });
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Padding(
          padding: EdgeInsets.all(8.0),
          child: Text(widget.title, 
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
        ),
        Expanded(
          child: Container(
            margin: EdgeInsets.all(8.0),
            padding: EdgeInsets.all(8.0),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.grey),
              borderRadius: BorderRadius.circular(4.0),
            ),
            child: ListView.builder(
              controller: _scrollController,
              itemCount: _logs.length,
              itemBuilder: (context, index) {
                final log = _logs[index];
                return Text(
                  '${log.timestamp.toString().split('.')[0]} ${log.message}',
                  style: TextStyle(
                    color: Colors.black,
                    fontFamily: 'Monospace',
                  ),
                );
              },
            ),
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }
}