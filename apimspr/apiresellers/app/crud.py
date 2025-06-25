from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException
from datetime import datetime

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import qrcode
import os
import secrets

from . import models
from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_reseller_by_api_key(db: Session, api_key: str):
    return db.query(models.Reseller).filter(models.Reseller.api_key == api_key).first()

def is_api_key_unique(db: Session, api_key: str) ->bool:
    return not db.query(models.Reseller).filter(models.Reseller.api_key == api_key).first()

def create_reseller(db: Session, reseller: schemas.ResellerCreate):
    while True:
        api_key = secrets.token_urlsafe(32)
        if is_api_key_unique(db, api_key):
            break

    db_reseller = models.Reseller(
        first_name=reseller.first_name,
        last_name=reseller.last_name,
        address=reseller.address,
        email=reseller.email,
        created_at= datetime.now(),
        api_key=api_key
    )

    qr_data = f"API_KEY: {api_key}"
    qr_path = f"qrcodes/{db_reseller.first_name}_{db_reseller.last_name}.png"
    os.makedirs("qrcodes", exist_ok=True)
    qr = qrcode.make(qr_data)
    qr.save(qr_path)

    send_email_with_qrcode(reseller.email, qr_path)

    db.add(db_reseller)
    db.commit()
    db.refresh(db_reseller)
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

def get_products_by_reseller(db: Session, reseller_id: int):
    return db.query(models.Product).filter(models.Product.reseller_id == reseller_id).all()

def update_stock(db: Session, product_id: int, quantity: int):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if stock:
        stock.quantity = quantity
        db.commit()
        db.refresh(stock)
    return stock



def create_product_for_reseller(db: Session, product: schemas.ProductCreate, reseller_id: int):
    db_product = models.Product(**product.dict(), reseller_id=reseller_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_stock_by_reseller(db: Session, reseller_id: int):
    return (
        db.query(models.Stock)
        .join(models.Product)
        .filter(models.Product.reseller_id == reseller_id)
        .all()
    )

def update_stock(db: Session, product_id: int, quantity: int):
    stock = db.query(models.Stock).filter(models.Stock.product_id == product_id).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock introuvable")
    stock.quantity = quantity
    db.commit()
    db.refresh(stock)
    return stock

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_orders_by_customer(db: Session, customer_id: int):
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

def create_order(db: Session, order_data: schemas.OrderCreate):
    db_order = models.Order(**order_data.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

