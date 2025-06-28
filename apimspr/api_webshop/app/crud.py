from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from hashlib import sha1

from . import models, schemas

# Auth Webshop : Clé API unique
def is_webshop_key_valid(db: Session, api_key: str):
    key_hash = sha1(api_key.encode()).hexdigest()
    return db.query(models.ApiKey).filter(
        models.ApiKey.key_hash == key_hash,
        models.ApiKey.revoked == False,
        models.ApiKey.type == 'webshop'
    ).first() is not None

# Produits
def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product

def get_products_by_category(db: Session, category_id: int):
    return db.query(models.Product).filter(models.Product.category_id == category_id).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, updates: schemas.ProductUpdate):
    db_product = get_product_by_id(db, product_id)
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)
    db.delete(db_product)
    db.commit()
    return {"message": "Produit supprimé avec succès"}

# Catégories
def get_all_categories(db: Session):
    return db.query(models.Category).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, updates: schemas.CategoryUpdate):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Catégorie introuvable")
    db.delete(category)
    db.commit()
    return {"message": "Catégorie supprimée avec succès"}

# Stocks
def get_stock_for_product(db: Session, product_id: int):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable")
    return stock

def create_stock(db: Session, stock: schemas.StockCreate):
    # Vérifie si un stock existe déjà pour ce produit
    existing = db.query(models.Stock).filter(models.Stock.product_id == stock.product_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Un stock existe déjà pour ce produit")
    db_stock = models.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_stock_by_product_id(db: Session, product_id: int):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable pour ce produit")
    return stock

def update_stock_by_product_id(db: Session, product_id: int, updates: schemas.StockUpdate):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable pour ce produit")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(stock, key, value)
    db.commit()
    db.refresh(stock)
    return stock

def delete_stock_by_product_id(db: Session, product_id: int):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable pour ce produit")
    db.delete(stock)
    db.commit()
    return {"message": "Stock supprimé avec succès"}

# Clients et prospects
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict(), is_active=True)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_all_customers(db: Session):
    return db.query(models.Customer).filter(models.Customer.is_active == True).all()

def get_customer_by_id(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id, models.Customer.is_active == True).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return customer

def update_customer(db: Session, customer_id: int, updates: schemas.CustomerUpdate):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer_id: int):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    db.delete(customer)
    db.commit()
    return {"message": "Client supprimé avec succès"}

def create_prospect(db: Session, prospect: schemas.ProspectCreate):
    db_prospect = models.Prospect(**prospect.dict())
    db.add(db_prospect)
    db.commit()
    db.refresh(db_prospect)
    return db_prospect

def update_prospect(db: Session, prospect_id: int, updates: schemas.ProspectUpdate):
    prospect = db.query(models.Prospect).filter(models.Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(prospect, key, value)
    db.commit()
    db.refresh(prospect)
    return prospect

def delete_prospect(db: Session, prospect_id: int):
    prospect = db.query(models.Prospect).filter(models.Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    db.delete(prospect)
    db.commit()
    return {"message": "Prospect supprimé avec succès"}

# Commandes
def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict(), created_at=datetime.now())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_all_prospects(db: Session):
    return db.query(models.Prospect).all()

def get_prospect_by_id(db: Session, prospect_id: int):
    prospect = db.query(models.Prospect).filter(models.Prospect.id == prospect_id).first()
    if not prospect:
        raise HTTPException(status_code=404, detail="Prospect introuvable")
    return prospect

def update_order(db: Session, order_id: int, updates: schemas.OrderUpdate):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    db.delete(order)
    db.commit()
    return {"message": "Commande supprimée avec succès"}

def get_order_items_by_order_id(db: Session, order_id: int):
    return db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).all()

def create_order_item(db: Session, order_item: schemas.OrderItemCreate):
    db_item = models.OrderItem(**order_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_order_item_by_order_id(db: Session, order_id: int, updates: schemas.OrderItemCreate):
    item = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ligne de commande introuvable")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

def delete_order_item_by_order_id(db: Session, order_id: int):
    item = db.query(models.OrderItem).filter(models.OrderItem.order_id == order_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ligne de commande introuvable")
    db.delete(item)
    db.commit()
    return {"message": "Ligne de commande supprimée"}
