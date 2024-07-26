from pydantic import BaseModel
from datetime import datetime

class FriendBase(BaseModel):
    name: str
    user_id: int

class FriendCreate(FriendBase):
    pass

class FriendUpdate(BaseModel):
    name: str

class FriendInDB(FriendBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
