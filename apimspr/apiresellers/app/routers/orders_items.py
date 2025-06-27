# routes/order_items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.dependencies import get_db, get_current_reseller

router = APIRouter(prefix="/order-items", tags=["Order Items"])

#  Lire tous les éléments de commande (limité)
@router.get("/", response_model=list[schemas.OrderItemOut])
def read_order_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), reseller = Depends(get_current_reseller)):
    return db.query(schemas.models.OrderItem).offset(skip).limit(limit).all()

#  Lire les éléments d’une commande spécifique
@router.get("/order/{order_id}", response_model=list[schemas.OrderItemOut])
def get_items_by_order_id(order_id: int, db: Session = Depends(get_db), reseller = Depends(get_current_reseller)):
    items = db.query(schemas.models.OrderItem).filter_by(order_id=order_id).all()
    if not items:
        raise HTTPException(status_code=404, detail="Aucun élément trouvé pour cette commande")
    return items
