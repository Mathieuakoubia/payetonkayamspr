from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# Get all categories
@router.get("/", response_model=list[schemas.CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)





