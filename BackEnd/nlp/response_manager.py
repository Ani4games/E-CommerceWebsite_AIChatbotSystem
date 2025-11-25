# backend/nlp/response_manager.py

from nlp.intent_model import predict_intent
from nlp.entity_model import extract_entities
from nlp.context_manager import ContextManager
from nlp.personalization import personalize_response
from nlp.knowledge_base import query_knowledge_base
from nlp.logger import log_interaction
from nlp.error_handler import log_error

context = ContextManager()

def generate_response(user_id: str, text: str):
    try:
        # ---------------------------------------
        # 1️⃣ FAQ CHECK (Highest Priority)
        # ---------------------------------------
        faq_answer = query_knowledge_base(text)
        if faq_answer:
            log_interaction(user_id, text, faq_answer, intent="faq")
            return faq_answer

        # ---------------------------------------
        # 2️⃣ INTENT DETECTION
        # ---------------------------------------
        intent_result = predict_intent(text)
        intent = intent_result["intent"]
        confidence = intent_result["confidence"]

        # ---------------------------------------
        # 3️⃣ LOW-CONFIDENCE HANDLING
        # ---------------------------------------
        if confidence < 0.40:
            fallback = "I'm not completely sure what you mean. Could you rephrase it?"
            log_interaction(user_id, text, fallback, intent="low_confidence")
            return fallback

        # ---------------------------------------
        # 4️⃣ SPECIAL CASES (Greeting / Goodbye)
        # ---------------------------------------
        if intent == "greeting":
            reply = "Hi there! 😊 How can I help you today?"
            log_interaction(user_id, text, reply, intent="greeting")
            return reply

        if intent == "goodbye":
            reply = "Goodbye! 👋 Have a great day ahead."
            log_interaction(user_id, text, reply, intent="goodbye")
            return reply

        # ---------------------------------------
        # 5️⃣ ENTITY EXTRACTION (with backup)
        # ---------------------------------------
        try:
            entities = extract_entities(text)
        except:
            entities = []

        context.update_context(user_id, intent, entities)

        # ---------------------------------------
        # 6️⃣ BASE RESPONSE TEMPLATES
        # ---------------------------------------
        base_responses = {
            "track_order": "Let me check your order status.",
            "return_item": "I can help you return your item.",
            "payment_info": "Sure! Here are the available payment methods.",
            "refund_request": "I can help you with your refund request.",
            "cancel_order": "I can help you cancel your order."
        }

        base_response = base_responses.get(intent, "I'm not fully sure, but I'll try to help.")

        # ---------------------------------------
        # 7️⃣ PERSONALIZE ONLY FOR MEANINGFUL INTENTS
        # ---------------------------------------
        SPECIAL_INTENTS = {"track_order", "payment_info", "refund_request", "return_item", "cancel_order"}

        if intent in SPECIAL_INTENTS:
            final = personalize_response(user_id, intent, base_response)
        else:
            final = base_response  # No personalization for general queries

        # ---------------------------------------
        # 8️⃣ LOGGING
        # ---------------------------------------
        log_interaction(user_id, text, final, intent=intent)

        return final

    except Exception as e:
        log_error(e)
        return "⚠️ Sorry, something went wrong on my end."
