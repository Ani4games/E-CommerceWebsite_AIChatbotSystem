# backend/nlp/personalization.py
import json
import os

# ------------------------------------------------------
# Setup
# ------------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
USER_FILE = os.path.join(BASE_DIR, "../data/user_profiles.json")

# Cache user data after first load
_user_cache = None

# ------------------------------------------------------
# Helper: Load user profiles safely
# ------------------------------------------------------
def load_user_profiles():
    global _user_cache

    if _user_cache is not None:
        return _user_cache  # return cached data

    if not os.path.exists(USER_FILE):
        print(f"⚠️ user_profiles.json not found at {USER_FILE}. Using default guest profile.")
        _user_cache = {
            "guest": {
                "name": "Guest",
                "preferred_product": "item",
                "recent_order": "#0000"
            }
        }
        return _user_cache

    try:
        with open(USER_FILE, "r", encoding="utf-8") as f:
            _user_cache = json.load(f)
    except json.JSONDecodeError:
        print("⚠️ user_profiles.json is invalid JSON. Using default profile.")
        _user_cache = {
            "guest": {
                "name": "Guest",
                "preferred_product": "item",
                "recent_order": "#0000"
            }
        }
    return _user_cache

# ------------------------------------------------------
# Get user profile
# ------------------------------------------------------
def get_user_profile(user_id):
    users = load_user_profiles()
    profile = users.get(user_id, users.get("guest", {
        "name": "Guest",
        "preferred_product": "item",
        "recent_order": "#0000"
    }))
    return profile

# ------------------------------------------------------
# Personalize chatbot response
# ------------------------------------------------------
def personalize_response(user_id, intent, base_response):
    user = get_user_profile(user_id)
    name = user.get("name", "Guest")
    product = user.get("preferred_product", "product")
    order_id = user.get("recent_order", "#0000")

    if intent == "track_order":
        return f"Hi {name}! Your order {order_id} for {product} is currently being processed."
    elif intent == "return_item":
        return f"Sure {name}, I’ve initiated a return for your {product}."
    elif intent == "payment_info":
        return f"{name}, you can pay using UPI, card, or COD — whichever you prefer."
    else:
        return f"{base_response} (By the way, nice choice on those {product}s 😄)"

# ------------------------------------------------------
# Quick test
# ------------------------------------------------------
if __name__ == "__main__":
    print(personalize_response("guest", "track_order", "Okay"))
