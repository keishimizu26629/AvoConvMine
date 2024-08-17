import re
from utils.constants import ATTRIBUTE_PREFIXES_TO_REMOVE

def clean_json_response(response_text: str) -> str:
    cleaned = re.sub(r'```json\n?', '', response_text)
    cleaned = re.sub(r'\n?```', '', cleaned)
    return cleaned.strip()

def clean_attribute_name(name: str) -> str:
    # 大文字小文字を区別せずにプレフィックスを削除
    pattern = '|'.join(map(re.escape, ATTRIBUTE_PREFIXES_TO_REMOVE))
    cleaned_name = re.sub(f'^({pattern})', '', name, flags=re.IGNORECASE)

    # スペースで区切られた各単語の先頭を大文字に
    return ' '.join(word.capitalize() for word in cleaned_name.split())
