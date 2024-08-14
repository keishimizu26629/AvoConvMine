from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from database import get_db
from controllers.auth_controller import AuthController
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return AuthController.register(user, db)

@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return AuthController.login(user_data, db)
