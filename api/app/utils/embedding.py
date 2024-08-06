import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Union, Tuple

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
    return model.encode(text).tolist()

def cosine_similarity(vec1: Union[List[float], np.ndarray], vec2: Union[List[float], np.ndarray]) -> Union[float, np.ndarray]:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    if vec1.ndim == 1:
        vec1 = vec1.reshape(1, -1)
    if vec2.ndim == 1:
        vec2 = vec2.reshape(1, -1)
    return np.dot(vec1, vec2.T) / (np.linalg.norm(vec1, axis=1).reshape(-1, 1) * np.linalg.norm(vec2, axis=1))

def cosine_similarity_single(vec1: Union[List[float], np.ndarray], vec2: Union[List[float], np.ndarray]) -> float:
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_best_match(query: str, candidates: List[str]) -> Tuple[str, float]:
    query_embedding = generate_embedding(query)
    candidate_embeddings = generate_embedding(candidates)
    similarities = cosine_similarity(query_embedding, candidate_embeddings)[0]
    best_index = np.argmax(similarities)
    return candidates[best_index], similarities[best_index]
