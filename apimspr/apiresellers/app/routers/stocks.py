from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
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
    return db.query(models.Stock).all()
@router.get("/{product_id}", response_model=schemas.StockOut)
def get_stock_by_product_id(
    product_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable pour ce produit")
    return stock