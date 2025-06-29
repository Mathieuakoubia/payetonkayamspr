from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter()
print(" app.routers.resellers bien importé")

# 1. Créer un revendeur : PUBLIC
@router.post("/",status_code=201, response_model=schemas.ResellerOut)
def create_reseller(reseller: schemas.ResellerCreate, db: Session = Depends(get_db)):
    return crud.create_reseller(db, reseller)

# 2. Obtenir un revendeur par API key : PUBLIC
@router.get("/by_key/{api_key}", response_model=schemas.ResellerOut)
def get_reseller_by_api_key(api_key: str, db: Session = Depends(get_db)):
    reseller = crud.get_reseller_by_api_key(db, api_key)
    if not reseller:
        raise HTTPException(status_code=404, detail="Revendeur introuvable ou clé invalide")
    return reseller

# 3. Lire tous les revendeurs : PROTÉGÉ
@router.get("/", response_model=list[schemas.ResellerOut])
def read_resellers(
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    return db.query(models.Reseller).all()

# 4. Lire un revendeur par ID : PROTÉGÉ
@router.get("/{reseller_id}", response_model=schemas.ResellerOut)
def read_reseller(
    reseller_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    db_reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not db_reseller:
        raise HTTPException(status_code=404, detail="Revendeur introuvable")
    return db_reseller

# 5. Mettre à jour : PROTÉGÉ
@router.put("/{reseller_id}", response_model=schemas.ResellerOut)
def update_reseller(
    reseller_id: int,
    reseller_data: schemas.ResellerCreate,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    db_reseller = crud.update_reseller(db, reseller_id, reseller_data)
    if not db_reseller:
        raise HTTPException(status_code=404, detail="Revendeur non trouvé")
    return db_reseller

# Supprimer : PROTÉGÉ
@router.delete("/{reseller_id}", status_code=204)
def delete_reseller(
    reseller_id: int,
    db: Session = Depends(get_db),
    reseller: models.Reseller = Depends(get_current_reseller)
):
    success = crud.delete_reseller(db, reseller_id)
    if not success:
        raise HTTPException(status_code=404, detail="Revendeur non trouvé")
