from pydantic import BaseModel

class ConversationInput(BaseModel):
    content: str
