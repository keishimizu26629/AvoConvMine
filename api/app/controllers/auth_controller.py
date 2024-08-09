from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserResponse, UserLogin, TokenResponse
from services.user_service import UserService
from utils.jwt import create_access_token

class AuthController:
    @staticmethod
    def register(user: UserCreate, db: Session) -> UserResponse:
        db_user = UserService.create_user(db, user)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User registration failed"
            )

        access_token = create_access_token(data={"sub": str(db_user.id)})

        return UserResponse(
            id=db_user.id,
            email=db_user.email,
            name=db_user.name,
            access_token=access_token,
            token_type="bearer"
        )

    @staticmethod
    def login(user_data: UserLogin, db: Session) -> TokenResponse:
        user = UserService.authenticate_user(db, user_data.email, user_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return TokenResponse(access_token=access_token, token_type="bearer")
