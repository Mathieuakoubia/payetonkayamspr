from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)

# ➕ Créer un client
@router.post("/", response_model=schemas.CustomerOut)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)  # on l'inclut même si pas utilisé pour future auth
):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

# 📄 Obtenir tous les clients
@router.get("/", response_model=list[schemas.CustomerOut])
def get_all_customers(
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return db.query(models.Customer).all()
