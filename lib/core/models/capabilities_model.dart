class CapabilitiesModel {
  final String platformName;
  final String udid;
  final String automationName;
  final String platformVersion;
  final String bundleId;
  final String appPath;
  final int newCommandTimeout;
  final int wdaLocalPort;

  CapabilitiesModel({
    this.platformName = 'iOS',
    this.udid = '',
    this.automationName = 'XCUITest',
    this.platformVersion = '',
    this.bundleId = '',
    this.appPath = '',
    this.newCommandTimeout = 60,
    this.wdaLocalPort = 8100,
  });

  Map<String, dynamic> toJson() => {
    'platformName': platformName,
    'appium:udid': udid,
    'appium:automationName': automationName,
    'appium:platformVersion': platformVersion,
    'appium:bundleId': bundleId,
    'appium:app': appPath.isNotEmpty ? appPath : null,
    'appium:newCommandTimeout': newCommandTimeout,
    'appium:wdaLocalPort': wdaLocalPort,
  };

  factory CapabilitiesModel.fromJson(Map<String, dynamic> json) {
    return CapabilitiesModel(
      platformName: json['platformName'] ?? 'iOS',
      udid: json['appium:udid'] ?? '',
      automationName: json['appium:automationName'] ?? 'XCUITest',
      platformVersion: json['appium:platformVersion'] ?? '',
      bundleId: json['appium:bundleId'] ?? '',
      appPath: json['appium:app'] ?? '',
      newCommandTimeout: json['appium:newCommandTimeout'] ?? 60,
      wdaLocalPort: json['appium:wdaLocalPort'] ?? 8100,
    );
  }

  CapabilitiesModel copyWith({
    String? platformName,
    String? udid,
    String? automationName,
    String? platformVersion,
    String? bundleId,
    String? appPath,
    int? newCommandTimeout,
    int? wdaLocalPort,
  }) {
    return CapabilitiesModel(
      platformName: platformName ?? this.platformName,
      udid: udid ?? this.udid,
      automationName: automationName ?? this.automationName,
      platformVersion: platformVersion ?? this.platformVersion,
      bundleId: bundleId ?? this.bundleId,
      appPath: appPath ?? this.appPath,
      newCommandTimeout: newCommandTimeout ?? this.newCommandTimeout,
      wdaLocalPort: wdaLocalPort ?? this.wdaLocalPort,
    );
  }
}