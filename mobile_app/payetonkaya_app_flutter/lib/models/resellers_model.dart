class Reseller {
  final String prenom;
  final String nom;
  final String email;
  final String adresse;
  final String dateNaissance;

  Reseller({
    required this.prenom,
    required this.nom,
    required this.email,
    required this.adresse,
    required this.dateNaissance,
  });

  Map<String, dynamic> toJson() => {
    "first_name": prenom,
    "last_name": nom,
    "email": email,
    "address": adresse,
    "birthdate": dateNaissance,
  };
}
