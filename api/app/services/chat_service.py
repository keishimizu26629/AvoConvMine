import json
import logging
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app.schemas.chat import InitialChatResponse
from app.utils.gemini_api import generate_gemini_response
from app.utils.text_processing import clean_json_response
from app.models.chat_history import ChatRequest, ChatResponse
from app.schemas.chat import ChatRequestSummary, ChatResponseSummary

logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    async def process_chat(user_id: int, content: str, db) -> InitialChatResponse:
        analysis = await ChatService.analyze_question(content)

        return InitialChatResponse(
            who=analysis.get("primary_subject"),
            what=analysis.get("attribute"),
            related_subject=analysis.get("related_subject"),
            question_category=ChatService.get_category_number(analysis.get("category"))
        )

    @staticmethod
    async def analyze_question(question: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following question in English: {question}

        Return a JSON object in the following format:
        {{
            "category": "Question category (①, ②, ③, or ④)",
            "primary_subject": "The main person or group the question is about, or 'unknown' if not specified",
            "related_subject": "Any related person or thing mentioned in the question, or null if none",
            "attribute": "The specific attribute or information being asked about",
            "relation": "The relationship between the primary_subject and related_subject, if applicable",
            "explanation": "Brief explanation of the classification and analysis"
        }}

        Category definitions with examples:
        ①: Questions asking to confirm or inquire about a specific attribute of a specific person or their relation
        Pattern: "Is/Are/Does/Do [Person/Person's relation] [Attribute]?" or similar confirmatory or inquiry questions
        Examples:
        - Is John an engineer?
        - Are Mary and Tom married?
        - Does Karen have a child?

        ②: Questions asking about a specific attribute of a specific person or their relation, typically starting with "What", "Where", "When", "How", or phrases like "tell me about"
        Pattern: "What/Where/When/How is/was [Person/Person's relation]'s [Attribute]?" or "Tell me about [Person's] [Attribute]" or similar specific inquiries
        Examples:
        - What is David's occupation?
        - Where does Emma live?
        - How old is Michael's daughter?
        - Tell me about Karen's occupation

        ③: Questions asking about a person or people with a specific attribute
        Pattern: "Who is/are/has [Attribute]?" or similar questions identifying people by attributes
        Examples:
        - Who is the tallest person in the group?
        - Which employee has the most experience?
        - Who are the new team members?
        - Who has a daughter?
        - Who lives in Tokyo?

        ④: Questions asking for a general description or overview of a specific person
        Pattern: Open-ended questions about a person without specifying an attribute
        Examples:
        - Can you tell me about Lisa?
        - What do you know about Dr. Johnson?

        Important:
        - Pay close attention to the structure and intent of the question.
        - For category ② questions, ensure that both the person (primary_subject) and the attribute are correctly identified, even if the question is phrased as "Tell me about [Person's] [Attribute]".
        - For category ③ questions, the primary_subject should be 'unknown' unless a specific group is mentioned.
        - The attribute for category ③ questions should be the characteristic or possession being asked about.

        Note: Return only the JSON object without any additional explanation.
        """

        response = await generate_gemini_response(prompt)
        cleaned_response = clean_json_response(response.text)

        try:
            return json.loads(cleaned_response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON: {cleaned_response}")
            return {"error": "Failed to parse response"}

    @staticmethod
    def get_category_number(category: Optional[str]) -> int:
        if category == "①":
            return 1
        elif category == "②":
            return 2
        elif category == "③":
            return 3
        elif category == "④":
            return 4
        else:
            return 0  # Unknown category

    @staticmethod
    def get_user_chats_service(db: Session, user_id: int) -> List[ChatRequestSummary]:
        logger.debug(f"Fetching chat requests for user_id: {user_id}")

        chat_requests = db.query(ChatRequest).filter(ChatRequest.user_id == user_id).all()
        chat_requests_summaries = []

        for chat_request in chat_requests:
            logger.debug(f"Processing chat_request_id: {chat_request.id}")

            response = db.query(ChatResponse).filter(ChatResponse.request_id == chat_request.id).first()

            if response:
                logger.debug(f"Found response for chat_request_id: {chat_request.id}")
                response_summary = ChatResponseSummary(
                    final_answer=response.final_answer,
                    created_at=response.created_at
                )
            else:
                logger.debug(f"No response found for chat_request_id: {chat_request.id}")
                response_summary = None

            chat_request_summary = ChatRequestSummary(
                content=chat_request.content,
                created_at=chat_request.created_at,
                response=response_summary
            )

            chat_requests_summaries.append(chat_request_summary)

        return chat_requests_summaries
