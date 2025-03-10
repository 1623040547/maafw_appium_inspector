class ServerStatusModel {
  final bool isRunning;
  final bool isExternal;
  final int port;
  final String type;

  ServerStatusModel({
    required this.isRunning,
    required this.isExternal,
    required this.port,
    required this.type,
  });
}