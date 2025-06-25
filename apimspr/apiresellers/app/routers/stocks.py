from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"],
)

# 📄 Obtenir le stock de tous les produits du revendeur
@router.get("/", response_model=list[schemas.StockOut])
def get_my_stock(
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return crud.get_stock_by_reseller(db=db, reseller_id=reseller.id)

# 🔄 Mettre à jour le stock d’un produit
@router.put("/{product_id}", response_model=schemas.StockOut)
def update_stock(
    product_id: int,
    stock_update: schemas.StockUpdate,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    # Vérifier que le produit appartient bien au revendeur
    product = crud.get_product(db, product_id)
    if not product or product.reseller_id != reseller.id:
        raise HTTPException(status_code=404, detail="Produit non trouvé ou non autorisé")

    return crud.update_stock(db=db, product_id=product_id, quantity=stock_update.quantity)
