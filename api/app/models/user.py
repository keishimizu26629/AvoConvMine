from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import BaseModel
from datetime import datetime, timezone

class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    firebase_uid = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    friends = relationship("Friend", back_populates="user")
    friend_attributes = relationship("FriendAttribute", back_populates="user")
    conversation_histories = relationship("ConversationHistory", back_populates="user")
