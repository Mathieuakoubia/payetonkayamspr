import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'product_detail_page.dart';

class ProductsPage extends StatefulWidget {
  final String apiKey;
  final http.Client httpClient;

  ProductsPage({required this.apiKey, http.Client? httpClient})
      : httpClient = httpClient ?? http.Client();

  @override
  _ProductsPageState createState() => _ProductsPageState();
}

class _ProductsPageState extends State<ProductsPage> {
  List<Map<String, dynamic>> products = [];

  @override
  void initState() {
    super.initState();
    fetchProducts();
  }

  Future<void> fetchProducts() async {
    final response = await widget.httpClient.get(
      Uri.parse('https://apirevendeurmspr.onrender.com/products/'),
      headers: {'X-API-Key': widget.apiKey},
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = json.decode(utf8.decode(response.bodyBytes));
      setState(() {
        products = data.cast<Map<String, dynamic>>();
      });
    } else {
      print('Erreur lors du chargement des produits');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Produits")),
      body: products.isEmpty
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: products.length,
              itemBuilder: (context, index) {
                var product = products[index];
                return ListTile(
                  title: Text(product['name'] ?? 'Produit inconnu'),
                  subtitle: Text("Prix : ${product['price']} €"),
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => ProductDetailPage(product: product),
                      ),
                    );
                  },
                );
              },
            ),
    );
  }
}
