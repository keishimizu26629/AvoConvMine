from pydantic import BaseModel
from typing import Optional, Any, Union, Dict, List

class ChatRequest(BaseModel):
    user_id: int
    content: str

class Category1Response(BaseModel):
    who: Optional[str]
    what: str
    related_subject: Optional[str]
    status: str
    answer: Union[str, Dict[str, Any], None]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class Category2Response(BaseModel):
    who: Optional[str]
    what: str
    related_subject: Optional[str]
    status: str
    answer: Optional[str]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class Category3Response(BaseModel):
    who: Optional[str]
    what: str
    related_subject: Optional[str]
    status: str
    answer: Optional[List[Dict[str, Any]]]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class Category4Response(BaseModel):
    who: Optional[str]
    what: Optional[str] = "general description"
    related_subject: Optional[str]
    status: str
    answer: Optional[str]
    summary: Optional[str]
    missing_info: Optional[str]
    approximation: Optional[Any]
    similarity_category: str
    final_answer: Optional[str]

class ChatResponse(BaseModel):
    question_category: int
    response: Union[Category1Response, Category2Response, Category3Response, Category4Response]

class InitialChatResponse(BaseModel):
    who: Optional[str] = None
    what: Optional[str] = None
    related_subject: Optional[str] = None
    question_category: int
