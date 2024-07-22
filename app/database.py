from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import get_env

Engine = create_engine(get_env().database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
BaseModel = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
