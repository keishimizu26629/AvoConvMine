import logging
from typing import Tuple, Dict, Any, List, Optional
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
            If the status is "Yes", confirm the information and provide relevant details from the 'answer' field.
            If the status is "No" or "Probably", explain that the information is not confirmed or is uncertain.
            Include specific details from the 'answer' and 'approximation' fields if available.
            The response should be in the same language as the question and should sound natural and conversational.

            Your response should be a simple string, not a JSON object. Start with a clear Yes or No if applicable.
            """
        if category == 2:
            prompt = f"""
            Based on the following question and result, generate a human-readable answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Please provide a concise and natural-sounding response that directly answers the question.
            If the status is "Found", include the specific information from the 'answer' field in your response.
            If the status is "Not Found", explain that the information is not available or couldn't be determined.
            The response should be in the same language as the question and should sound natural and conversational.
            Do not include phrases like "Based on the information provided" or "According to the result".
            """
        elif category == 3:
            prompt = f"""
            Based on the following question and result, generate a human-readable answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Please provide a concise and natural-sounding response that lists all the people who match the criteria.
            Use the information from the 'answer' field to provide details about the matching individuals.
            If no one matches, state that no one was found.
            The response should be in the same language as the question and should sound natural and conversational.
            """
        else:
            return "I'm sorry, I don't have enough information to answer that question."

        gemini_response = await generate_gemini_response(prompt)
        final_answer = clean_json_response(gemini_response.text)

        # 回答が JSON 形式になっていないか確認し、なっていれば適切に処理する
        try:
            parsed_answer = json.loads(final_answer)
            if isinstance(parsed_answer, dict):
                return parsed_answer.get('response', final_answer)
        except json.JSONDecodeError:
            pass

        return final_answer

    @staticmethod
    async def process_category_1(db: Session, user_id: int, who: str, what: str, related_subject: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 1 for user_id: {user_id}, who: {who}, what: {what}, related_subject: {related_subject}")

        friend = find_friend(db, who)
        if not friend:
            logger.debug("Friend not found, returning 'No' with low confidence")
            return {"status": "No", "answer": None, "approximation": "Friend not found"}, "low"

        all_attributes = get_all_friend_attributes(db, friend.id, user_id)
        if not all_attributes:
            logger.debug(f"No attributes found for friend {friend.name}")
            return {"status": "No", "answer": None, "approximation": "No attributes found"}, "low"

        what_embedding = generate_embedding(what)

        # 関連する属性を特定
        relevant_attributes = []
        for attr_info in all_attributes:
            attr_text = f"{attr_info.name} {attr_info.value}"
            attr_similarity = cosine_similarity_single(what_embedding, generate_embedding(attr_text))

            category_similarities = [cosine_similarity_single(what_embedding, generate_embedding(syn))
                                    for synonyms in ATTRIBUTE_SYNONYMS.values()
                                    for syn in synonyms]
            category_similarity = max(category_similarities) if category_similarities else 0

            if attr_similarity > 0.5 or category_similarity > 0.5:
                relevant_attributes.append((attr_info, max(attr_similarity, category_similarity)))

        if not relevant_attributes:
            logger.debug("No relevant attributes found")
            return {"status": "No", "answer": None, "approximation": "No relevant attributes found"}, "low"

        # 類似度でソートし、最も関連性の高い属性を選択
        relevant_attributes.sort(key=lambda x: x[1], reverse=True)
        best_attribute_info, best_similarity = relevant_attributes[0]

        # 関連する属性の情報を集約
        aggregated_info = {}
        for attr_info, _ in relevant_attributes:
            keys = attr_info.name.split('_')
            current = aggregated_info
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = attr_info.value

        logger.debug(f"Best matching attribute: {best_attribute_info.name} with similarity {best_similarity}")

        # Gemini APIを使用して推論
        prompt = f"""
        Question: Does {who} {what}?
        Known information about {who}:
        {json.dumps(aggregated_info, indent=2)}
        Best matching attribute: {best_attribute_info.name} with value: {best_attribute_info.value}

        Based on this information, please provide:
        1. A likelihood score (0-1 scale) that the answer to the question is Yes.
        2. The most relevant piece of information to answer this question.
        3. A detailed explanation of your reasoning, including specific details from the known information.
        4. A final, concise, and natural-sounding answer to the original question that incorporates all of the above information.

        Return a JSON object with the following format:
        {{
            "likelihood": "A value between 0 and 1",
            "relevant_info": "The most relevant piece of information",
            "explanation": "Your detailed explanation including specific information",
            "final_answer": "A concise, natural-sounding answer to the original question"
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
            "answer": best_attribute_info.value,
            "approximation": {
                "attribute": best_attribute_info.name,
                "value": best_attribute_info.value
            },
            "explanation": gemini_result['explanation'],
            "relevant_info": gemini_result['relevant_info'],
            "final_answer": gemini_result['final_answer']
        }

        return result, confidence

    @staticmethod
    async def process_category_2(db: Session, user_id: int, who: str, what: str, related_subject: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 2 for user_id: {user_id}, who: {who}, what: {what}, related_subject: {related_subject}")

        friend = find_friend(db, who)
        if not friend:
            logger.debug("Friend not found, returning 'Not Found' with low confidence")
            return {"status": "Not Found", "answer": None, "approximation": "Friend not found"}, "low"

        all_attributes = get_all_friend_attributes(db, friend.id, user_id)
        if not all_attributes:
            logger.debug(f"No attributes found for friend {friend.name}")
            return {"status": "Not Found", "answer": None, "approximation": "No attributes found"}, "low"

        what_embedding = generate_embedding(what)

        # 関連する属性名を取得
        related_attributes = []
        for category, synonyms in ATTRIBUTE_SYNONYMS.items():
            if any(synonym.lower() in what.lower() for synonym in synonyms):
                related_attributes.extend(synonyms)

        # 位置情報の優先順位を設定
        location_priority = LOCATION_PRIORITIES.get("live", [])

        best_attribute = None
        best_similarity = -1

        for attr in all_attributes:
            attr_name_lower = attr.name.lower()

            # 優先度ボーナスを計算
            priority_bonus = 0
            if attr.name in location_priority:
                priority_bonus = (len(location_priority) - location_priority.index(attr.name)) * 0.1

            # 属性名の類似度を計算
            name_similarity = cosine_similarity_single(what_embedding, generate_embedding(attr.name))

            # 属性値の類似度を計算
            value_similarity = cosine_similarity_single(what_embedding, generate_embedding(attr.value))

            # 総合的な類似度を計算
            total_similarity = max(name_similarity, value_similarity) + priority_bonus

            logger.debug(f"Attribute: {attr.name}, Value: {attr.value}, Similarity: {total_similarity}")

            if total_similarity > best_similarity:
                best_similarity = total_similarity
                best_attribute = attr

        logger.debug(f"Best matching attribute: {best_attribute.name if best_attribute else 'None'} with similarity {best_similarity}")

        if best_similarity >= 0.5:
            result = {
                "status": "Found",
                "answer": best_attribute.value,
                "approximation": {"attribute": best_attribute.name, "value": best_attribute.value}
            }
            confidence = "high" if best_similarity >= 0.8 else "medium"
        else:
            result = {"status": "Not Found", "answer": None, "approximation": "No matching attribute found"}
            confidence = "low"

        final_answer = await ChatProcessingService.generate_final_answer(f"What is {who}'s {what}?", result, 2)
        result["final_answer"] = final_answer

        return result, confidence

    @staticmethod
    async def process_category_3(db: Session, user_id: int, what: str, related_subject: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 3 for user_id: {user_id}, what: {what}")

        # 質問のembeddingを生成
        what_embedding = generate_embedding(what)

        # すべての友人属性を取得
        all_friend_attributes = (
            db.query(Friend, Attribute, FriendAttribute)
            .join(FriendAttribute, Friend.id == FriendAttribute.friend_id)
            .join(Attribute, FriendAttribute.attribute_id == Attribute.id)
            .filter(FriendAttribute.user_id == user_id)
            .all()
        )

        matching_friends = {}
        for friend, attribute, friend_attribute in all_friend_attributes:
            attr_text = f"{attribute.name}: {friend_attribute.value}"
            attr_embedding = generate_embedding(attr_text)
            similarity = cosine_similarity_single(what_embedding, attr_embedding)

            if similarity > 0.5:  # この閾値は調整可能
                if friend.id not in matching_friends:
                    matching_friends[friend.id] = {"name": friend.name, "attributes": [], "max_similarity": 0}
                matching_friends[friend.id]["attributes"].append({
                    "name": attribute.name,
                    "value": friend_attribute.value,
                    "similarity": similarity
                })
                matching_friends[friend.id]["max_similarity"] = max(matching_friends[friend.id]["max_similarity"], similarity)

        # 類似度でソート
        matching_friends = sorted(matching_friends.values(), key=lambda x: x["max_similarity"], reverse=True)

        logger.debug(f"Found {len(matching_friends)} matching friends")

        if not matching_friends:
            result = {"status": "Not Found", "answer": None, "approximation": "No matching friends found"}
            final_answer = await ChatProcessingService.generate_final_answer(f"Who has a {what}?", result, 3)
            result["final_answer"] = final_answer
            return result, "low"

        # Gemini APIを使用して回答を生成
        prompt = f"""
        Question: Who has a {what}?
        Matching friends and their relevant attributes:
        {json.dumps(matching_friends, indent=2)}

        Based on this information:
        1. List all the people who have a {what}, sorted by relevance.
        2. How confident are you in this answer? (0-1 scale)
        3. Provide a brief explanation for your reasoning, including why each person matches the criteria.

        Return a JSON object with the following format:
        {{
            "matching_people": [
                {{
                    "name": "Name1",
                    "reason": "Reason why this person matches"
                }},
                ...
            ],
            "confidence": "A value between 0 and 1",
            "explanation": "Your overall explanation"
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
