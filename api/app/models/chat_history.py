from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from database import BaseModel
from datetime import datetime, timezone

class ChatRequest(BaseModel):
    __tablename__ = "chat_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    response = relationship("ChatResponse", back_populates="request", uselist=False)


class ChatResponse(BaseModel):
    __tablename__ = "chat_responses"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("chat_requests.id"), unique=True)
    question_category = Column(Integer)
    who = Column(String, index=True)
    what = Column(String, index=True)
    related_subject = Column(String, nullable=True)
    status = Column(String)
    answer = Column(Text)
    approximation_attribute = Column(String)
    approximation_value = Column(String)
    similarity_category = Column(String)
    final_answer = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    request = relationship("ChatRequest", back_populates="response")
