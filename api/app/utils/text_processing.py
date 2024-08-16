import re
from app.config.settings import settings

def clean_json_response(response_text: str) -> str:
    cleaned = re.sub(r'```json\n?', '', response_text)
    cleaned = re.sub(r'\n?```', '', cleaned)
    return cleaned.strip()

def clean_attribute_name(name: str) -> str:
    # 設定ファイルから除外するプレフィックスを取得
    prefixes_to_remove = settings.ATTRIBUTE_PREFIXES_TO_REMOVE

    # 大文字小文字を区別せずにプレフィックスを削除
    pattern = '|'.join(map(re.escape, prefixes_to_remove))
    cleaned_name = re.sub(f'^({pattern})', '', name, flags=re.IGNORECASE)

    # スペースで区切られた各単語の先頭を大文字に
    return ' '.join(word.capitalize() for word in cleaned_name.split())
