from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(verify_webshop_key)]
)


@router.post("/", response_model=schemas.CustomerOut, status_code=201)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@router.get("/", response_model=List[schemas.CustomerOut])
def get_all_customers(db: Session = Depends(get_db)):
    return crud.get_all_customers(db)

@router.get("/{customer_id}", response_model=schemas.CustomerOut)
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_by_id(db, customer_id)

@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(customer_id: int, updates: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    return crud.update_customer(db, customer_id, updates)

@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return crud.delete_customer(db, customer_id)