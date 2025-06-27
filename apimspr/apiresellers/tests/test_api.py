from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime
from hashlib import sha1
from uuid import uuid4

from app.main import app
from app.models import Reseller, ApiKey, Base
from app.Databases import get_db  

# Utilisation de SQLite en mémoire pour isoler les tests
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables
Base.metadata.create_all(bind=engine)

# Remplacement de la dépendance par une BDD de test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

#  Définition du client après la surcharge de dépendance
client = TestClient(app)

# ------------------------------------------------------
# FONCTION UTILITAIRE
# ------------------------------------------------------

def add_reseller_with_api_key(db: Session, revoked=False, is_active=True):
    reseller = Reseller(
        first_name="Jean",
        last_name="Testeur",
        address="123 rue test",
        email=f"jean_{uuid4().hex[:6]}@example.com",
        created_at=datetime.now(),
        is_active=is_active
    )
    db.add(reseller)
    db.commit()
    db.refresh(reseller)

    raw_key = f"CLEF_VALID_TEST_{uuid4().hex}"
    key_hash = sha1(raw_key.encode()).hexdigest()
    key = ApiKey(
        key_hash=key_hash,
        reseller_id=reseller.id,
        created_at=datetime.now(),
        type="reseller",
        revoked=revoked
    )
    db.add(key)
    db.commit()
    db.refresh(key)
    return raw_key

# ------------------------------------------------------
# TESTS
# ------------------------------------------------------

def test_create_reseller_via_api():
    response = client.post("/resellers/", json={
        "first_name": "Alice",
        "last_name": "Doe",
        "address": "456 rue API",
        "email": f"alice_{uuid4().hex[:6]}@api.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert "email" in data

# def test_access_with_valid_key():
#     db = TestingSessionLocal()
#     key = add_reseller_with_api_key(db)
#     db.close()
#     response = client.get("/resellers/", headers={"X-API-Key": key})
#     assert response.status_code == 200


def test_access_without_key():
    response = client.get("/resellers/")
    assert response.status_code == 403

def test_access_with_invalid_key():
    response = client.get("/resellers/", headers={"X-API-Key": "FAUSSE_CLE"})
    assert response.status_code == 401

def test_access_with_revoked_key():
    db = TestingSessionLocal()
    key = add_reseller_with_api_key(db, revoked=True)
    db.close()
    response = client.get("/resellers/", headers={"X-API-Key": key})
    assert response.status_code in [401, 403]

# def test_access_with_inactive_reseller():
#     db = TestingSessionLocal()
#     key = add_reseller_with_api_key(db, is_active=False)
#     db.close()
#     response = client.get("/resellers/", headers={"X-API-Key": key})
#     assert response.status_code == 403

