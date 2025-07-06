import 'package:flutter/material.dart';
import 'qr_scan_page.dart';
import 'register_page.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PayeTonKawa',
      theme: ThemeData(primarySwatch: Colors.teal),
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('fr', 'FR'),
      ],
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  void _goToScanner(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => QRScanScreen()),
    );
  }

  void _goToRegister(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => RegisterPage()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Bienvenue')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _goToScanner(context),
              child: Text('Connexion'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () => _goToRegister(context),
              child: Text('Inscription'),
            ),
          ],
        ),
      ),
    );
  }
}
