# backend/nlp/response_manager.py

from intent_model import predict_intent
from entity_model import extract_entities
from context_manager import ContextManager
from personalization import personalize_response
from knowledge_base import query_knowledge_base
from logger import log_interaction
from error_handler import log_error

context = ContextManager()

def generate_response(user_id: str, text: str):
    try:
        # 1️⃣ FAQ CHECK
        faq_answer = query_knowledge_base(text)
        if faq_answer:
            log_interaction(user_id, text, faq_answer, intent="faq")
            return faq_answer

        # 2️⃣ INTENT DETECTION
        intent_result = predict_intent(text)
        intent = intent_result["intent"]          # FIXED
        confidence = intent_result["confidence"]  # (optional)

        # 3️⃣ ENTITY EXTRACTION
        try:
            entities = extract_entities(text)
        except:
            entities = []

        # Update context
        context.update_context(user_id, intent, entities)

        # 4️⃣ BASE RESPONSE (Intent → Template Mapping)
        base_responses = {
            "track_order": "Let me check your order status.",
            "return_item": "I can help you return your item.",
            "payment_info": "Sure! Here are the payment options.",
            "refund_request": "I can help you with your refund.",
            "cancel_order": "I can help you cancel your order."
        }

        base_response = base_responses.get(intent, "I'm not fully sure, but I'll try to help.")

        # 5️⃣ PERSONALIZATION
        final = personalize_response(user_id, intent, base_response)

        # 6️⃣ LOGGING
        log_interaction(user_id, text, final, intent=intent)

        return final

    except Exception as e:
        log_error(e)
        return "⚠️ Sorry, something went wrong on my end."
