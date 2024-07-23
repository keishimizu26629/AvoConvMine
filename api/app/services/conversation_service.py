import json
from schemas.conversation import ConversationInput
from utils.text_processing import clean_json_response
from utils.gemini_api import generate_gemini_response

async def extract_attributes_service(conversation: ConversationInput):
    try:
        prompt = f"""
        Analyze the following text and extract all relevant information about the person mentioned.
        Convert this information into a JSON object. The structure of the JSON should be determined based on the content of the text.
        Include all significant details mentioned, using appropriate key names that best describe each piece of information.

        Text:
        {conversation.content}

        Guidelines:
        - Create a JSON object that accurately represents all the information in the text.
        - Use descriptive and appropriate key names for each piece of information.
        - Include all relevant details, no matter how minor they might seem.
        - The structure of the JSON should be flexible and based on the content of the text.
        - Ensure the output is a valid JSON object without any additional text or formatting.

        Your response should be only the JSON object, with no additional explanation or text.
        """
        response = await generate_gemini_response(prompt)

        cleaned_response = clean_json_response(response.text)

        try:
            attributes_json = json.loads(cleaned_response)
            return {"attributes": attributes_json}
        except json.JSONDecodeError:
            return {"raw_response": cleaned_response}

    except Exception as e:
        return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}
