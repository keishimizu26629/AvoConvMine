from sqlalchemy.orm import Session
from app.models.friend import Friend, FriendAttribute, Attribute

def get_all_friends_attributes(db: Session, user_id: int):
    friends_attributes = db.query(Friend, FriendAttribute, Attribute)\
        .join(FriendAttribute, Friend.id == FriendAttribute.friend_id)\
        .join(Attribute, FriendAttribute.attribute_id == Attribute.id)\
        .filter(FriendAttribute.user_id == user_id)\
        .all()

    result = {}
    for friend, friend_attr, attr in friends_attributes:
        if friend.id not in result:
            result[friend.id] = []
        result[friend.id].append(attr)

    return result
