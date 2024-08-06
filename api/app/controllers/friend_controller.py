from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.friend import Friend
from schemas.conversation import ConversationInput
from schemas.friend import FriendCreate, FriendUpdate, FriendInDB
from schemas.attribute import AttributeSchema
from services import conversation_service, attribute_service, friend_service
from database import get_db
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FriendController:
    @staticmethod
    async def extract_and_save_attributes(conversation: ConversationInput, db: Session = Depends(get_db)):
        logger.debug(f"Starting extract_and_save_attributes for user_id: {conversation.user_id}, friend_id: {conversation.friend_id}")
        try:
            # Extract attributes from conversation
            logger.debug("Extracting attributes from conversation")
            result = await conversation_service.extract_attributes_service(conversation)
            logger.debug(f"Extracted result: {result}")
            if "error" in result:
                logger.error(f"Error in extract_attributes_service: {result['error']}")
                raise HTTPException(status_code=400, detail=result["error"])

            if "attributes" not in result:
                logger.error(f"No 'attributes' key in result: {result}")
                raise HTTPException(status_code=500, detail="Unexpected response format from attribute extraction")

            # Process attributes and save them
            logger.debug("Processing and saving attributes")
            processed_attributes = await attribute_service.process_attributes(db, conversation.user_id, conversation.friend_id, result["attributes"])

            # Save conversation history
            await conversation_service.save_conversation_history(db, conversation)

            logger.debug("Attributes extracted and saved successfully")
            return {
                "message": "Attributes extracted and saved successfully",
                "attributes": processed_attributes,
                "updated_count": len([attr for attr in processed_attributes if attr not in result["attributes"]])
            }
        except KeyError as ke:
            logger.exception(f"KeyError occurred: {str(ke)}")
            raise HTTPException(status_code=500, detail=f"Missing key in result: {str(ke)}")
        except Exception as e:
            logger.exception(f"An error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def get_all_attributes(db: Session = Depends(get_db)):
        attributes = await friend_service.get_all_attributes(db)
        return [AttributeSchema.from_orm(attr) for attr in attributes]

    @staticmethod
    async def find_similar_attributes(query: str, db: Session = Depends(get_db)):
        similar_attributes = await friend_service.find_similar_attributes(db, query)
        if not similar_attributes:
            return {"message": "No similar attributes found"}
        return {"similar_attributes": similar_attributes}

    @staticmethod
    def create_friend(friend: FriendCreate, db: Session = Depends(get_db)):
        return friend_service.create_friend(db, friend)

    @staticmethod
    def get_friend(friend_id: int, db: Session = Depends(get_db)):
        db_friend = friend_service.get_friend(db, friend_id)
        if db_friend is None:
            raise HTTPException(status_code=404, detail="Friend not found")
        return db_friend

    @staticmethod
    def get_friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return friend_service.get_friends(db, skip=skip, limit=limit)

    @staticmethod
    def update_friend(friend_id: int, friend: FriendUpdate, db: Session = Depends(get_db)):
        db_friend = friend_service.update_friend(db, friend_id, friend)
        if db_friend is None:
            raise HTTPException(status_code=404, detail="Friend not found")
        return db_friend
