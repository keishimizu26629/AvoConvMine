from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import get_env

Engine = create_engine(get_env().DATABASE_URL)  # 小文字から大文字に変更
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)
BaseModel = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
