from sqlalchemy.orm import Session
from models.friend import Friend, FriendAttribute, Attribute
import logging
import json
from utils.embedding import generate_embedding, cosine_similarity

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def save_friend_attributes(db: Session, friend_id: int, processed_attributes: dict):
    try:
        for key, value in processed_attributes.items():
            try:
                attribute = db.query(Attribute).filter(Attribute.name == key).first()
                if not attribute:
                    logger.warning(f"Attribute {key} not found in the database")
                    continue

                friend_attr = db.query(FriendAttribute).filter(
                    FriendAttribute.friend_id == friend_id,
                    FriendAttribute.attribute_id == attribute.id
                ).first()

                if friend_attr:
                    friend_attr.value = value
                else:
                    friend_attr = FriendAttribute(friend_id=friend_id, attribute_id=attribute.id, value=value)
                    db.add(friend_attr)
            except Exception as e:
                logger.exception(f"Error processing attribute {key}: {str(e)}")

        db.commit()
        return {"message": "Friend attributes saved successfully"}
    except Exception as e:
        db.rollback()
        logger.exception(f"Error saving friend attributes: {str(e)}")
        raise

def get_friends(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Friend).offset(skip).limit(limit).all()

async def get_all_attributes(db: Session):
    return db.query(Attribute).all()

async def find_similar_attributes(db: Session, query: str, threshold: float = 0.8):
    query_embedding = generate_embedding(query)

    similar_attributes = []
    all_attributes = db.query(Attribute).all()

    for attr in all_attributes:
        attr_embedding = json.loads(attr.embedding)
        similarity = cosine_similarity(query_embedding, attr_embedding)
        if similarity >= threshold:
            similar_attributes.append({
                "id": attr.id,
                "name": attr.name,
                "similarity": similarity
            })

    return similar_attributes

async def calculate_similarities(db: Session, query: str):
    query_embedding = generate_embedding(query)

    similarities = []
    all_attributes = db.query(Attribute).all()

    for attr in all_attributes:
        attr_embedding = json.loads(attr.embedding)
        similarity = cosine_similarity(query_embedding, attr_embedding)
        similarities.append({
            "id": attr.id,
            "name": attr.name,
            "similarity": similarity
        })

    return similarities
