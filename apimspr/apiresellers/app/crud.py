from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import os
import secrets
import qrcode
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from hashlib import sha1

from . import models
from . import schemas

# Reseller 

def is_api_key_unique(db: Session, key_hash: str) -> bool:
    return not db.query(models.ApiKey).filter(models.ApiKey.key_hash == key_hash).first()

def get_reseller_by_api_key(db: Session, api_key: str):
    key_hash = sha1(api_key.encode()).hexdigest()
    key = db.query(models.ApiKey).filter(
        models.ApiKey.key_hash == key_hash,
        models.ApiKey.revoked == False,
        models.ApiKey.type == 'reseller'
    ).first()
    return key.reseller if key and key.reseller else None

def create_reseller(db: Session, reseller: schemas.ResellerCreate):
    # Vérifier si l'email existe déjà
    existing = db.query(models.Reseller).filter(models.Reseller.email == reseller.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email déjà existant")

    # Créer le revendeur
    db_reseller = models.Reseller(
        first_name=reseller.first_name,
        last_name=reseller.last_name,
        address=reseller.address,
        email=reseller.email,
        created_at=datetime.now()
    )
    db.add(db_reseller)
    db.commit()
    db.refresh(db_reseller)

    # Générer une clé unique
    raw_key = secrets.token_urlsafe(32)
    key_hash = sha1(raw_key.encode()).hexdigest()

    # Enregistrer la clé hashée
    db_key = models.ApiKey(
        key_hash=key_hash,
        type="reseller",
        reseller_id=db_reseller.id,
        created_at=datetime.now()
    )
    db.add(db_key)
    db.commit()

    # Générer et envoyer le QR code
    qr_data = f"{raw_key}"
    qr_path = f"qrcodes/{db_reseller.first_name}_{db_reseller.last_name}.png"
    os.makedirs("qrcodes", exist_ok=True)
    qr = qrcode.make(qr_data)
    qr.save(qr_path)

    send_email_with_qrcode(reseller.email, qr_path)

    return db_reseller

def send_email_with_qrcode(to_email: str, qr_code_path: str):
    from_email = "matheothedon@gmail.com"
    password = "gopu zgei jvjy msrh"
    subject = "Votre QR Code pour l'authentification"

    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    body = "Veuillez scanner ce QR Code pour vous connecter à l'application."
    message.attach(MIMEText(body, 'plain'))

    with open(qr_code_path, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename=qr_code.png")
        message.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(message)
        server.quit()
        print(f"E-mail envoyé à {to_email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")

def update_reseller(db: Session, reseller_id: int, reseller_data: schemas.ResellerCreate):
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        return None
    reseller.first_name = reseller_data.first_name
    reseller.last_name = reseller_data.last_name
    reseller.address = reseller_data.address
    reseller.email = reseller_data.email
    db.commit()
    db.refresh(reseller)
    return reseller

def delete_reseller(db: Session, reseller_id: int):
    reseller = db.query(models.Reseller).filter(models.Reseller.id == reseller_id).first()
    if not reseller:
        return False
    db.delete(reseller)
    db.commit()
    return True

#  Product 

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products_by_category(db: Session, category_id: int):
    return db.query(models.Product).filter(models.Product.category_id == category_id).all()


#  Stock

def get_all_stock(db: Session):
    return db.query(models.Stock).all()

def get_stock_by_product_id(db: Session, product_id: int):
    return db.query(models.Stock).filter(models.Stock.product_id == product_id).first()


#  categories


def get_all_categories(db: Session):
    return db.query(models.Category).all()


