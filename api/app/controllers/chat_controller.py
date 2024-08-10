import logging
from fastapi import Depends
from sqlalchemy.orm import Session
from schemas.chat import ChatRequest, ChatResponse, Category1Response, Category2Response, Category3Response, Category4Response, InitialChatResponse
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
            result, similarity_category = await ChatProcessingService.process_category_1(
                db,
                user_id,
                initial_response.who,
                initial_response.what,
                initial_response.related_subject
            )
            response = Category1Response(
                who=initial_response.who,
                what=initial_response.what,
                related_subject=initial_response.related_subject,
                status=result["status"],
                answer=result["answer"] if isinstance(result["answer"], (str, dict)) else None,
                approximation=result.get("approximation"),
                similarity_category=similarity_category,
                final_answer=result.get("final_answer")
            )
        elif initial_response.question_category == 2:
            result, similarity_category = await ChatProcessingService.process_category_2(
                db,
                user_id,
                initial_response.who,
                initial_response.what,
                initial_response.related_subject,
                content
            )
            response = Category2Response(
                who=initial_response.who,
                what=initial_response.what,
                status=result["status"],
                answer=result["answer"],
                approximation=result.get("approximation"),
                similarity_category=similarity_category,
                final_answer=result.get("final_answer")
            )
        elif initial_response.question_category == 3:
            result, similarity_category = await ChatProcessingService.process_category_3(
                db,
                user_id,
                initial_response.what
            )
            response = Category3Response(
                who=initial_response.who,
                what=initial_response.what,
                related_subject=initial_response.related_subject,
                status=result["status"],
                answer=result["answer"],
                approximation=result.get("approximation"),
                similarity_category=similarity_category,
                final_answer=result.get("final_answer")
            )
        # In ChatController
        elif initial_response.question_category == 4:
            result, confidence = await ChatProcessingService.process_category_4(
                db,
                user_id,
                initial_response.who
            )
            response = Category4Response(
                who=initial_response.who,
                what=initial_response.what or "general description",
                related_subject=initial_response.related_subject,
                status=result.get("status", "Unknown"),
                answer=result.get("answer"),
                summary=result.get("summary", "Summary not available."),
                missing_info=result.get("missing_info"),
                approximation=result.get("approximation"),
                similarity_category=confidence,
                final_answer=result.get("final_answer")
            )
        else:
            # 他のカテゴリーの処理（必要に応じて追加）
            response = None

        return ChatResponse(
            question_category=initial_response.question_category,
            response=response
        )

    @staticmethod
    async def process_test_chat(user_id: int, content: str, db: Session = Depends(get_db)) -> InitialChatResponse:
        initial_response = await ChatService.process_chat(user_id, content, db)
        logger.debug(f"Initial ChatResponse: {initial_response}")
        return initial_response
