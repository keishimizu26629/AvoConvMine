from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import BaseModel

class ConversationHistory(BaseModel):
    __tablename__ = "conversation_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    friend_id = Column(Integer, ForeignKey("friends.id"), index=True)
    conversation_date = Column(DateTime, default=datetime.now(timezone.utc))
    context = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="conversation_histories")
    friend = relationship("Friend", back_populates="conversation_histories")
