from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Connexion à la base principale PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg2://")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


Base = declarative_base()

# Dépendance utilisée dans l'API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
