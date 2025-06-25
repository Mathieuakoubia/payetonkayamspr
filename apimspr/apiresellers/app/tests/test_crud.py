# app/tests/test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Reseller
from app.crud import get_reseller_by_api_key

# Base de données temporaire en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_get_reseller_by_api_key(db):
    # Arrange : Ajouter un revendeur
    test_reseller = Reseller(
        first_name="Alice",
        last_name="Durand",
        address="123 rue des Fleurs",
        email="alice@example.com",
        api_key="TEST1234",
    )
    db.add(test_reseller)
    db.commit()

    # Act : Appeler la fonction avec la bonne clé
    result = get_reseller_by_api_key(db, "TEST1234")

    # Assert : Vérifier que c'est bien celui qu'on a inséré
    assert result is not None
    assert result.email == "alice@example.com"

