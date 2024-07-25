from pydantic import BaseModel
from datetime import datetime

class FriendBase(BaseModel):
    user_id: int
    name: str

class FriendCreate(FriendBase):
    pass

class FriendInDB(FriendBase):
    id: int

    class Config:
        orm_mode = True

class AttributeSchema(BaseModel):
    id: int
    name: str
    embedding: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
