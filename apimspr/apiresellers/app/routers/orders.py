from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
    dependencies=[Depends(get_current_reseller)]
)

@router.get("/", response_model=list[schemas.OrderOut])
def get_all_orders(
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return db.query(models.Order).all()

#  Obtenir toutes les commandes d’un client
@router.get("/customer/{customer_id}", response_model=list[schemas.OrderOut])
def get_orders_by_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    customer = crud.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")

    return crud.get_orders_by_customer(db, customer_id)

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order_by_id(
    order_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return order
