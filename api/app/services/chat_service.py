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
        Analyze the following question in English: {question}

        Return a JSON object in the following format:
        {{
            "category": "Question category (①, ②, ③, or ④)",
            "person": "Name of the person if the question is about a specific person, otherwise null",
            "attribute": "The exact phrase or words used in the question to describe the attribute or information being asked about, or 'general description' for category ④ questions",
            "explanation": "Brief explanation of the classification"
        }}

        Category definitions with examples:
        ①: Questions asking to confirm or inquire about a specific attribute of a specific person
        Pattern: "Is/Are/Does/Do [Person] [Attribute]?" or similar confirmatory or inquiry questions
        Examples:
        - Is John an engineer?
        - Are Mary and Tom married?
        - Was Sarah born in New York?
        - Does Karen run a florist in Tokyo?
        - Do the Smiths live in California?

        ②: Questions asking about a specific attribute of a specific person, typically starting with "What", "Where", "When", "How"
        Pattern: "What/Where/When/How is/was [Person]'s [Attribute]?" or similar specific inquiries
        Examples:
        - What is David's occupation?
        - Where does Emma live?
        - How old is Michael?
        - When did Lisa graduate?

        ③: Questions asking about a person with a specific attribute
        Pattern: "Who is/are the [Attribute]?" or similar questions identifying people by attributes
        Examples:
        - Who is the tallest person in the group?
        - Which employee has the most experience?
        - Who are the new team members?

        ④: Questions asking for a general description or overview of a specific person
        Pattern: Open-ended questions about a person without specifying an attribute
        Examples:
        - Can you tell me about Lisa?
        - What do you know about Dr. Johnson?
        - How would you describe Alex?

        Important:
        - Pay close attention to the structure and intent of the question.
        - For category ①, the question must be seeking confirmation or inquiry about a specific attribute, often using "Is", "Are", "Does", "Do", etc.
        - For category ②, the question must be asking about a specific attribute of a named person, typically starting with "What", "Where", "When", "How", etc.
        - For category ③, the question must be asking to identify a person or people based on an attribute.
        - For category ④, the question must be open-ended and seeking general information about a person.

        Note: For the "attribute" field, use the exact words or phrase from the question that describe what is being asked about. For category ④, use 'general description'.

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
