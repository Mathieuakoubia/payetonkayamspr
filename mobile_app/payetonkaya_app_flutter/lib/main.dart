import 'package:flutter/material.dart';
import 'qr_scan_page.dart'; // Ce sera ta page de scan

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PayeTonKawa',
      theme: ThemeData(primarySwatch: Colors.teal),
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Bienvenue')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () => _goToScanner(context), // pour connexion
              child: Text('Connexion'),
            ),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // TODO: Créer une page d'inscription plus tard
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Inscription à venir...')),
                );
              },
              child: Text('Inscription'),
            ),
          ],
        ),
      ),
    );
  }
}
