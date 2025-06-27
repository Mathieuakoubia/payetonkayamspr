from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL_1 = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+psycopg2://")
engine_1 = create_engine(DATABASE_URL_1)
SessionLocal_1 = sessionmaker(bind=engine_1, autocommit=False, autoflush=False)


# Modèle commun 
Base = declarative_base()

# Dépendances FastAPI
def get_db():
    db = SessionLocal_1()
    try:
        yield db
    finally:
        db.close()


