from sqlalchemy.orm import Session
from .Databases import SessionLocal

from fastapi import Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from . import crud, Databases


API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_db():
    db = Databases.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_reseller(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if not api_key:
        raise HTTPException(status_code=403, detail="Clé API manquante")
    reseller = crud.get_reseller_by_api_key(db, api_key=api_key)
    if not reseller:
        raise HTTPException(status_code=401, detail="Clé API invalide ou inconnue")
    if not reseller.is_active:
        raise HTTPException(status_code=403, detail="Ce compte revendeur est désactivé")
    return reseller
