import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, ApiKey, Product
from app.schemas import ProductCreate
from app import crud, schemas


#  Base de données en mémoire pour tests unitaires
@pytest.fixture(scope="function")
def db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    yield db
    db.close()

# 🔹 Test : Création du revendeur et clé API
def test_create_reseller(db):
    data = schemas.ResellerCreate(
        first_name="Alice",
        last_name="Dupont",
        address="123 rue test",
        email="alice@example.com"
    )

    reseller = crud.create_reseller(db, data)

    assert reseller.id is not None
    assert reseller.email == "alice@example.com"

    key = db.query(ApiKey).filter(ApiKey.reseller_id == reseller.id).first()
    assert key is not None
    assert key.type == "reseller"
    assert key.revoked is False

# 🔹 Test : Clé API invalide → doit retourner None
def test_get_reseller_by_invalid_key(db):
    result = crud.get_reseller_by_api_key(db, "FAKE_KEY")
    assert result is None

def test_get_product_returns_all_products(db):
    # 1. Vérifie que la base est vide au début
    products = crud.get_product(db)
    assert isinstance(products, list)
    assert len(products) == 0

    # 2. Ajoute un produit
    new_product = ProductCreate(
        name="Café Bio",
        description="Un café doux et fruité",
        price=5.99,
        category_id=1,
        image="image.jpg"
    )
    # Ajoute la catégorie pour éviter clé étrangère cassée (si tu as FK)
    from app.models import Category
    category = Category(name="Boissons")
    db.add(category)
    db.commit()
    db.refresh(category)

    new_product.category_id = category.id
    crud.create_product(db, new_product)

    # 3. Vérifie que le produit a été ajouté
    products = crud.get_product(db)
    assert len(products) == 1
    assert products[0].name == "Café Bio"
