# backend/nlp/context_manager.py
import datetime

class ContextManager:
    """
    Tracks user context across multiple chatbot interactions.
    Stores the last detected intent and entities for each user_id.
    """

    def __init__(self):
        # Structure: {user_id: {"intent": str, "entities": list, "updated_at": datetime}}
        self.session_data = {}

    def update_context(self, user_id, intent, entities):
        """
        Update or create context for a given user.
        """
        if not user_id:
            return  # safety: ignore missing IDs

        self.session_data[user_id] = {
            "intent": intent,
            "entities": entities,
            "updated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"[CTX] Updated for {user_id} → intent={intent}, entities={entities}")

    def get_context(self, user_id):
        """
        Retrieve saved context for a given user.
        Returns None if no prior data exists.
        """
        return self.session_data.get(user_id)

    def clear_context(self, user_id=None):
        """
        Clear context for a single user or all users.
        """
        if user_id:
            self.session_data.pop(user_id, None)
            print(f"[CTX] Cleared context for {user_id}")
        else:
            self.session_data.clear()
            print("[CTX] Cleared all user contexts")
if __name__ == "__main__":
    ctx = ContextManager()
    ctx.update_context("user123", "track_order", [("order #12345", "ORDER_ID")])
    print(ctx.get_context("user123"))
    ctx.clear_context("user123")
    print(ctx.get_context("user123"))
