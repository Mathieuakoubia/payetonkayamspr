from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.Databases import engine
from app.dependencies import get_db
from app.routers import resellers, products, stocks, orders, orders_items, customers

from app.models import Base  # Assure-toi que Base est importé ici

# Crée les tables dans la base si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Revendeur PayeTonKawa",
    description="API pour gérer les revendeurs, produits, stocks et commandes",
    version="1.0.0"
)

# CORS (pour permettre à l'app mobile de communiquer avec l’API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(resellers.router, prefix="/resellers", tags=["Resellers"])
app.include_router(customers.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(stocks.router)
app.include_router(orders_items.router)
