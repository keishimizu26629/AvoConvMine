from pydantic import BaseModel
from typing import Optional, Any, Union

class ChatRequest(BaseModel):
    user_id: int
    content: str

class InitialChatResponse(BaseModel):
    who: Optional[str]
    what: str
    question_category: int

class Category1Response(BaseModel):
    who: str
    what: str
    answer: str
    approximation: Optional[Any]
    similarity_category: str

class Category2Response(BaseModel):
    who: str
    what: str
    answer: Any

class Category3Response(BaseModel):
    what: str
    who: Optional[str]
    answer: Any

class Category4Response(BaseModel):
    who: str
    description: str

class ChatResponse(BaseModel):
    question_category: int
    response: Union[Category1Response, Category2Response, Category3Response, Category4Response]
