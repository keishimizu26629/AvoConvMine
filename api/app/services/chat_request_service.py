from sqlalchemy.orm import Session
from app.models.chat_history import ChatRequest

class ChatRequestService:
    @staticmethod
    async def save_chat_request(db: Session, user_id: int, content: str):
        chat_request = ChatRequest(user_id=user_id, content=content)
        db.add(chat_request)
        db.commit()
        db.refresh(chat_request)
        return chat_request
