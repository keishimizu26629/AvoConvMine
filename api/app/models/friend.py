from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date, JSON, Boolean
from sqlalchemy.orm import relationship
from database import BaseModel
from datetime import datetime, timezone

class Friend(BaseModel):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="friends")
    friend_attributes = relationship("FriendAttribute", back_populates="friend")
    conversation_histories = relationship("ConversationHistory", back_populates="friend")

class Attribute(BaseModel):
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    friend_attributes = relationship("FriendAttribute", back_populates="attribute")

class FriendAttribute(BaseModel):
    __tablename__ = "friend_attributes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    friend_id = Column(Integer, ForeignKey("friends.id"))
    attribute_id = Column(Integer, ForeignKey("attributes.id"))
    value = Column(String)
    embedding = Column(Text)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    user = relationship("User", back_populates="friend_attributes")
    friend = relationship("Friend", back_populates="friend_attributes")
    attribute = relationship("Attribute", back_populates="friend_attributes")
