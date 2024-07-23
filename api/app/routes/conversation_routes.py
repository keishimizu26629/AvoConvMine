from fastapi import APIRouter, Depends
from schemas.conversation import ConversationInput
from services.conversation_service import extract_attributes_service

router = APIRouter()

@router.post("/extract_attributes")
async def extract_attributes(conversation: ConversationInput):
    return await extract_attributes_service(conversation)
