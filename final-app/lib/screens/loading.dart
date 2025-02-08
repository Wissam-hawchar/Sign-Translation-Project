import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

class LoadingPage extends StatefulWidget {
  final Widget nextScreen;

  const LoadingPage({Key? key, required this.nextScreen}) : super(key: key);

  @override
  State<LoadingPage> createState() => _LoadingPageState();
}

class _LoadingPageState extends State<LoadingPage> {
  @override
  void initState() {
    super.initState();
    _preloadResources();
  }

  Future<void> _preloadResources() async {
    try {
      final manifestContent = await rootBundle.loadString('AssetManifest.json');
      final Map<String, dynamic> manifestMap = json.decode(manifestContent);

      final assetsToPreload = manifestMap.keys
          .where((String key) => key.startsWith('assets/'))
          .toList();

      for (String assetPath in assetsToPreload) {
        if (assetPath.endsWith('.png') ||
            assetPath.endsWith('.jpg') ||
            assetPath.endsWith('.gif')) {
          await precacheImage(AssetImage(assetPath), context);
        }
      }

      if (mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (context) => widget.nextScreen),
        );
      }
    } catch (e) {
      print('Error preloading resources: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      backgroundColor: Colors.teal,
      body: Center(
        child: SpinKitDoubleBounce(
          color: Colors.white,
          size: 100.0,
        ),
      ),
    );
  }
}
