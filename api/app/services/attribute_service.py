from sqlalchemy.orm import Session
from models.friend import Attribute
from utils.embedding import generate_embedding, cosine_similarity
import json

SIMILARITY_THRESHOLD = 0.8

def flatten_json(data, prefix=''):
    items = []
    for key, value in data.items():
        new_key = f"{prefix}{key}".replace('_', ' ')
        if isinstance(value, dict):
            items.extend(flatten_json(value, f"{new_key} ").items())
        elif isinstance(value, list):
            items.append((new_key, ' '.join(map(str, value))))
        else:
            items.append((new_key, str(value)))
    return dict(items)

async def process_attributes(db: Session, attributes_json):
    flattened_attributes = flatten_json(attributes_json)
    processed_attributes = {}

    for key, value in flattened_attributes.items():
        attribute_text = f"{key}: {value}"
        new_embedding = generate_embedding(attribute_text)

        similar_attribute = None
        max_similarity = 0

        for existing_attr in db.query(Attribute).all():
            existing_embedding = json.loads(existing_attr.embedding)
            similarity = cosine_similarity(new_embedding, existing_embedding)
            if similarity > max_similarity and similarity >= SIMILARITY_THRESHOLD:
                max_similarity = similarity
                similar_attribute = existing_attr

        if similar_attribute:
            processed_attributes[similar_attribute.name] = value
        else:
            new_attribute = Attribute(name=key, embedding=json.dumps(new_embedding))
            db.add(new_attribute)
            db.flush()
            processed_attributes[key] = value

    db.commit()
    return processed_attributes
