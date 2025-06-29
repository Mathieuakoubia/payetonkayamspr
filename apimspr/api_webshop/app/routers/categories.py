from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(verify_webshop_key)]
)

# Get all categories
@router.get("/", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)

# Create a category
@router.post("/", response_model=schemas.CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

# Update a category
@router.put("/{category_id}", response_model=schemas.CategoryOut)
def update_category(category_id: int, updates: schemas.CategoryUpdate, db: Session = Depends(get_db)):
    return crud.update_category(db, category_id, updates)

# Delete a category
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db, category_id)