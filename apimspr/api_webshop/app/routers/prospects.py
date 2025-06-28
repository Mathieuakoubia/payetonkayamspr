from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key

router = APIRouter(
    prefix="/prospects",
    tags=["Prospects"],
    dependencies=[Depends(verify_webshop_key)]
)
@router.get("/", response_model=List[schemas.ProspectOut])
def get_all_prospects(db: Session = Depends(get_db)):
    return crud.get_all_prospects(db)



@router.post("/", response_model=schemas.ProspectOut, status_code=status.HTTP_201_CREATED)
def create_prospect(prospect: schemas.ProspectCreate, db: Session = Depends(get_db)):
    return crud.create_prospect(db, prospect)

@router.get("/{prospect_id}", response_model=schemas.ProspectOut)
def get_prospect_by_id(prospect_id: int, db: Session = Depends(get_db)):
    return crud.get_prospect_by_id(db, prospect_id)

@router.put("/{prospect_id}", response_model=schemas.ProspectOut)
def update_prospect(prospect_id: int, updates: schemas.ProspectUpdate, db: Session = Depends(get_db)):
    return crud.update_prospect(db, prospect_id, updates)

@router.delete("/{prospect_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_prospect(prospect_id: int, db: Session = Depends(get_db)):
    crud.delete_prospect(db, prospect_id)
    return None
