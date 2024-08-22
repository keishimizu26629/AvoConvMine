from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.chat import ChatRequest, ChatResponse, InitialChatResponse, ChatRequestSummary
from controllers.chat_controller import ChatController
from utils.jwt import get_current_user_id
from database import get_db

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def process_chat(
    chat_request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return await ChatController.process_chat(current_user_id, chat_request.content, db)

@router.post("/test-chat", response_model=InitialChatResponse)
async def test_chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    return await ChatController.process_test_chat(chat_request.user_id, chat_request.content, db)

@router.get("/chats/", response_model=List[ChatRequestSummary])
async def get_user_chats(
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    try:
        return ChatController.get_user_chats(db, current_user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
