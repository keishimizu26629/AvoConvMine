import logging
from typing import Tuple, Dict, Any, List
from sqlalchemy.orm import Session
from models.friend import Attribute
from models.friend import FriendAttribute
from models.friend import Friend, FriendAttribute, Attribute
from utils.chat_processing_utils import find_attribute, find_friend, get_friend_attribute, get_all_friend_attributes, get_all_friend_attributes, get_friends_by_attribute
from utils.embedding import generate_embedding, cosine_similarity_single
from utils.gemini_api import generate_gemini_response
from utils.text_processing import clean_json_response
from utils.attribute_synonyms import ATTRIBUTE_SYNONYMS, LOCATION_PRIORITIES
import json

logger = logging.getLogger(__name__)

class ChatProcessingService:
    @staticmethod
    def format_attributes(attributes):
        return "\n".join([f"- {attr.name}: {attr.value}" for attr in attributes])
    @staticmethod
    async def generate_final_answer(question: str, result: Dict[str, Any], category: int) -> str:
        if category == 1:
            prompt = f"""
            Based on the following question and result, generate a human-readable answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Please provide a concise and natural-sounding response that answers the question directly.
            If the status is "Yes", confirm the information.
            If the status is "No" or "Probably", explain that the information is not confirmed or is uncertain.
            The response should be in the same language as the question and should sound natural and conversational.
            """
        elif category == 2:
            prompt = f"""
            Based on the following question and result, generate a human-readable answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Please provide a concise and natural-sounding response that directly answers the question.
            Include the specific information (answer) in your response if available.
            If the information is not found, explain that it's not available.
            The response should be in the same language as the question and should sound natural and conversational.
            Do not start the answer with "Yes" or "No".
            """
        if category == 3:
            prompt = f"""
            Based on the following question and result, generate a human-readable answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Please provide a concise and natural-sounding response that lists all the people who match the criteria.
            If no one matches, state that no one was found.
            The response should be in the same language as the question and should sound natural and conversational.
            """
        else:
            return "I'm sorry, I don't have enough information to answer that question."

        gemini_response = await generate_gemini_response(prompt)
        final_answer = clean_json_response(gemini_response.text)

        return final_answer

    @staticmethod
    async def process_category_1(db: Session, user_id: int, who: str, what: str) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 1 for user_id: {user_id}, who: {who}, what: {what}")

        friend = find_friend(db, who)
        if not friend:
            logger.debug("Friend not found, returning 'No' with low confidence")
            return {"status": "No", "answer": None, "approximation": "Friend not found"}, "low"

        all_attributes = get_all_friend_attributes(db, friend.id, user_id)
        if not all_attributes:
            logger.debug(f"No attributes found for friend {friend.name}")
            return {"status": "No", "answer": None, "approximation": "No attributes found"}, "low"

        what_embedding = generate_embedding(what)

        # 関連する属性名を取得
        related_attributes = []
        for category, synonyms in ATTRIBUTE_SYNONYMS.items():
            if any(synonym.lower() in what.lower() for synonym in synonyms):
                related_attributes.extend(synonyms)

        # 位置情報の優先順位を設定
        location_priority = None
        if "live" in what.lower():
            location_priority = LOCATION_PRIORITIES["live"]
        elif "work" in what.lower():
            location_priority = LOCATION_PRIORITIES["work"]

        best_attribute = None
        best_similarity = -1

        for attr in all_attributes:
            if related_attributes and attr.name not in related_attributes:
                continue

            # 位置情報の優先順位に基づいて類似度にボーナスを与える
            bonus = 0
            if location_priority:
                try:
                    priority_index = location_priority.index(attr.name)
                    bonus = (len(location_priority) - priority_index) * 0.1  # 優先度に応じてボーナスを付与
                except ValueError:
                    pass

            attr_embedding = generate_embedding(f"{attr.name}: {attr.value}")
            similarity = cosine_similarity_single(what_embedding, attr_embedding) + bonus
            logger.debug(f"Attribute: {attr.name}, Value: {attr.value}, Similarity: {similarity}")
            if similarity > best_similarity:
                best_similarity = similarity
                best_attribute = attr

        logger.debug(f"Best matching attribute: {best_attribute.name if best_attribute else 'None'} with similarity {best_similarity}")

        # Gemini APIを使用して推論
        prompt = f"""
        Question: Does {who} {what}?
        Known information about {who}:
        {json.dumps([{"name": attr.name, "value": attr.value} for attr in all_attributes], indent=2)}
        Best matching attribute: {best_attribute.name if best_attribute else 'None'} with value: {best_attribute.value if best_attribute else 'None'}

        Based on this information, answer the following:
        1. How likely is it that the answer to the question is Yes? (0-1 scale)
        2. What is the most relevant piece of information to answer this question?
        3. Provide a brief explanation for your reasoning.

        Return a JSON object with the following format:
        {{
            "likelihood": "A value between 0 and 1",
            "relevant_info": "The most relevant piece of information",
            "explanation": "Your explanation"
        }}
        """

        gemini_response = await generate_gemini_response(prompt)
        gemini_result = json.loads(clean_json_response(gemini_response.text))

        logger.debug(f"Gemini API response: {gemini_result}")

        # 最終的な判断
        likelihood = float(gemini_result['likelihood'])
        if likelihood > 0.8:
            status = "Yes"
            confidence = "high"
        elif likelihood > 0.5:
            status = "Probably"
            confidence = "medium"
        else:
            status = "No"
            confidence = "low"

        result = {
            "status": status,
            "answer": best_attribute.value if best_attribute else None,
            "approximation": {
                "attribute": best_attribute.name,
                "value": best_attribute.value
            } if best_attribute else None,
            "explanation": gemini_result['explanation'],
            "relevant_info": gemini_result['relevant_info']
        }

        final_answer = await ChatProcessingService.generate_final_answer(f"Does {who} {what}?", result, 1)
        result["final_answer"] = final_answer

        return result, confidence

    @staticmethod
    async def process_category_2(db: Session, user_id: int, who: str, what: str) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 2 for user_id: {user_id}, who: {who}, what: {what}")

        friend = find_friend(db, who)
        if not friend:
            logger.debug("Friend not found, returning 'No' with low confidence")
            return {"status": "No", "answer": None, "approximation": "Friend not found"}, "low"

        # 全ての属性を取得
        all_attributes = get_all_friend_attributes(db, friend.id, user_id)
        if not all_attributes:
            logger.debug(f"No attributes found for friend {friend.name}")
            return {"status": "No", "answer": None, "approximation": "No attributes found"}, "low"

        # 質問のembeddingを生成
        what_embedding = generate_embedding(what)

        # 関連する属性名を取得
        related_attributes = []
        for category, synonyms in ATTRIBUTE_SYNONYMS.items():
            if any(synonym.lower() in what.lower() for synonym in synonyms):
                related_attributes.extend(synonyms)

        # 位置情報の優先順位を設定
        location_priority = None
        if "live" in what.lower():
            location_priority = LOCATION_PRIORITIES["live"]
        elif "work" in what.lower():
            location_priority = LOCATION_PRIORITIES["work"]

        # 最も類似度の高い属性を見つける
        best_attribute = None
        best_similarity = -1

        for attr in all_attributes:
            if related_attributes and attr.name not in related_attributes:
                continue

            # 位置情報の優先順位に基づいて類似度にボーナスを与える
            bonus = 0
            if location_priority:
                try:
                    priority_index = location_priority.index(attr.name)
                    bonus = (len(location_priority) - priority_index) * 0.1  # 優先度に応じてボーナスを付与
                except ValueError:
                    pass

            attr_embedding = generate_embedding(attr.name)
            similarity = cosine_similarity_single(what_embedding, attr_embedding) + bonus
            logger.debug(f"Attribute: {attr.name}, Similarity: {similarity}")
            if similarity > best_similarity:
                best_similarity = similarity
                best_attribute = attr

        logger.debug(f"Best matching attribute: {best_attribute.name if best_attribute else 'None'} with similarity {best_similarity}")

        if best_similarity >= 0.5:  # 類似度のしきい値を調整
            result = {
                "status": "Yes",
                "answer": best_attribute.value,
                "approximation": {"attribute": best_attribute.name, "value": best_attribute.value}
            }
            confidence = "high" if best_similarity >= 0.8 else "medium"
        else:
            result = {"status": "No", "answer": None, "approximation": "No matching attribute found"}
            confidence = "low"

        final_answer = await ChatProcessingService.generate_final_answer(f"What is {who}'s {what}?", result, 2)
        result["final_answer"] = final_answer

        return result, confidence

    @staticmethod
    async def process_category_3(db: Session, user_id: int, what: str) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 3 for user_id: {user_id}, what: {what}")

        # 全ての属性を取得
        all_attributes = db.query(Attribute.name).distinct().all()
        all_attribute_names = [attr.name for attr in all_attributes]

        # 質問のembeddingを生成
        what_embedding = generate_embedding(what)

        # 各属性との類似度を計算
        attribute_similarities = []
        for attr_name in all_attribute_names:
            attr_embedding = generate_embedding(attr_name)
            similarity = cosine_similarity_single(what_embedding, attr_embedding)
            attribute_similarities.append((attr_name, similarity))

        # 類似度でソートし、上位の属性を選択
        attribute_similarities.sort(key=lambda x: x[1], reverse=True)
        relevant_attributes = [attr[0] for attr in attribute_similarities[:5]]  # 上位5つの属性を使用

        logger.debug(f"Selected relevant attributes: {relevant_attributes}")

        # 関連する属性に基づいて友人を検索
        matching_friends = (
            db.query(Friend)
            .join(FriendAttribute, Friend.id == FriendAttribute.friend_id)
            .join(Attribute, FriendAttribute.attribute_id == Attribute.id)
            .filter(
                FriendAttribute.user_id == user_id,
                Attribute.name.in_(relevant_attributes)
            )
            .distinct()
            .all()
        )

        logger.debug(f"Found {len(matching_friends)} matching friends")

        if not matching_friends:
            result = {"status": "No", "answer": None, "approximation": "No matching friends found"}
            final_answer = await ChatProcessingService.generate_final_answer(f"Who has a {what}?", result, 3)
            result["final_answer"] = final_answer
            return result, "low"

        # 各友人の関連属性を取得
        friend_data = []
        for friend in matching_friends:
            attributes = (
                db.query(Attribute.name, FriendAttribute.value)
                .join(FriendAttribute, Attribute.id == FriendAttribute.attribute_id)
                .filter(
                    FriendAttribute.friend_id == friend.id,
                    FriendAttribute.user_id == user_id,
                    Attribute.name.in_(relevant_attributes)
                )
                .all()
            )
            friend_data.append({
                "name": friend.name,
                "attributes": dict(attributes)
            })

        # Gemini APIを使用して回答を生成
        prompt = f"""
        Question: Who has a {what}?
        Matching friends and their relevant attributes:
        {json.dumps(friend_data, indent=2)}

        Based on this information:
        1. List all the people who have a {what}.
        2. How confident are you in this answer? (0-1 scale)
        3. Provide a brief explanation for your reasoning.

        Return a JSON object with the following format:
        {{
            "matching_people": ["Name1", "Name2", ...],
            "confidence": "A value between 0 and 1",
            "explanation": "Your explanation"
        }}
        """

        gemini_response = await generate_gemini_response(prompt)
        gemini_result = json.loads(clean_json_response(gemini_response.text))

        logger.debug(f"Gemini API response: {gemini_result}")

        # 最終的な判断
        confidence = float(gemini_result['confidence'])
        if confidence > 0.8:
            confidence_level = "high"
        elif confidence > 0.5:
            confidence_level = "medium"
        else:
            confidence_level = "low"

        result = {
            "status": "Found" if gemini_result['matching_people'] else "Not Found",
            "answer": gemini_result['matching_people'],
            "approximation": None,
            "explanation": gemini_result['explanation']
        }

        final_answer = await ChatProcessingService.generate_final_answer(f"Who has a {what}?", result, 3)
        result["final_answer"] = final_answer

        return result, confidence_level
