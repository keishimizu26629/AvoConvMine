from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from schemas.conversation import ConversationInput
from schemas.friend import FriendInDB, AttributeSchema
from controllers.friend_controller import FriendController
from database import get_db

router = APIRouter()

@router.post("/friends/{friend_id}/extract_attributes")
async def extract_attributes(friend_id: int, conversation: ConversationInput, db: Session = Depends(get_db)):
    return await FriendController.extract_and_save_attributes(friend_id, conversation, db)

@router.get("/friends/", response_model=list[FriendInDB])
def read_friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return FriendController.get_friends(skip, limit, db)

@router.get("/attributes", response_model=list[AttributeSchema])
async def get_all_attributes(db: Session = Depends(get_db)):
    return await FriendController.get_all_attributes(db)

@router.post("/attributes/similar")
async def find_similar_attributes(query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return await FriendController.find_similar_attributes(query, db)

@router.post("/attributes/similarities")
async def calculate_similarities(query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return await FriendController.calculate_similarities(query, db)
