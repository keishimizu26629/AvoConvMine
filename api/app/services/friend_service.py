import numpy as np
from typing import List
from fastapi import HTTPException
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from app.utils.embedding import generate_embedding
from app.models.friend import Friend, FriendAttribute, Attribute
from app.models.conversation_history import ConversationHistory
from app.schemas.friend import FriendCreate, FriendUpdate, FriendDetailResponse, FriendAttributeResponse, ConversationHistoryItem

import logging
import json
from utils.embedding import generate_embedding, cosine_similarity

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def save_friend_attributes(db: Session, user_id: int, friend_id: int, processed_attributes: dict):
    try:
        for key, value in processed_attributes.items():
            try:
                attribute = db.query(Attribute).filter(Attribute.name == key).first()
                if not attribute:
                    logger.warning(f"Attribute {key} not found in the database")
                    continue

                friend_attr = db.query(FriendAttribute).filter(
                    FriendAttribute.user_id == user_id,
                    FriendAttribute.friend_id == friend_id,
                    FriendAttribute.attribute_id == attribute.id
                ).first()

                if friend_attr:
                    friend_attr.value = value
                else:
                    friend_attr = FriendAttribute(user_id=user_id, friend_id=friend_id, attribute_id=attribute.id, value=value)
                    db.add(friend_attr)
            except Exception as e:
                logger.exception(f"Error processing attribute {key}: {str(e)}")

        db.commit()
        return {"message": "Friend attributes saved successfully"}
    except Exception as e:
        db.rollback()
        logger.exception(f"Error saving friend attributes: {str(e)}")
        raise

async def get_all_attributes(db: Session):
    return db.query(Attribute).all()

async def find_similar_attributes(db: Session, query: str, threshold: float = 0.7) -> List[dict]:
    logger.debug(f"Searching for attributes similar to: {query}")
    query_embedding = generate_embedding(query)
    logger.debug(f"Query embedding: {query_embedding[:5]}...")  # 最初の5要素のみ表示

    similar_attributes = []
    all_attributes = db.query(Attribute).all()
    logger.debug(f"Total attributes in database: {len(all_attributes)}")

    # 全ての属性名のembeddingを一度に生成し、2D配列に変換
    attribute_names = [attr.name for attr in all_attributes]
    attribute_embeddings = np.array([generate_embedding(name) for name in attribute_names])

    # query_embeddingを2D配列に変換
    query_embedding_2d = np.array(query_embedding).reshape(1, -1)

    # 全ての属性embeddingとクエリembeddingの類似度を一度に計算
    similarities = cosine_similarity(query_embedding_2d, attribute_embeddings)[0]

    for attr, similarity in zip(all_attributes, similarities):
        logger.debug(f"Attribute: {attr.name}, Similarity: {similarity}")
        if similarity >= threshold:
            similar_attributes.append({
                "id": attr.id,
                "name": attr.name,
                "similarity": float(similarity)  # numpyのfloat32をPythonのfloatに変換
            })

    logger.debug(f"Found {len(similar_attributes)} similar attributes")
    return similar_attributes

def create_friend(db: Session, friend: FriendCreate, user_id: int):
    # 同じユーザーIDで同じ名前のフレンドが既に存在するかチェック
    existing_friend = db.query(Friend).filter(
        Friend.user_id == user_id,
        Friend.name == friend.name
    ).first()

    if existing_friend:
        raise HTTPException(status_code=400, detail="A friend with this name already exists for this user")

    # 新しいフレンドを作成
    db_friend = Friend(name=friend.name, user_id=user_id)
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend

def get_friend(db: Session, friend_id: int):
    return db.query(Friend).filter(Friend.id == friend_id).first()

def get_friends(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Friend).offset(skip).limit(limit).all()

def get_friends_by_user_id(db: Session, user_id: int, skip: int = 0, limit: int = 500):
    return db.query(Friend).filter(Friend.user_id == user_id).offset(skip).limit(limit).all()

def update_friend(db: Session, friend_id: int, friend: FriendUpdate):
    db_friend = db.query(Friend).filter(Friend.id == friend_id).first()
    if db_friend:
        for key, value in friend.dict().items():
            setattr(db_friend, key, value)
        db.commit()
        db.refresh(db_friend)
    return db_friend

def delete_friend(db: Session, friend_id: int):
    db_friend = db.query(Friend).filter(Friend.id == friend_id).first()
    if db_friend:
        db.delete(db_friend)
        db.commit()
    return db_friend

def get_friend_details_with_history(db: Session, user_id: int, friend_id: int) -> FriendDetailResponse:
    friend = db.query(Friend).filter(Friend.id == friend_id, Friend.user_id == user_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    attributes = db.query(Attribute.name, FriendAttribute.value)\
        .join(FriendAttribute, Attribute.id == FriendAttribute.attribute_id)\
        .filter(FriendAttribute.friend_id == friend_id, FriendAttribute.user_id == user_id)\
        .all()

    conversations = db.query(ConversationHistory.context, ConversationHistory.conversation_date)\
        .filter(ConversationHistory.user_id == user_id, ConversationHistory.friend_id == friend_id)\
        .order_by(ConversationHistory.conversation_date.desc())\
        .all()

    return FriendDetailResponse(
        friend_name=friend.name,
        attributes=[
            FriendAttributeResponse(attribute_name=name, value=value)
            for name, value in attributes
        ],
        conversations=[
            ConversationHistoryItem(context=context, conversation_date=conversation_date)
            for context, conversation_date in conversations
        ]
    )
