import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

async def generate_gemini_response(prompt: str):
    model = genai.GenerativeModel('gemini-pro')
    return model.generate_content(prompt)
