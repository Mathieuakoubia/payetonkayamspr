import pytest
from app import crud, schemas
from sqlalchemy.orm import Session
from datetime import date
import os
from fastapi.testclient import TestClient
from app.main import app  # Adjust this import if your FastAPI app is defined elsewhere
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.databases import Base

# Nouvelle base SQLite en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables pour les tests
Base.metadata.create_all(bind=engine)

# Dépendance de test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override la dépendance dans l'app FastAPI
app.dependency_overrides = {}
app.dependency_overrides['get_db'] = override_get_db

client = TestClient(app)
HEADERS = {"x-api-key": os.getenv("WEBSHOP_API_KEY", "clef_tres_longue_et_complexe")}

#  Produits 

def test_get_products():
    response = client.get("/products/", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#  Clients 

def test_create_customer():
    payload = {
        "first_name": "Alice",
        "last_name": "Durand",
        "address": "456 rue Test",
        "birthdate": "1995-05-10",
        "email": "alice@example.com"
    }
    response = client.post("/customers/", json=payload, headers=HEADERS)
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]

# Commandes

def test_create_order():
    payload = {
        "customer_id": 1
    }
    response = client.post("/orders/", json=payload, headers=HEADERS)
    assert response.status_code == 201
    assert "id" in response.json()