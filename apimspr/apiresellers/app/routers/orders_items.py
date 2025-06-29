# routes/order_items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.dependencies import get_db, get_current_reseller

router = APIRouter(prefix="/order-items", tags=["Order Items"])

