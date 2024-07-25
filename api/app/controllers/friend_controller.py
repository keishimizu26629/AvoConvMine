from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.friend import Friend
from schemas.conversation import ConversationInput
from schemas.friend import AttributeSchema
from services import conversation_service, attribute_service, friend_service
from database import get_db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FriendController:
    @staticmethod
    async def extract_and_save_attributes(friend_id: int, conversation: ConversationInput, db: Session = Depends(get_db)):
        logger.debug(f"Starting extract_and_save_attributes for friend_id: {friend_id}")
        try:
            # Extract attributes from conversation
            logger.debug("Extracting attributes from conversation")
            result = await conversation_service.extract_attributes_service(conversation)
            if "error" in result:
                logger.error(f"Error in extract_attributes_service: {result['error']}")
                raise HTTPException(status_code=400, detail=result["error"])

            # Process attributes and check for similarities
            logger.debug("Processing attributes")
            processed_attributes = await attribute_service.process_attributes(db, result["attributes"])

            # Save processed attributes to friend
            logger.debug("Saving processed attributes")
            save_result = await friend_service.save_friend_attributes(db, friend_id, processed_attributes)

            logger.debug("Attributes extracted and saved successfully")
            return {"message": "Attributes extracted and saved successfully", "attributes": processed_attributes}
        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")
            raise

    @staticmethod
    def get_friends(skip: int, limit: int, db: Session):
        return friend_service.get_friends(db, skip, limit)

    @staticmethod
    async def get_all_attributes(db: Session = Depends(get_db)):
        attributes = await friend_service.get_all_attributes(db)
        return [AttributeSchema.from_orm(attr) for attr in attributes]

    @staticmethod
    async def find_similar_attributes(query: str, db: Session = Depends(get_db)):
        similar_attributes = await friend_service.find_similar_attributes(db, query)
        return similar_attributes

    @staticmethod
    async def calculate_similarities(query: str, db: Session = Depends(get_db)):
        return await friend_service.calculate_similarities(db, query)
