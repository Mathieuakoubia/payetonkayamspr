import 'package:flutter/material.dart';
import 'products_page.dart';


class MenuPage extends StatelessWidget {
  final String nom;
  final String apiKey;

  MenuPage({required this.nom, required this.apiKey});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Menu')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Bienvenue, $nom !',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 30),
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ProductsPage(apiKey: apiKey),
                  ),
                );
              },
              child: Text("Voir les produits"),
            ),
          ],
        ),
      ),
    );
  }
}
