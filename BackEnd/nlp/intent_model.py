"""
E-Commerce Chatbot — Intent Classification Model (Optimized Version)
Author: Anirudh ✨
"""

# ===============================
# 🔧 Imports
# ===============================
import os
import joblib
import warnings
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

warnings.filterwarnings("ignore")

# ===============================
# 📂 Paths
# ===============================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/intents.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../models/intent_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "../models/vectorizer.pkl")

os.makedirs(os.path.join(BASE_DIR, "../models"), exist_ok=True)


# ===============================
# 🧽 CLEANER — Intent + Text
# ===============================
def clean_dataset(df):
    df = df.copy()

    df.columns = df.columns.str.strip().str.lower()

    df["query"] = (
        df["query"]
        .astype(str)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
        .str.lower()
    )

    # Keep underscores: greeting, return_item — DO NOT remove!
    df["intent"] = (
        df["intent"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    return df


# ===============================
# 🧠 TRAIN INTENT MODEL
# ===============================
def train_intent_model():
    print("\n============================================================")
    print("🤖 TRAINING OPTIMIZED INTENT CLASSIFICATION MODEL")
    print("============================================================\n")

    df = pd.read_csv(DATA_PATH)
    df = clean_dataset(df)

    # Show distribution
    print("================ INTENT DISTRIBUTION ================")
    print(f"Total samples: {len(df)}")
    print(df["intent"].value_counts())
    print("=====================================================\n")

    X = df["query"]
    y = df["intent"]

    # Stratified & safe split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # ===============================
    # ⚡ OPTIMIZED TF-IDF VECTORIZER
    # ===============================
    # Word n-grams + Char n-grams = HUGE boost
    vectorizer = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        min_df=2,
        max_df=0.9,
        sublinear_tf=True,
        lowercase=True,
        max_features=10000
    )

    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # ===============================
    # ⚙️ LOGISTIC REGRESSION (balanced)
    # ===============================
    model = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        multi_class="ovr",
        n_jobs=-1
    )
    model.fit(X_train_vec, y_train)

    # Save artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Model training complete.")
    print("Saved to:")
    print(" -", MODEL_PATH)
    print(" -", VECTORIZER_PATH)

    # ===============================
    # 📊 EVALUATION
    # ===============================
    print("\n📊 Evaluating Model...\n")

    y_pred = model.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Accuracy: {acc:.3f}")

    print("\n📄 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    print("📌 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    print(pd.DataFrame(cm, index=model.classes_, columns=model.classes_))

    print("\n❌ Sample Misclassifications:")
    for q, t, p in zip(X_test[:15], y_test[:15], y_pred[:15]):
        if t != p:
            print(f"Query: {q}")
            print(f"  Predicted: {p}")
            print(f"  Actual:    {t}")
            print("---")

    return model, vectorizer


# ===============================
# 🚀 SAFE LOADER (FastAPI)
# ===============================
def load_or_train_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("⚠ No model found. Training new one...")
        return train_intent_model()

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    return model, vectorizer


# ===============================
# 🔍 Predict Intent
# ===============================
def predict_intent(text, confidence_threshold=0.55):
    model, vectorizer = load_or_train_model()

    vec = vectorizer.transform([text.lower()])
    probs = model.predict_proba(vec)[0]

    prediction = model.predict(vec)[0]
    top_conf = float(max(probs))

    # If confidence too low → fallback
    if top_conf < confidence_threshold:
        prediction = "uncertain"

    return {
        "intent": prediction,
        "confidence": top_conf,
        "scores": dict(zip(model.classes_, [float(p) for p in probs]))
    }


# ===============================
# 🧪 Manual Execution
# ===============================
if __name__ == "__main__":
    train_intent_model()
