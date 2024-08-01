import json
import logging
from typing import Dict, Any, Optional
from schemas.chat import InitialChatResponse
from utils.gemini_api import generate_gemini_response
from utils.text_processing import clean_json_response

logger = logging.getLogger(__name__)

class ChatService:
    @staticmethod
    async def process_chat(user_id: int, content: str, db) -> InitialChatResponse:
        analysis = await ChatService.analyze_question(content)

        return InitialChatResponse(
            who=analysis.get("person"),
            what=analysis.get("attribute"),
            question_category=ChatService.get_category_number(analysis.get("category"))
        )
    
    @staticmethod
    async def analyze_question(question: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following question: {question}

        Return a JSON object in the following format:
        {{
            "category": "Question category (①, ②, ③, or ④)",
            "person": "Name of the person if the question is about a specific person, otherwise null",
            "attribute": "The exact phrase or words used in the question to describe the attribute or information being asked about, or 'general description' for category ④ questions",
            "explanation": "Brief explanation of the classification"
        }}

        Category definitions:
        ①: Questions asking to confirm a specific attribute of a specific person
        ②: Questions asking about a specific attribute of a specific person
        ③: Questions asking about a person with a specific attribute
        ④: Questions asking for a general description or overview of a specific person

        Examples of category ④ questions:
        - Can you tell me about [Person]?
        - What is [Person] like?
        - How would you describe [Person]?
        - Can you describe [Person]'s personality?

        Note: For the "attribute" field, use the exact words or phrase from the question that describe what is being asked about, not a general category. For category ④, use 'general description'.

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
