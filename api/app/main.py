import os
import json
import re
from fastapi import FastAPI
from routes import user_routes
from database import Engine, BaseModel as SQLAlchemyBaseModel
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

app.include_router(user_routes.router)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# GeminiAPIの設定
genai.configure(api_key=GEMINI_API_KEY)

class ConversationInput(BaseModel):
    content: str

def clean_json_response(response_text: str) -> str:
    # Markdownの装飾を除去
    cleaned = re.sub(r'```json\n?', '', response_text)
    cleaned = re.sub(r'\n?```', '', cleaned)
    # 前後の空白を除去
    return cleaned.strip()

@app.post("/extract_attributes")
async def extract_attributes(conversation: ConversationInput):
    try:
        model = genai.GenerativeModel('gemini-pro')
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
        response = model.generate_content(prompt)

        # レスポンスをクリーニング
        cleaned_response = clean_json_response(response.text)

        # クリーニングされたレスポンスをJSONとしてパース
        try:
            attributes_json = json.loads(cleaned_response)
            return {"attributes": attributes_json}
        except json.JSONDecodeError:
            # JSONとしてパースできない場合は、クリーニングされた原文を返す
            return {"raw_response": cleaned_response}

    except Exception as e:
        # その他のエラーが発生した場合
        return {"error": str(e), "raw_response": response.text if 'response' in locals() else None}

@app.on_event("startup")
async def startup():
    SQLAlchemyBaseModel.metadata.create_all(bind=Engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
