import re

def clean_json_response(response_text: str) -> str:
    cleaned = re.sub(r'```json\n?', '', response_text)
    cleaned = re.sub(r'\n?```', '', cleaned)
    return cleaned.strip()
