class ServerConstants {
  // 服务器配置
  static const int defaultAppiumPort = 4723;
  static const int defaultPythonPort = 5000;
  static const Duration serverTimeout = Duration(seconds: 20);
  
  // 服务器类型
  static const String appiumType = 'appium';
  static const String pythonType = 'python';
  
  // 服务器路径
  static const String appiumCommand = 'appium';
  static const List<String> appiumArgs = ['--relaxed-security'];
}