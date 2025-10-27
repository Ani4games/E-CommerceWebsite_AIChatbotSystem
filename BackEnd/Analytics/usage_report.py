import pandas as pd
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "../logs/chatbot_logs.csv")

def generate_report():
    df = pd.read_csv(LOG_FILE, header=None,
                     names=["timestamp", "user_id", "query", "response", "intent"])

    print("===== Chatbot Usage Report =====")
    print(f"Total Conversations: {len(df)}")
    print("\nTop 5 Intents:")
    print(df["intent"].value_counts().head(5))

    print("\nMost Active Users:")
    print(df["user_id"].value_counts().head(3))

    print("\nUnanswered or Generic Queries:")
    print(df[df["intent"] == "unknown"]["query"].head(5))
    
if __name__ == "__main__":
    generate_report()
