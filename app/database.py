from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 支援多種環境的資料庫連線
DATABASE_URL = (
    os.getenv("DATABASE_URL") or 
    os.getenv("POSTGRES_URL") or 
    "postgresql://postgres:postgres@localhost:5432/crm_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
