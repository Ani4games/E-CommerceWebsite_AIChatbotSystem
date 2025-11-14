import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(__file__)
RAW_PATH = os.path.join(BASE_DIR, "../data/customer_queries.csv")
OUT_PATH = os.path.join(BASE_DIR, "../data/cleaned_customer_queries.csv")

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s?#]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def map_intent(query):
    q = query.lower()

    # Greeting
    if any(g in q for g in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "greeting"

    # Track order
    if any(t in q for t in ["where is my order", "track", "shipment", "delivery status"]):
        return "track_order"

    # Cancel order
    if any(c in q for c in ["cancel", "cancel my order", "stop my order"]):
        return "cancel_order"

    # Return item
    if any(r in q for r in ["return", "replace"]):
        return "return_item"

    # Refund
    if any(f in q for f in ["refund", "money back", "return my money"]):
        return "refund_request"

    # Payment Info
    if any(p in q for p in ["payment", "upi", "pay", "cod", "card"]):
        return "payment_info"

    return "other"   # fallback

def preprocess():
    df = pd.read_csv(RAW_PATH)

    # Keep only query column
    df = df[['query']]

    # Clean text
    df['query'] = df['query'].apply(clean_text)

    # Add intent column
    df['intent'] = df['query'].apply(map_intent)

    # Save output
    df.to_csv(OUT_PATH, index=False)
    print(f"✔ Cleaned data saved to: {OUT_PATH}")

    print("\nIntent distribution:")
    print(df['intent'].value_counts())

if __name__ == "__main__":
    preprocess()
