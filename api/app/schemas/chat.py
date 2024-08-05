from pydantic import BaseModel
from typing import Optional, Any, Union

class ChatRequest(BaseModel):
    user_id: int
    content: str

class Category1Response(BaseModel):
    who: Optional[str]
    what: str
    status: str
    answer: Optional[str]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class Category2Response(BaseModel):
    who: Optional[str]
    what: str
    status: str
    answer: Optional[str]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class Category3Response(BaseModel):
    what: str
    who: Optional[str]
    status: str
    answer: Optional[str]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class ChatResponse(BaseModel):
    question_category: int
    response: Union[Category1Response, Category2Response, Category3Response]

class InitialChatResponse(BaseModel):
    who: Optional[str]
    what: Optional[str]
    question_category: int
