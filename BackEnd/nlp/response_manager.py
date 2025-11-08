from nlp.intent_model import predict_intent
from nlp.entity_model import extract_entities
from nlp.context_manager import ContextManager
from nlp.personalization import personalize_response
from nlp.knowledge_base import query_knowledge_base
from nlp.logger import log_interaction
from nlp.error_handler import log_error
##Library Initial Errors: Didn't completed the programs
context = ContextManager()

def generate_response(user_id, text):
    try:
        faq_answer = query_knowledge_base(text)
        if faq_answer:
            log_interaction(user_id, text, faq_answer, intent="faq")
            return faq_answer

        intent = predict_intent(text)
        entities = extract_entities(text)
        context.update_context(user_id, intent, entities)

        base_response = "I'm not sure, but let me check."
        if intent == "track_order":
            base_response = "Tracking your latest order."
        elif intent == "return_item":
            base_response = "Returning your item now."
        elif intent == "payment_info":
            base_response = "Here's payment details."

        final = personalize_response(user_id, intent, base_response)
        log_interaction(user_id, text, final, intent=intent) #Need some csv work to be done, then maybe it may work 
        return final
    except Exception as e:
        log_error(e)
        return "⚠️ Sorry, something went wrong on my end."
