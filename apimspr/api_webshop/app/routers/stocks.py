from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key

router = APIRouter(
    prefix="/stocks",
    tags=["Stocks"],
    dependencies=[Depends(verify_webshop_key)]
)

@router.get("/", response_model=List[schemas.StockOut])
def get_all_stocks(db: Session = Depends(get_db)):
    return crud.get_stock_for_product(db)

@router.post("/", response_model=schemas.StockOut, status_code=status.HTTP_201_CREATED)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return crud.create_stock(db, stock)

@router.put("/by-product/{product_id}", response_model=schemas.StockOut)
def update_stock_by_product_id(product_id: int, updates: schemas.StockUpdate, db: Session = Depends(get_db)):
    return crud.update_stock_by_product_id(db, product_id, updates)

@router.delete("/by-product/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stock_by_product_id(product_id: int, db: Session = Depends(get_db)):
    crud.delete_stock_by_product_id(db, product_id)
    return None

@router.get("/by-product/{product_id}", response_model=schemas.StockOut)
def get_stock_by_product_id(product_id: int, db: Session = Depends(get_db)):
    return crud.get_stock_by_product_id(db, product_id)