import json
import logging
from typing import Tuple, Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.friend import Attribute
from app.models.friend import FriendAttribute
from app.models.friend import Friend, FriendAttribute, Attribute
from app.utils.chat_processing_utils import find_attribute, find_friend, get_friend_attribute, get_all_friend_attributes, get_all_friend_attributes, get_friends_by_attribute
from app.utils.embedding import generate_embedding, cosine_similarity_single
from app.utils.gemini_api import generate_gemini_response
from app.utils.text_processing import clean_json_response
from app.utils.attribute_synonyms import ATTRIBUTE_SYNONYMS, LOCATION_PRIORITIES

logger = logging.getLogger(__name__)

class ChatProcessingService:
    @staticmethod
    def format_attributes(attributes):
        return "\n".join([f"- {attr.name}: {attr.value}" for attr in attributes])
    @staticmethod
    async def generate_final_answer(question: str, result: Dict[str, Any], category: int) -> str:
        if category == 1:
            prompt = f"""
            Based on the following question and result, generate a factual answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Provide a concise response that directly answers the question.
            If the status is "Yes", confirm the information using only the details from the 'answer' field.
            If the status is "No" or "Probably", state that the information is not confirmed or is uncertain.
            Include only specific details from the 'answer' and 'approximation' fields if available.
            The response should be factual and avoid any subjective interpretations.

            Your response should be a simple string, not a JSON object. Start with a clear Yes or No if applicable.
            """
        elif category == 2:
            prompt = f"""
            Based on the following question and result, generate a factual answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Please follow these guidelines to create an appropriate response:

            1. Carefully consider the specific attribute being asked about in the question.
            2. Check if the information in the 'answer' and 'approximation' fields directly relates to the asked attribute.
            3. If the information doesn't directly answer the question but is related, explain the relationship.
            4. If the exact information isn't available, clearly state this and provide any related information if available.
            5. The response should be concise but complete, addressing the question directly.
            6. Avoid making assumptions or adding information not present in the given data.
            7. If the information is uncertain or approximate, reflect this in your answer.

            Provide a natural language response that accurately reflects the available information and directly addresses the question.
            """
        elif category == 3:
            prompt = f"""
            Based on the following question and result, generate a factual answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Provide a concise response that lists all the people who match the criteria.
            Use only the information from the 'answer' field to provide details about the matching individuals.
            If no one matches, state that no one was found.
            The response should be purely factual and avoid any subjective interpretations.
            """
        elif category == 4:
            prompt = f"""
            Based on the following question and result, generate a factual answer:

            Question: {question}
            Result: {json.dumps(result, indent=2)}

            Provide a concise summary of the factual information about the person.
            Include only the information present in the 'summary' and 'answer' fields.
            If there is missing information, briefly mention it using the 'missing_info' field.
            The response should be purely factual and avoid any subjective interpretations or assumptions.
            """
        else:
            return "I'm sorry, I don't have enough information to answer that question."

        gemini_response = await generate_gemini_response(prompt)
        return clean_json_response(gemini_response.text)

    @staticmethod
    async def process_category_1(
        db: Session,
        user_id: int,
        who: str,
        what: str,
        related_subject: Optional[str] = None
    ) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 1 for user_id: {user_id}, who: {who}, what: {what}, related_subject: {related_subject}")

        friend = find_friend(db, who, user_id)
        logger.debug(f"Found friend: {friend.name if friend else 'None'} with id: {friend.id if friend else 'None'}")
        if not friend:
            logger.debug("Friend not found, returning 'No' with low confidence")
            return {"status": "No", "answer": None, "approximation": "Friend not found"}, "low"

        all_attributes = get_all_friend_attributes(db, friend.id, user_id)
        logger.debug(f"Retrieved attributes: {[attr.name for attr in all_attributes]}")
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
    async def process_category_2(
        db: Session,
        user_id: int,
        who: str,
        what: str,
        related_subject: Optional[str] = None,
        content: str = ""
    ) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 2 for user_id: {user_id}, who: {who}, what: {what}, related_subject: {related_subject}")

        friend = find_friend(db, who, user_id)
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

        final_answer = await ChatProcessingService.generate_final_answer(content, result, 2)
        if not final_answer:
            final_answer = f"I'm sorry, but I couldn't find any information about {result.get('who', 'the person')}'s {result.get('what', 'attribute')}."
        result["final_answer"] = final_answer

        logger.debug(f"Final result for category 2: {result}")
        logger.debug(f"Confidence: {confidence}")

        return result, confidence

    @staticmethod
    async def process_category_3(db: Session, user_id: int, what: str, related_subject: Optional[str] = None) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 3 for user_id: {user_id}, what: {what}, related_subject: {related_subject}")

        all_friends = db.query(Friend).filter(Friend.user_id == user_id).all()
        what_embedding = generate_embedding(what)

        matching_friends = []
        for friend in all_friends:
            all_attributes = get_all_friend_attributes(db, friend.id, user_id)
            if not all_attributes:
                continue

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

            if relevant_attributes:
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

                matching_friends.append({
                    "name": friend.name,
                    "best_attribute": best_attribute_info,
                    "similarity": best_similarity,
                    "aggregated_info": aggregated_info
                })

        if not matching_friends:
            logger.debug("No matching friends found")
            return {"status": "Not Found", "answer": None, "approximation": "No matching friends found"}, "low"

        # Gemini APIを使用して推論
        prompt = f"""
        Question: Who {what}?
        Known information about matching friends:
        {json.dumps([{
            "name": friend["name"],
            "best_matching_attribute": f"{friend['best_attribute'].name}: {friend['best_attribute'].value}",
            "other_relevant_info": friend["aggregated_info"]
        } for friend in matching_friends], indent=2)}

        Based on this information, please provide:
        1. A list of friends who most likely match the criteria, sorted by relevance.
        2. For each friend, explain why they match the criteria, using specific details from their information.
        3. A confidence score (0-1 scale) for each friend's match to the criteria.
        4. A final, concise, and natural-sounding answer to the original question that summarizes the findings.

        Return a JSON object with the following format:
        {{
            "matching_friends": [
                {{
                    "name": "Friend's name",
                    "explanation": "Explanation of why this friend matches",
                    "confidence": "A value between 0 and 1"
                }}
            ],
            "final_answer": "A concise, natural-sounding answer to the original question"
        }}
        """

        gemini_response = await generate_gemini_response(prompt)
        gemini_result = json.loads(clean_json_response(gemini_response.text))

        logger.debug(f"Gemini API response: {gemini_result}")

        # 最終的な結果を構築
        result = {
            "status": "Found" if gemini_result["matching_friends"] else "Not Found",
            "answer": gemini_result["matching_friends"],
            "final_answer": gemini_result["final_answer"]
        }

        # 信頼度の計算
        confidence = "high" if any(float(friend["confidence"]) > 0.8 for friend in gemini_result["matching_friends"]) else \
                    "medium" if any(float(friend["confidence"]) > 0.5 for friend in gemini_result["matching_friends"]) else \
                    "low"

        return result, confidence

    @staticmethod
    async def process_category_4(db: Session, user_id: int, who: str) -> Tuple[Dict[str, Any], str]:
        logger.debug(f"Processing category 4 for user_id: {user_id}, who: {who}")
        friend = find_friend(db, who, user_id)
        if not friend:
            logger.debug(f"Friend {who} not found")
            return {
                "status": "Not Found",
                "answer": None,
                "summary": f"No information found for {who}.",
                "missing_info": f"{who} not found in the database",
                "approximation": f"{who} not found in the database",
                "final_answer": f"No information available for {who}."
            }, "low"

        all_attributes = get_all_friend_attributes(db, friend.id, user_id)
        if not all_attributes:
            logger.debug(f"No attributes found for friend {who}")
            return {
                "status": "Not Found",
                "answer": None,
                "summary": f"No detailed information available for {who}.",
                "missing_info": f"No attributes found for {who}",
                "approximation": f"No information available for {who}",
                "final_answer": f"No detailed information available for {who}."
            }, "low"

        # 属性を整理
        aggregated_info = {}
        for attr in all_attributes:
            keys = attr.name.split('_')
            current = aggregated_info
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = attr.value

        logger.debug(f"aggregated_info: {aggregated_info}")

        # Gemini APIを使用して要約と説明を生成
        prompt = f"""
        Please provide a factual summary about {who} based on the following information:

        {json.dumps(aggregated_info, indent=2)}

        In your response:
        1. List only the factual information available about {who}.
        2. Do not include any assumptions, interpretations, or subjective statements.
        3. If information is missing or unclear, state this explicitly.
        4. Provide the information in a concise, bullet-point format.
        5. Provide a brief, factual paragraph summarizing the key points.

        Return a JSON object with the following format:
        {{
            "summary": "A list of factual points about {who}",
            "detailed_description": "A brief paragraph summarizing the key factual points",
            "missing_info": "List of any notable missing information",
            "final_answer": "A concise, factual summary of {who} in one or two sentences"
        }}
        """

        gemini_response = await generate_gemini_response(prompt)

        # レスポンスの内容をログに出力
        logger.debug(f"Raw Gemini API response: {gemini_response.text}")

        cleaned_response = clean_json_response(gemini_response.text)
        logger.debug(f"Cleaned Gemini API response: {cleaned_response}")

        try:
            gemini_result = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            # エラー時のフォールバック処理
            gemini_result = {
                "summary": f"Error processing information for {who}.",
                "detailed_description": "An error occurred while processing the response.",
                "missing_info": "Unable to retrieve information due to a processing error.",
                "final_answer": f"I'm sorry, but I encountered an error while retrieving information about {who}."
            }

        logger.debug(f"Processed Gemini API response: {gemini_result}")

        result = {
            "status": "Found",
            "answer": gemini_result["detailed_description"],
            "summary": gemini_result["summary"],
            "missing_info": gemini_result.get("missing_info"),
            "approximation": None,
            "final_answer": gemini_result["final_answer"]
        }

        logger.debug(f"process_category_4 result: {result}")

        return result, "high"
