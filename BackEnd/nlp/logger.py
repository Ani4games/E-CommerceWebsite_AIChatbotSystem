# backend/nlp/logger.py
import csv, os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/chatbot_logs.csv")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log_interaction(user_id, user_input, bot_response, intent="unknown"):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), user_id, user_input, bot_response, intent])
