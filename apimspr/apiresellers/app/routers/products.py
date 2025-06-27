from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/products",
    tags=["Produits"],
    dependencies=[Depends(get_current_reseller)]
)

# Lire tous les produits
@router.get("/", response_model=list[schemas.Product])
def read_all_products(db: Session = Depends(get_db)):
    return crud.get_product(db)

# Lire un produit par ID
@router.get("/{product_id}", response_model=schemas.Product)
def read_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return product

@router.get("/by_category/{category_id}", response_model=list[schemas.Product])
def read_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return db.query(models.Product).filter(models.Product.category_id == category_id).all()
