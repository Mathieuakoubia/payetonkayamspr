# tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app
from app.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.Databases import get_db

# Crée une BDD SQLite temporaire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables
Base.metadata.create_all(bind=engine)

# Surcharge la dépendance de DB pour les tests
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_reseller():
    # Données d'exemple
    data = {
        "first_name": "Alice",
        "last_name": "Durand",
        "address": "123 rue des Fleurs",
        "email": "alice@example.com",
        "api_key": "TEST1234",
    }

    # Appel de la route POST /resellers/ (à adapter si besoin)
    response = client.post("/resellers/", json=data)

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"
