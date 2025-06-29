from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"],
)

#  Obtenir tout le stock (consultation seulement)
@router.get("/", response_model=list[schemas.StockOut])
def get_all_stock(
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return crud.get_all_stock(db)

@router.get("/{product_id}", response_model=schemas.StockOut)
def get_stock_by_product_id(
    product_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    stock = crud.get_stock_by_product_id(db, product_id)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable pour ce produit")
    return stock