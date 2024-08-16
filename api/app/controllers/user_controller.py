from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate

class UserController:
    @staticmethod
    def create_user(user: UserCreate, db: Session):
        return UserService.create_user(db, user)

    @staticmethod
    def get_user(user_id: int, db: Session):
        user = UserService.get_user(db, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def get_users(skip: int, limit: int, db: Session):
        return UserService.get_users(db, skip, limit)

    @staticmethod
    def update_user(user_id: int, user: UserUpdate, db: Session):
        updated_user = UserService.update_user(db, user_id, user)
        if updated_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user

    @staticmethod
    def delete_user(user_id: int, db: Session):
        deleted_user = UserService.delete_user(db, user_id)
        if deleted_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
