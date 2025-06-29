from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .databases import engine
from . import models
from .routers import customers, prospects, products, orders, stocks, categories, order_items


# Création des tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Webshop - PayeTonKawa")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(customers.router, tags=["Customers"])
app.include_router(prospects.router, tags=["Prospects"])
app.include_router(products.router, tags=["Products"])
app.include_router(orders.router,)
app.include_router(stocks.router, tags=["Stocks"])
app.include_router(categories.router, tags=["Categories"])
app.include_router(order_items.router,)