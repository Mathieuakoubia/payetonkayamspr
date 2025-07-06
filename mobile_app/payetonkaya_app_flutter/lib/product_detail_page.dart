import 'package:flutter/material.dart'; // Assure-toi que ce fichier existe et est bien importé

class ProductDetailPage extends StatelessWidget {
  final Map product;

  ProductDetailPage({required this.product});

  @override
  Widget build(BuildContext context) {
    
    final String modelUrl = "https://github.com/KhronosGroup/glTF-Sample-Models/blob/main/2.0/Duck/glTF-Binary/Duck.glb";


    return Scaffold(
      appBar: AppBar(title: Text(product['name'] ?? 'Produit')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(product['description'] ?? '', style: TextStyle(fontSize: 16)),
            SizedBox(height: 10),
            Text("Prix : ${product['price']} €", style: TextStyle(fontSize: 18)),
            SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text("La fonctionnalité AR est temporairement désactivée.")),
                );
              },
              child: Text("Afficher en réalité augmentée"),
            ),
          ],
        ),
      ),
    );
  }
}
