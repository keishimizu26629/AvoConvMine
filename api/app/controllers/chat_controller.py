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
                answer=result["answer"],
                approximation=result.get("approximation"),
                similarity_category=similarity_category
            )
        # elif question_category == 2:
        #     # Category 2の処理
        #     result = await ChatProcessingService.process_category_2(db, user_id, who, what)
        #     return ChatResponse(
        #         question_category=question_category,
        #         response=Category2Response(
        #             who=who,
        #             what=what,
        #             answer=result
        #         )
        #     )
        # elif question_category == 3:
        #     # Category 3の処理
        #     result = await ChatProcessingService.process_category_3(db, user_id, what)
        #     return ChatResponse(
        #         question_category=question_category,
        #         response=Category3Response(
        #             what=what,
        #             who=result.get("who"),
        #             answer=result.get("answer")
        #         )
        #     )
        # elif question_category == 4:
        #     # Category 4の処理
        #     description = await ChatProcessingService.process_category_4(db, user_id, who)
        #     return ChatResponse(
        #         question_category=question_category,
        #         response=Category4Response(
        #             who=who,
        #             description=description
        #         )
        #     )
        else:
            # 未知のカテゴリの場合
            return ChatResponse(
                question_category=0,
                response={"error": "Unknown question category"}
            )
        return ChatResponse(
            question_category=initial_response.question_category,
            response=response
        )
