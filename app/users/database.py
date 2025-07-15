from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.users.config import settings
import os
from sqlalchemy.orm import declarative_base

## this line go to the model folder and Loading all files 
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
