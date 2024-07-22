from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.user_controller import UserController
from schemas.user import UserCreate, UserUpdate, UserInDB
from database import get_db

router = APIRouter()

@router.post("/users/", response_model=UserInDB)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserController.create_user(user, db)

@router.get("/users/{user_id}", response_model=UserInDB)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.get_user(user_id, db)

@router.get("/users/", response_model=list[UserInDB])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserController.get_users(skip, limit, db)

@router.put("/users/{user_id}", response_model=UserInDB)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UserController.update_user(user_id, user, db)

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserController.delete_user(user_id, db)
