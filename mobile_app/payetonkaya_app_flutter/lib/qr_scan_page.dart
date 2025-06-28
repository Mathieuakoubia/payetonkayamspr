import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'package:http/http.dart' as http;
import 'menu_page.dart';

class QRScanScreen extends StatefulWidget {
  @override
  _QRScanScreenState createState() => _QRScanScreenState();
}

class _QRScanScreenState extends State<QRScanScreen> {
  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');
  QRViewController? controller;
  String? qrCode;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Scanner le QR Code')),
      body: Column(
        children: [
          Expanded(
            flex: 5,
            child: Stack(
              children: [
                QRView(
                  key: qrKey,
                  onQRViewCreated: _onQRViewCreated,
                ),
                Center(
                  child: Container(
                    width: 250,
                    height: 250,
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.teal, width: 4),
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ],
            ),
          ),
          if (qrCode != null)
            Expanded(
              child: Center(
                child: Text('Clé API scannée : $qrCode'),
              ),
            ),
        ],
      ),
    );
  }

  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) async {
      controller.pauseCamera();
      final scannedKey = scanData.code;

      if (scannedKey == null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('QR code invalide')),
        );
        controller.resumeCamera();
        return;
      }

      final response = await http.get(
        Uri.parse('https://apirevendeurmspr.onrender.com/resellers/by_key/$scannedKey'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final firstName = data['first_name'];

        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => MenuPage(nom: firstName, apiKey: scannedKey),
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Clé API invalide ou non reconnue')),
        );
        controller.resumeCamera();
      }
    });
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }
}
