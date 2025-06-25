from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

# 📄 Obtenir toutes les commandes d'un client
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


# 🆕 Créer une commande pour un client
@router.post("/", response_model=schemas.OrderOut)
def create_order(
    order_data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    # Vérifie que le client existe
    customer = crud.get_customer(db, order_data.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")

    return crud.create_order(db, order_data)
