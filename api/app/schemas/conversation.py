from pydantic import BaseModel

class ConversationInput(BaseModel):
    user_id: int
    friend_id: int
    context: str
