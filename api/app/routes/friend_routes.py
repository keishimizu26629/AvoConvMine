import logging
from fastapi import APIRouter, Depends, Body, HTTPException, Request
from sqlalchemy.orm import Session
from controllers.friend_controller import FriendController
from schemas.friend import FriendCreate, FriendUpdate, FriendInDB, FriendDetailRequest, FriendDetailResponse, UpdateFriendDetailsRequest, UpdateFriendDetailsResponse
from schemas.conversation import ConversationInput
from schemas.attribute import AttributeSchema
from utils.jwt import get_current_user_id
from database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/friends/extract_attributes")
async def extract_attributes(
    conversation: ConversationInput = Body(...),
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return await FriendController.extract_and_save_attributes(current_user_id, conversation, db)

@router.get("/attributes", response_model=list[AttributeSchema])
async def get_all_attributes(db: Session = Depends(get_db)):
    return await FriendController.get_all_attributes(db)

@router.post("/attributes/similar")
async def find_similar_attributes(query: str = Body(..., embed=True), db: Session = Depends(get_db)):
    return await FriendController.find_similar_attributes(query, db)

@router.post("/friends/", response_model=FriendInDB)
async def create_friend(
    friend: FriendCreate,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    try:
        return FriendController.create_friend(friend, db, current_user_id)
    except HTTPException as e:
        # HTTPExceptionをそのまま再発生させる
        raise e
    except Exception as e:
        # その他の例外は500 Internal Server Errorとして処理
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/friends/{friend_id}", response_model=FriendInDB)
async def read_friend(friend_id: int, db: Session = Depends(get_db)):
    return await FriendController.get_friend(friend_id, db)

@router.get("/friends/", response_model=list[FriendInDB])
async def read_friends(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    try:
        return FriendController.get_friends(db, current_user_id)
    except HTTPException as e:
        # HTTPExceptionをそのまま再発生させる
        raise e
    except Exception as e:
        # その他の例外は500 Internal Server Errorとして処理
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/friends/{friend_id}", response_model=FriendInDB)
async def update_friend(friend_id: int, friend: FriendUpdate, db: Session = Depends(get_db)):
    return await FriendController.update_friend(friend_id, friend, db)

@router.delete("/friends/{friend_id}")
async def delete_friend(
    friend_id: int,
    db: Session = Depends(get_db)
):
    return await FriendController.delete_friend(friend_id, db)

@router.post("/friend/details", response_model=FriendDetailResponse)
async def get_friend_details_with_history(
    request: FriendDetailRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    try:
        return FriendController.get_friend_details_with_history(db, current_user_id, request)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/friend/update", response_model=UpdateFriendDetailsResponse)
async def update_friend_details(
    request: UpdateFriendDetailsRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    logger.info(f"Received update request for friend_id: {request.friend_id}")
    try:
        result = FriendController.update_friend_details(db, current_user_id, request)
        logger.info(f"Successfully updated friend details for friend_id: {request.friend_id}")
        return result
    except HTTPException as e:
        logger.error(f"HTTP exception occurred: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/test-friends")
async def test_create_friend(
    friend: FriendCreate,
    current_user_id: int = Depends(get_current_user_id)
):
    return {
        "message": "認証成功",
        "user_id": current_user_id,
        "friend_name": friend.name
    }
