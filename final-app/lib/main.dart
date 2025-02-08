import 'package:finalseminar/screens/home.dart';
import 'package:finalseminar/screens/loading.dart';
import 'package:finalseminar/screens/onboarding1.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoadingPageWrapper(), // Start with the LoadingPageWrapper
    );
  }
}

class LoadingPageWrapper extends StatefulWidget {
  const LoadingPageWrapper({Key? key}) : super(key: key);

  @override
  State<LoadingPageWrapper> createState() => _LoadingPageWrapperState();
}

class _LoadingPageWrapperState extends State<LoadingPageWrapper> {
  bool? isFirstLaunch;

  @override
  void initState() {
    super.initState();
    _checkFirstLaunch();
  }

  Future<void> _checkFirstLaunch() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      isFirstLaunch = prefs.getBool('first_launch') ?? true;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (isFirstLaunch == null) {
      // While loading SharedPreferences, show a loading indicator
      return const Scaffold(
        backgroundColor: Colors.teal,
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    // Return the LoadingPage with navigation to the correct screen
    return LoadingPage(
      nextScreen: isFirstLaunch! ? Onboarding1Screen() : Home(),
    );
  }
}
