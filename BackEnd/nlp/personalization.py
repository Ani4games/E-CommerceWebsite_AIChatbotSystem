# backend/nlp/personalization.py
import json, os

BASE_DIR = os.path.dirname(__file__)
USER_FILE = os.path.join(BASE_DIR, "../data/user_profiles.json")

def get_user_profile(user_id):
    with open(USER_FILE, "r") as f:
        users = json.load(f)
    return users.get(user_id, users["guest"])

def personalize_response(user_id, intent, base_response):
    user = get_user_profile(user_id)
    name = user["name"]
    product = user["preferred_product"]
    order_id = user["recent_order"]

    if intent == "track_order":
        return f"Hi {name}! Your order {order_id} for {product} is currently being processed."
    elif intent == "return_item":
        return f"Sure {name}, I've initiated a return for your {product}."
    elif intent == "payment_info":
        return f"{name}, you can pay using UPI, card, or COD — whichever you prefer."
    else:
        return f"{base_response} (by the way, nice choice on those {product}s 😄)"
