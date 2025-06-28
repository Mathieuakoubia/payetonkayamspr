import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.databases import Base
from app import crud, schemas, models
from datetime import date

# Création d'une base SQLite en mémoire 
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Produit

def test_create_product(db_session: Session):
    product = schemas.ProductCreate(
        name="Test Product",
        description="Un produit de test",
        category_id=1,
        price=10.99,
        image="image.jpg"
    )
    result = crud.create_product(db_session, product)
    assert result.name == product.name

def test_get_all_products(db_session: Session):
    result = crud.get_all_products(db_session)
    assert isinstance(result, list)

# Client

def test_create_customer(db_session: Session):
    customer = schemas.CustomerCreate(
        first_name="John",
        last_name="Doe",
        address="123 rue de Test",
        birthdate=date(1990, 1, 1),
        email="john.doe@example.com"
    )
    result = crud.create_customer(db_session, customer)
    assert result.email == customer.email

#  Commandes 

def test_create_order(db_session: Session):
    order = schemas.OrderCreate(
        customer_id=1
    )
    result = crud.create_order(db_session, order)
    assert result.customer_id == order.customer_id
