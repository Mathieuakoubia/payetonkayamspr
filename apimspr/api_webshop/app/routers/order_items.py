from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key

router = APIRouter(
    prefix="/order_items",
    tags=["Order_Items"],
    dependencies=[Depends(verify_webshop_key)]
)

@router.get("/order-items/{order_id}", response_model=list[schemas.OrderItemOut])
def get_order_items(order_id: int, db: Session = Depends(get_db)):
    return crud.get_order_items_by_order_id(db, order_id)

@router.post("/order-items/", response_model=schemas.OrderItemOut, status_code=status.HTTP_201_CREATED)
def create_order_item(order_item: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return crud.create_order_item(db, order_item)

@router.put("/order-items/{order_id}", response_model=schemas.OrderItemOut)
def update_order_item(order_id: int, updates: schemas.OrderItemCreate, db: Session = Depends(get_db)):
    return crud.update_order_item_by_order_id(db, order_id, updates)

@router.delete("/order-items/{order_id}")
def delete_order_item(order_id: int, db: Session = Depends(get_db)):
    return crud.delete_order_item_by_order_id(db, order_id)

