from pydantic import BaseModel
from datetime import datetime

class ConversationInput(BaseModel):
    friend_id: int
    context: str
    conversation_date: datetime
