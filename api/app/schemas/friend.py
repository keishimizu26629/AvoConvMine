from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FriendBase(BaseModel):
    name: str
    user_id: int

class FriendCreate(BaseModel):
    name: str
    user_id: Optional[int] = None

class FriendUpdate(BaseModel):
    name: str

class FriendInDB(FriendBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class FriendAttributeResponse(BaseModel):
    attribute_name: str
    value: str

class FriendDetailRequest(BaseModel):
    friend_id: int

class ConversationHistoryItem(BaseModel):
    context: str
    conversation_date: datetime

class FriendDetailResponse(BaseModel):
    friend_name: str
    attributes: List[FriendAttributeResponse]
    conversations: List[ConversationHistoryItem]

class FriendAttributeUpdate(BaseModel):
    attribute_name: str
    value: str

class UpdateFriendDetailsRequest(BaseModel):
    friend_id: int
    attributes: List[FriendAttributeUpdate]

class UpdateFriendDetailsResponse(BaseModel):
    friend_name: str
    attributes: List[FriendAttributeUpdate]
