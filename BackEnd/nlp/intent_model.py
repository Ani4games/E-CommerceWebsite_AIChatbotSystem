"""
ML-Based E-Commerce Chatbot Project
Intent Detection Model (Clean Production Version)
"""

# ===============================
# 🔧 Imports
# ===============================
import pandas as pd
import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

# ===============================
# ⚙️ Paths
# ===============================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/intents.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../models/intent_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "../models/vectorizer.pkl")

os.makedirs(os.path.join(BASE_DIR, "../models"), exist_ok=True)

# ===============================
# 🧠 Train Intent Model
# ===============================
def train_intent_model():
    """Train model and save artifacts."""
    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip().str.lower()
    df['query'] = df['query'].astype(str).str.strip()
    df['intent'] = df['intent'].astype(str).str.strip().str.lower()

    X = df['query']
    y = df['intent']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.8
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    # Save model and vectorizer
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Model training complete.")
    print("Saved to:")
    print(" -", MODEL_PATH)
    print(" -", VECTORIZER_PATH)

    return model, vectorizer


# ===============================
# 🚀 Safe Loader (Used by FastAPI)
# ===============================
def load_or_train_model():
    """Load model; train only if missing."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("⚠ No model found. Training a new one...")
        return train_intent_model()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


# ===============================
# 🔍 Predict Intent
# ===============================
def predict_intent(text, confidence_threshold=0.55):
    model, vectorizer = load_or_train_model()

    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probabilities = model.predict_proba(text_vec)[0]

    top_conf = max(probabilities)
    all_scores = dict(zip(model.classes_, probabilities))

    if top_conf < confidence_threshold:
        prediction = "uncertain"

    return {
        "intent": prediction,
        "confidence": float(top_conf),
        "all_scores": {k: float(v) for k, v in all_scores.items()}
    }


# ===============================
# 🧪 Manual Training Mode
# ===============================
if __name__ == "__main__":
    # Only run training when manually executing:
    # python intent_model.py
    train_intent_model()
