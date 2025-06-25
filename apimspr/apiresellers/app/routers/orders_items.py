# routes/order_items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(prefix="/order-items", tags=["Order Items"])

@router.get("/", response_model=list[schemas.OrderItemOut])
def read_order_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), reseller = Depends(get_current_reseller)):
    return crud.get_order_items(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.OrderItemCreate)
def create_order_item(item: schemas.OrderItemCreate, db: Session = Depends(get_db), reseller = Depends(get_current_reseller)):
    return crud.create_order_item(db, item)

@router.put("/{item_id}", response_model=schemas.OrderItemOut)
def update_order_item(item_id: int, item: schemas.OrderItemCreate, db: Session = Depends(get_db), reseller = Depends(get_current_reseller)):
    db_item = crud.update_order_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")
    return db_item

@router.delete("/{item_id}")
def delete_order_item(item_id: int, db: Session = Depends(get_db), reseller = Depends(get_current_reseller)):
    success = crud.delete_order_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order item not found")
    return {"message": "Deleted successfully"}
