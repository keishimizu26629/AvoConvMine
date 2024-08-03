import logging
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas.chat import ChatRequest, ChatResponse, Category1Response, Category2Response, Category3Response
from services.chat_service import ChatService
from services.chat_processing_service import ChatProcessingService
from database import get_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ChatController:
    @staticmethod
    async def process_chat(user_id: int, content: str, db: Session = Depends(get_db)) -> ChatResponse:
        initial_response = await ChatService.process_chat(user_id, content, db)

        logger.debug(f"Initial ChatResponse: {initial_response}")

        if initial_response.question_category == 1:
            result, similarity_category = await ChatProcessingService.process_category_1(db, user_id, initial_response.who, initial_response.what)
            response = Category1Response(
                who=initial_response.who,
                what=initial_response.what,
                status=result["status"],
                answer=result["answer"],
                approximation=result.get("approximation"),
                similarity_category=similarity_category
            )
        elif initial_response.question_category == 2:
            result, similarity_category = await ChatProcessingService.process_category_2(db, user_id, initial_response.who, initial_response.what)
            response = Category2Response(
                who=initial_response.who,
                what=initial_response.what,
                status=result["status"],
                answer=result["answer"],
                approximation=result.get("approximation"),
                similarity_category=similarity_category
            )
        else:
            # 他のカテゴリーの処理（必要に応じて追加）
            response = None

        return ChatResponse(
            question_category=initial_response.question_category,
            response=response
        )
