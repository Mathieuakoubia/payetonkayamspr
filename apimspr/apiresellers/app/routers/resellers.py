from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.dependencies import get_db, get_current_reseller

router = APIRouter()

print("✅ app.routers.resellers bien importé")



# ➕ Création d’un revendeur (et envoi du QR code)
@router.post("/", response_model=schemas.ResellerOut)
def create_reseller(reseller: schemas.ResellerCreate, db: Session = Depends(get_db)):
    return crud.create_reseller(db, reseller)

# 📥 Lire tous les revendeurs
@router.get("/", response_model=list[schemas.ResellerOut])
def read_resellers(db: Session = Depends(get_db)):
    return db.query(models.Reseller).all()

# 📥 Lire un revendeur par ID
@router.get("/{reseller_id}", response_model=schemas.ResellerOut)
def read_reseller(reseller_id: int, db: Session = Depends(get_db)):
    db_reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not db_reseller:
        raise HTTPException(status_code=404, detail="Revendeur introuvable")
    return db_reseller

# ✏️ Mettre à jour un revendeur
@router.put("/{reseller_id}", response_model=schemas.ResellerOut)
def update_reseller(reseller_id: int, reseller: schemas.ResellerCreate, db: Session = Depends(get_db)):
    db_reseller = crud.update_reseller(db, reseller_id, reseller)
    if not db_reseller:
        raise HTTPException(status_code=404, detail="Revendeur non trouvé")
    return db_reseller

# ❌ Supprimer un revendeur
@router.delete("/{reseller_id}", status_code=204)
def delete_reseller(reseller_id: int, db: Session = Depends(get_db)):
    success = crud.delete_reseller(db, reseller_id)
    if not success:
        raise HTTPException(status_code=404, detail="Revendeur non trouvé")
