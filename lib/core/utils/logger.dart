import 'dart:async';

class Logger {
  static final Logger _instance = Logger._internal();
  final _logController = StreamController<LogMessage>.broadcast();

  factory Logger() => _instance;

  Logger._internal();

  Stream<LogMessage> get logStream => _logController.stream;

  void log(String message, LogType type) {
    _logController.add(LogMessage(message: message, type: type));
  }
}

enum LogType {
  appium,
  python,
  info,
  error,
}

class LogMessage {
  final String message;
  final LogType type;
  final DateTime timestamp;

  LogMessage({
    required this.message,
    required this.type,
    DateTime? timestamp,
  }) : timestamp = timestamp ?? DateTime.now();
}