import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models.friend import Friend
from schemas.conversation import ConversationInput
from schemas.friend import FriendCreate, FriendUpdate, FriendInDB, FriendDetailRequest, FriendDetailResponse, UpdateFriendDetailsRequest, UpdateFriendDetailsResponse
from schemas.attribute import AttributeSchema
from services import conversation_service, attribute_service, friend_service
from database import get_db

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FriendController:
    @staticmethod
    async def extract_and_save_attributes(user_id: int, conversation: ConversationInput, db: Session = Depends(get_db)):
        logger.debug(f"Starting extract_and_save_attributes for user_id: {user_id}, friend_id: {conversation.friend_id}")
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
            processed_attributes = await attribute_service.process_attributes(db, user_id, conversation.friend_id, result["attributes"])

            # Save conversation history
            await conversation_service.save_conversation_history(db, user_id, conversation)

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
    def create_friend(friend: FriendCreate, db: Session, user_id: int):
        try:
            return friend_service.create_friend(db, friend, user_id)
        except HTTPException as e:
            # HTTPExceptionをそのまま再発生させる
            raise e
        except Exception as e:
            # その他の例外は500 Internal Server Errorとして処理
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def get_friend(friend_id: int, db: Session = Depends(get_db)):
        db_friend = friend_service.get_friend(db, friend_id)
        if db_friend is None:
            raise HTTPException(status_code=404, detail="Friend not found")
        return db_friend

    @staticmethod
    def get_friends(db: Session, user_id: int):
        return friend_service.get_friends_by_user_id(db, user_id)

    @staticmethod
    def update_friend(friend_id: int, friend: FriendUpdate, db: Session = Depends(get_db)):
        db_friend = friend_service.update_friend(db, friend_id, friend)
        if db_friend is None:
            raise HTTPException(status_code=404, detail="Friend not found")
        return db_friend

    @staticmethod
    def get_friend_details_with_history(db: Session, user_id: int, request: FriendDetailRequest) -> FriendDetailResponse:
        try:
            return friend_service.get_friend_details_with_history(db, user_id, request.friend_id)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def update_friend_details(db: Session, user_id: int, request: UpdateFriendDetailsRequest) -> UpdateFriendDetailsResponse:
        logger.info(f"Updating friend details for user_id: {user_id}, friend_id: {request.friend_id}")
        try:
            result = friend_service.update_friend_details(db, user_id, request.friend_id, request.attributes)
            logger.info("Successfully updated friend details")
            return result
        except HTTPException as e:
            logger.error(f"HTTP exception occurred: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
