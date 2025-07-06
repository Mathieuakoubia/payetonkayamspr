import 'package:flutter/material.dart';

class ProductDetailPage extends StatelessWidget {
  final Map product;

  ProductDetailPage({required this.product});

  @override
  Widget build(BuildContext context) {
    final String? imageUrl = product['image'];

    return Scaffold(
      appBar: AppBar(title: Text(product['name'] ?? 'Produit')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (imageUrl != null && imageUrl.isNotEmpty)
              Center(
                child: Image.network(
                  imageUrl,
                  height: 200,
                  errorBuilder: (context, error, stackTrace) {
                    return Text("Impossible de charger l'image");
                  },
                ),
              )
            else
              Center(child: Text("Aucune image disponible")),
            SizedBox(height: 20),
            Text(product['description'] ?? '', style: TextStyle(fontSize: 16)),
            SizedBox(height: 10),
            Text("Prix : ${product['price']} €",
                style: TextStyle(fontSize: 18)),
            SizedBox(height: 20),
          ],
        ),
      ),
    );
  }
}
