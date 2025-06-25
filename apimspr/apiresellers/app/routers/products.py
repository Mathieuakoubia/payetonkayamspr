from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[],
)

# ➕ Ajouter un produit
@router.post("/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return crud.create_product_for_reseller(db=db, product=product, reseller_id=reseller.id)


# 📄 Lister les produits du revendeur connecté
@router.get("/", response_model=list[schemas.Product])
def read_my_products(
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return crud.get_products_by_reseller(db=db, reseller_id=reseller.id)

# 🖊️ Mettre à jour un produit
@router.put("/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product_update: schemas.ProductCreate,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    product = crud.get_product(db, product_id)
    if not product or product.reseller_id != reseller.id:
        raise HTTPException(status_code=404, detail="Produit introuvable ou non autorisé")
    
    for key, value in product_update.dict().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

# ❌ Supprimer un produit
@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    product = crud.get_product(db, product_id)
    if not product or product.reseller_id != reseller.id:
        raise HTTPException(status_code=404, detail="Produit introuvable ou non autorisé")
    
    db.delete(product)
    db.commit()
    return