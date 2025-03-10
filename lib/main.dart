import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'core/constants/server_constants.dart';
import 'features/control/pages/control_page.dart';
import 'features/control/providers/control_state.dart';
import 'features/control/providers/server_state.dart';
import 'services/server/server_service.dart';
import 'services/appium/appium_service.dart';
import 'services/config/config_service.dart';
import 'core/constants/app_constants.dart';
import 'shared/theme/app_theme.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  final configService = ConfigService();
  final serverState = ServerState();
  final serverService = ServerService(
    serverState: serverState,
  );
  
  runApp(MyApp(
    configService: configService,
    serverService: serverService,
    serverState: serverState,  // 添加这行
  ));
}

class MyApp extends StatelessWidget {
  final ConfigService configService;
  final ServerService serverService;
  final ServerState serverState;  // 添加这行

  const MyApp({
    Key? key,
    required this.configService,
    required this.serverService,
    required this.serverState,  // 添加这行
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ControlState()),
        ChangeNotifierProvider.value(value: serverState),  // 修改这行
        Provider.value(value: configService),
        Provider.value(value: serverService),
        Provider(
          create: (_) => AppiumService(
            baseUrl: 'http://${AppConstants.wsHost}:${ServerConstants.defaultPythonPort}',
          ),
        ),
      ],
      child: MaterialApp(
        title: AppConstants.appName,
        theme: AppTheme.lightTheme,
        home: ControlPage(),
      ),
    );
  }
}
