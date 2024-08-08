from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin
from core.config import get_env
from database import get_db
from services.user_service import create_user, authenticate_user
from utils.jwt import create_access_token
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    logger.debug("Success to request!")
    db_user = create_user(db, user)
    return {"message": "User registered successfully", "user_id": db_user.id}

@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})  # user.id を使用
    return {"access_token": access_token, "token_type": "bearer"}
