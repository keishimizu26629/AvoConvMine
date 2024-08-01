from sqlalchemy.orm import Session
from models.friend import Attribute
from models.friend import FriendAttribute
from utils.text_processing import clean_attribute_name
from utils.json_utils import flatten_json
from utils.embedding import generate_embedding, cosine_similarity
from utils.text_processing import clean_attribute_name
import json

async def process_attributes(db: Session, user_id: int, friend_id: int, attributes: dict):
    flattened_attributes = flatten_json(attributes)
    processed_attributes = {}

    for key, value in flattened_attributes.items():
        cleaned_key = clean_attribute_name(key)

        # Attributeの検索または作成
        attribute = await find_or_create_attribute(db, cleaned_key)

        # Embeddingの生成
        embedding = generate_embedding(f"{cleaned_key}: {value}")

        # FriendAttributeの作成または更新
        friend_attr = db.query(FriendAttribute).filter(
            FriendAttribute.user_id == user_id,
            FriendAttribute.friend_id == friend_id,
            FriendAttribute.attribute_id == attribute.id
        ).first()

        if friend_attr:
            friend_attr.value = str(value)
            friend_attr.embedding = json.dumps(embedding)
        else:
            friend_attr = FriendAttribute(
                user_id=user_id,
                friend_id=friend_id,
                attribute_id=attribute.id,
                value=str(value),
                embedding=json.dumps(embedding)
            )
            db.add(friend_attr)

        processed_attributes[cleaned_key] = value

    db.commit()
    return processed_attributes

async def find_or_create_attribute(db: Session, attribute_name: str):
    attribute = db.query(Attribute).filter(Attribute.name == attribute_name).first()
    if not attribute:
        attribute = Attribute(name=attribute_name)
        db.add(attribute)
        db.flush()
        db.refresh(attribute)
    return attribute

async def find_similar_attributes(db: Session, query: str, threshold: float = 0.7):
    query_embedding = generate_embedding(query)

    similar_attributes = []
    all_attributes = await db.query(Attribute).all()

    for attr in all_attributes:
        attr_embedding = generate_embedding(attr.name)
        similarity = cosine_similarity(query_embedding, attr_embedding)
        if similarity >= threshold:
            similar_attributes.append({
                "id": attr.id,
                "name": attr.name,
                "similarity": similarity
            })

    return similar_attributes
