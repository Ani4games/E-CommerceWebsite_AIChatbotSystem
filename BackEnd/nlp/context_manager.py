# backend/nlp/context_manager.py
class ContextManager:
    def __init__(self):
        self.session_data = {}

    def update_context(self, user_id, intent, entities):
        self.session_data[user_id] = {"intent": intent, "entities": entities}

    def get_context(self, user_id):
        return self.session_data.get(user_id, None)
