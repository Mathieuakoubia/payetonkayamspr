from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(verify_webshop_key)]
)

@router.get("/", response_model=List[schemas.OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    return crud.get_all_orders(db)

@router.post("/", response_model=schemas.OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)

@router.get("/{order_id}", response_model=schemas.OrderOut)
def get_order_by_id(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order_by_id(db, order_id)

@router.put("/{order_id}", response_model=schemas.OrderOut)
def update_order(order_id: int, updates: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.update_order(db, order_id, updates)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    crud.delete_order(db, order_id)
    return None
