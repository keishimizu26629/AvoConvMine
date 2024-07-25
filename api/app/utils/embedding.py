import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # より適切なモデルに変更可能

def generate_embedding(text: str) -> list:
    return model.encode(text).tolist()

def cosine_similarity(vec1: list, vec2: list) -> float:
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
