import logging
from sqlalchemy.orm import Session
from app.models.chat_history import ChatResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class ChatResponseService:
    @staticmethod
    async def save_chat_response(db: Session, request_id: int, response_data: dict):
        logger.debug(f"Received response_data in save_chat_response: {response_data}")
        try:
            # answerフィールドの処理
            answer = response_data['response'].get('answer')
            if isinstance(answer, (list, dict)):
                answer = json.dumps(answer)

            # approximationの処理（既存のコード）
            approximation = response_data['response'].get('approximation')
            if isinstance(approximation, dict):
                approximation_attribute = approximation.get('attribute')
                approximation_value = approximation.get('value')
            elif isinstance(approximation, str):
                approximation_attribute = None
                approximation_value = approximation
            else:
                approximation_attribute = None
                approximation_value = None

            chat_response = ChatResponse(
                request_id=request_id,
                question_category=response_data['question_category'],
                who=response_data['response'].get('who'),
                what=response_data['response'].get('what'),
                related_subject=response_data['response'].get('related_subject'),
                status=response_data['response'].get('status'),
                answer=answer,  # 処理済みのanswer
                approximation_attribute=approximation_attribute,
                approximation_value=approximation_value,
                similarity_category=response_data['response'].get('similarity_category'),
                final_answer=response_data['response'].get('final_answer')
            )
            db.add(chat_response)
            db.commit()
            db.refresh(chat_response)
            return chat_response
        except Exception as e:
            logger.error(f"Error in save_chat_response: {str(e)}", exc_info=True)
            raise
