import logging
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.friend import Friend, Attribute, FriendAttribute
from app.utils.embedding import generate_embedding, cosine_similarity_single

logger = logging.getLogger(__name__)

def find_attribute(db: Session, what: str):
    all_attributes = db.query(Attribute).all()
    what_embedding = generate_embedding(what)

    best_attribute = None
    best_similarity = -1

    for attr in all_attributes:
        attr_embedding = generate_embedding(attr.name)
        similarity = cosine_similarity_single(what_embedding, attr_embedding)
        if similarity > best_similarity:
            best_similarity = similarity
            best_attribute = attr

    return best_attribute, best_similarity

def find_friend(db: Session, who: str, user_id: int):
    logger.debug(f"Searching for friend: {who} for user_id: {user_id}")

    friend = db.query(Friend).filter(
        func.lower(Friend.name) == who.lower(),
        Friend.user_id == user_id
    ).first()

    if friend:
        logger.debug(f"Found friend by name: {friend.name} (id: {friend.id}) for user_id: {user_id}")
        return friend

    # Friend.name で見つからなかった場合、Attribute経由で検索
    logger.debug(f"Friend not found by name for user_id: {user_id}, searching through attributes")
    name_attribute = db.query(Attribute).filter(Attribute.id == 29).first()
    if name_attribute:
        friend_with_name = db.query(FriendAttribute).filter(
            FriendAttribute.attribute_id == name_attribute.id,
            func.lower(FriendAttribute.value).like(f"%{who.lower()}%"),
            FriendAttribute.user_id == user_id
        ).first()
        if friend_with_name:
            friend = db.query(Friend).filter(Friend.id == friend_with_name.friend_id, Friend.user_id == user_id).first()
            if friend:
                logger.debug(f"Found friend through attributes: {friend.name} (id: {friend.id}) for user_id: {user_id}")
                return friend

    logger.debug(f"Friend not found: {who} for user_id: {user_id}")
    return None

def get_friend_attribute(db: Session, friend_id: int, attribute_id: int, user_id: int):
    return db.query(FriendAttribute).filter(
        FriendAttribute.friend_id == friend_id,
        FriendAttribute.attribute_id == attribute_id,
        FriendAttribute.user_id == user_id
    ).first()

def get_all_friend_attributes(db: Session, friend_id: int, user_id: int):
    logger.debug(f"Getting attributes for friend_id: {friend_id}, user_id: {user_id}")
    attributes = (
        db.query(FriendAttribute, Attribute.name)
        .join(Attribute, FriendAttribute.attribute_id == Attribute.id)
        .filter(
            and_(
                FriendAttribute.friend_id == friend_id,
                FriendAttribute.user_id == user_id
            )
        )
        .all()
    )

    result = [
        AttributeInfo(name=attr_name, value=friend_attr.value)
        for friend_attr, attr_name in attributes
    ]

    logger.debug(f"Retrieved {len(result)} attributes for friend_id: {friend_id}")
    return result

class AttributeInfo:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

def get_friends_by_attribute(db: Session, user_id: int, attribute_id: int, attribute_value: str):
    """
    指定された属性と値に基づいて友人を検索します。

    :param db: データベースセッション
    :param user_id: ユーザーID
    :param attribute_id: 属性ID
    :param attribute_value: 検索する属性値
    :return: マッチする友人のリスト（各友人の名前と全ての属性を含む）
    """
    matching_friends = (
        db.query(Friend)
        .join(FriendAttribute, Friend.id == FriendAttribute.friend_id)
        .filter(
            and_(
                FriendAttribute.user_id == user_id,
                FriendAttribute.attribute_id == attribute_id,
                FriendAttribute.value.ilike(f"%{attribute_value}%")
            )
        )
        .all()
    )

    result = []
    for friend in matching_friends:
        friend_attributes = get_all_friend_attributes(db, friend.id, user_id)
        result.append({
            "name": friend.name,
            "attributes": friend_attributes
        })

    return result
