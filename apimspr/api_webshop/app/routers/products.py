from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os

from .. import schemas, crud
from app.databases import get_db
from app.dependencies import verify_webshop_key
from app.supabase_client import supabase



router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[Depends(verify_webshop_key)]
)

@router.get("/", response_model=List[schemas.Product])
def get_all_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@router.get("/{product_id}", response_model=schemas.Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product_by_id(db, product_id)

@router.put("/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, updates: schemas.ProductUpdate, db: Session = Depends(get_db)):
    return crud.update_product(db, product_id, updates)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    crud.delete_product(db, product_id)
    return None

@router.post("/{product_id}/upload_image")
async def upload_image(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    file_ext = file.filename.split('.')[-1]
    file_path = f"products/{product_id}.{file_ext}"

   
    bucket = supabase.storage.from_("payetonkayaimages")
    # Supprime le fichier existant s'il y en a un
    try:
        bucket.remove(file_path)
    except Exception:
        pass

    res = bucket.upload(file_path, contents, {"content-type": file.content_type})
    if not res:
        raise HTTPException(status_code=500, detail="Erreur lors de l'upload sur Supabase")

    public_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/payetonkayaimages/{file_path}"

    product = crud.get_product_by_id(db, product_id)
    product.image = public_url
    db.commit()
    db.refresh(product)

    return {"image_url": public_url}