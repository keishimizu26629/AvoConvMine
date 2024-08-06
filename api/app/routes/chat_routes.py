from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.chat import ChatRequest, ChatResponse, InitialChatResponse
from controllers.chat_controller import ChatController
from database import get_db

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def process_chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    content = chat_request.content.strip().lower()  # 入力を正規化
    return await ChatController.process_chat(chat_request.user_id, content, db)

@router.post("/test-chat", response_model=InitialChatResponse)
async def test_chat(chat_request: ChatRequest, db: Session = Depends(get_db)):
    return await ChatController.process_test_chat(chat_request.user_id, chat_request.content, db)
