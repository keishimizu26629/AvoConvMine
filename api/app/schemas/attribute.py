from pydantic import BaseModel
from datetime import datetime

class AttributeSchema(BaseModel):
    id: int
    name: str
    embedding: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
