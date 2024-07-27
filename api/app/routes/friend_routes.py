from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.orm import Session
from controllers.friend_controller import FriendController
from schemas.friend import FriendCreate, FriendUpdate, FriendInDB
from schemas.conversation import ConversationInput
from schemas.attribute import AttributeSchema
from database import get_db

router = APIRouter()

@router.post("/friends/extract_attributes")
async def extract_attributes(conversation: ConversationInput = Body(...), db: Session = Depends(get_db)):
    return await FriendController.extract_and_save_attributes(conversation, db)

@router.get("/attributes", response_model=list[AttributeSchema])
async def get_all_attributes(db: Session = Depends(get_db)):
    return await FriendController.get_all_attributes(db)

@router.post("/attributes/similar")
async def find_similar_attributes(query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return await FriendController.find_similar_attributes(query, db)

@router.post("/friends/", response_model=FriendInDB)
def create_friend(friend: FriendCreate, db: Session = Depends(get_db)):
    try:
        return FriendController.create_friend(friend, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/friends/{friend_id}", response_model=FriendInDB)
async def read_friend(friend_id: int, db: Session = Depends(get_db)):
    return await FriendController.get_friend(friend_id, db)

@router.get("/friends/", response_model=list[FriendInDB])
async def read_friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return await FriendController.get_friends(skip, limit, db)

@router.put("/friends/{friend_id}", response_model=FriendInDB)
async def update_friend(friend_id: int, friend: FriendUpdate, db: Session = Depends(get_db)):
    return await FriendController.update_friend(friend_id, friend, db)

@router.delete("/friends/{friend_id}")
async def delete_friend(friend_id: int, db: Session = Depends(get_db)):
    return await FriendController.delete_friend(friend_id, db)
