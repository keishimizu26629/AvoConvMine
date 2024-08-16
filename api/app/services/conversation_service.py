import json
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from schemas.conversation import ConversationInput
from models.conversation_history import ConversationHistory
from utils.text_processing import clean_json_response
from utils.gemini_api import generate_gemini_response
from utils.attribute_keywords import UPDATE_KEYWORDS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def extract_attributes_service(conversation: ConversationInput):
    try:
        prompt = f"""
        Analyze the following text and extract all relevant information about the person mentioned.
        Convert this information into a JSON object. The structure of the JSON should be flat, with keys using underscores to represent hierarchy.
        Include all significant details mentioned, using appropriate key names that best describe each piece of information.

        Text:
        {conversation.context}

        Guidelines:
        - Create a flat JSON object that accurately represents all the information in the text.
        - Use descriptive and appropriate key names for each piece of information.
        - Use underscores to represent hierarchy in keys (e.g., "Family_Children_Count" instead of nested objects).
        - Include all relevant details, no matter how minor they might seem.
        - Ensure the output is a valid JSON object without any additional text or formatting.

        Your response should be only the JSON object, with no additional explanation or text.
        """
        response = await generate_gemini_response(prompt)

        cleaned_response = clean_json_response(response.text)

        try:
            attributes_json = json.loads(cleaned_response)
            return {"attributes": attributes_json}
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON: {cleaned_response}")
            return {"error": "Failed to parse response", "raw_response": cleaned_response}

    except Exception as e:
        logger.exception(f"Error in extract_attributes_service: {str(e)}")
        return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}

async def save_conversation_history(db: Session, user_id: int, conversation: ConversationInput):
    new_history = ConversationHistory(
        user_id=user_id,
        friend_id=conversation.friend_id,
        conversation_date=conversation.conversation_date,
        context=conversation.context
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history
