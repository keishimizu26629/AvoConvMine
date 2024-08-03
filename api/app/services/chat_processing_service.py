import logging
from typing import Tuple, Dict, Any
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.friend import Friend, Attribute, FriendAttribute
from utils.embedding import generate_embedding, cosine_similarity_single

logger = logging.getLogger(__name__)

class ChatProcessingService:
    @staticmethod
    async def process_category_1(db: Session, user_id: int, who: str, what: str) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 1 for user_id: {user_id}, who: {who}, what: {what}")

        # ①Attribute.nameをEmbeddingした配列を取得
        attributes = db.query(Attribute).all()
        logger.debug(f"Found {len(attributes)} attributes")
        attribute_embeddings = [generate_embedding(attr.name) for attr in attributes]

        # "what"をEmbeddingした値でコサイン類似度を求める
        what_embedding = generate_embedding(what)
        logger.debug(f"Generated embedding for '{what}'")

        similarities = [cosine_similarity_single(what_embedding, attr_embedding) for attr_embedding in attribute_embeddings]
        max_similarity = max(similarities)
        max_index = similarities.index(max_similarity)
        logger.debug(f"Max similarity: {max_similarity}, Index: {max_index}")

        attribute = attributes[max_index]
        logger.debug(f"Selected attribute: {attribute.name}")

        # ②"who"の値をFriend.nameで調べる（大文字小文字を区別しない）
        friend = db.query(Friend).filter(func.lower(Friend.name) == who.lower()).first()
        if not friend:
            logger.debug(f"Friend not found with name: {who}")
            # ③"who"の値をFriend.nameで調べて該当しない場合（大文字小文字を区別しない）
            name_attribute = db.query(Attribute).filter(Attribute.id == 29).first()
            if name_attribute:
                friend_with_name = db.query(FriendAttribute).filter(
                    FriendAttribute.attribute_id == name_attribute.id,
                    func.lower(FriendAttribute.value).like(f"%{who.lower()}%")
                ).first()
                if friend_with_name:
                    friend = db.query(Friend).filter(Friend.id == friend_with_name.friend_id).first()
                    logger.debug(f"Found friend through name attribute: {friend.name if friend else 'Not found'}")

        if not friend:
            logger.debug("Friend not found, returning 'No' with low confidence")
            return {"answer": "No", "approximation": "Friend not found"}, "low"

        logger.debug(f"Found friend: {friend.name}")

        # 該当するFriendAttributeを取得
        friend_attribute = db.query(FriendAttribute).filter(
            FriendAttribute.friend_id == friend.id,
            FriendAttribute.attribute_id == attribute.id,
            FriendAttribute.user_id == user_id
        ).first()

        if not friend_attribute:
            logger.debug(f"Attribute not found for friend {friend.name}")
            return {"answer": "No", "approximation": "Attribute not found"}, "low"

        logger.debug(f"Found friend attribute: {friend_attribute.value}")

        # ④該当するFriendAttibute.valueをEmbeddingした値でコサイン類似度を求める
        value_embedding = generate_embedding(friend_attribute.value)
        similarity = cosine_similarity_single(what_embedding, value_embedding)
        logger.debug(f"Similarity between '{what}' and '{friend_attribute.value}': {similarity}")

        # ⑤類似度に基づいて回答を生成
        if similarity >= 0.8:
            logger.debug("High similarity, returning 'Yes'")
            return {"status": "Yes", "answer": None, "approximation": None}, "high"
        elif similarity >= 0.5:
            logger.debug("Medium similarity, returning 'No' with approximation")
            return {"status": "No", "answer": None, "approximation": {"attribute": attribute.name, "value": friend_attribute.value}}, "medium"
        else:
            logger.debug("Low similarity, returning 'No'")
            return {"status": "No", "answer": None, "approximation": None}, "low"

    @staticmethod
    async def process_category_2(db: Session, user_id: int, who: str, what: str) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 2 for user_id: {user_id}, who: {who}, what: {what}")

        # ①Attribute.nameをEmbeddingした配列を取得
        attributes = db.query(Attribute).all()
        logger.debug(f"Found {len(attributes)} attributes")
        attribute_embeddings = [generate_embedding(attr.name) for attr in attributes]

        # "what"をEmbeddingした値でコサイン類似度を求める
        what_embedding = generate_embedding(what)
        logger.debug(f"Generated embedding for '{what}'")

        similarities = [cosine_similarity_single(what_embedding, attr_embedding) for attr_embedding in attribute_embeddings]
        max_similarity = max(similarities)
        max_index = similarities.index(max_similarity)
        logger.debug(f"Max similarity: {max_similarity}, Index: {max_index}")

        attribute = attributes[max_index]
        logger.debug(f"Selected attribute: {attribute.name}")

        # ②"who"の値をFriend.nameで調べる（大文字小文字を区別しない）
        friend = db.query(Friend).filter(func.lower(Friend.name) == who.lower()).first()
        if not friend:
            logger.debug(f"Friend not found with name: {who}")
            # ③"who"の値をFriend.nameで調べて該当しない場合（大文字小文字を区別しない）
            name_attribute = db.query(Attribute).filter(Attribute.id == 29).first()
            if name_attribute:
                friend_with_name = db.query(FriendAttribute).filter(
                    FriendAttribute.attribute_id == name_attribute.id,
                    func.lower(FriendAttribute.value).like(f"%{who.lower()}%")
                ).first()
                if friend_with_name:
                    friend = db.query(Friend).filter(Friend.id == friend_with_name.friend_id).first()
                    logger.debug(f"Found friend through name attribute: {friend.name if friend else 'Not found'}")

        if not friend:
            logger.debug("Friend not found, returning 'No' with low confidence")
            return {"status": "No", "answer": None, "approximation": "Friend not found"}, "low"

        logger.debug(f"Found friend: {friend.name}")

        # 該当するFriendAttributeを取得
        friend_attribute = db.query(FriendAttribute).filter(
            FriendAttribute.friend_id == friend.id,
            FriendAttribute.attribute_id == attribute.id,
            FriendAttribute.user_id == user_id
        ).first()

        if not friend_attribute:
            logger.debug(f"Attribute not found for friend {friend.name}")
            return {"status": "No", "answer": None, "approximation": "Attribute not found"}, "low"

        logger.debug(f"Found friend attribute: {friend_attribute.value}")

        # 該当するFriendAttibute.valueをEmbeddingした値でコサイン類似度を求める
        value_embedding = generate_embedding(friend_attribute.value)
        similarity = cosine_similarity_single(what_embedding, value_embedding)
        logger.debug(f"Similarity between '{what}' and '{friend_attribute.value}': {similarity}")

        # 類似度に基づいて回答を生成
        if similarity >= 0.8:
            logger.debug("High similarity, returning 'Yes' with answer")
            return {"status": "Yes", "answer": friend_attribute.value, "approximation": None}, "high"
        elif similarity >= 0.5:
            logger.debug("Medium similarity, returning 'No' with approximation")
            return {"status": "No", "answer": None, "approximation": {"attribute": attribute.name, "value": friend_attribute.value}}, "medium"
        else:
            logger.debug("Low similarity, returning 'No'")
            return {"status": "No", "answer": None, "approximation": "No"}, "low"
