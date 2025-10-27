"""
ML-Based E-Commerce Chatbot Project
Week 3 - Intent Detection Model
--------------------------------
Goal:
    Train a classifier to predict user intents based on text queries.
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
import numpy as np

# ===============================
# ⚙️ Paths
# ===============================
BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "../data/cleaned_customer_queries.csv")
MODEL_PATH = os.path.join(BASE_DIR, "../models/intent_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "../models/vectorizer.pkl")

os.makedirs(os.path.join(BASE_DIR, "../models"), exist_ok=True)

# ===============================
# 🧠 Train Intent Model
# ===============================
def train_intent_model():
    # Load data
    df = pd.read_csv(DATA_PATH)
    if 'intent' not in df.columns:
        raise ValueError("Dataset must include an intent column for training.")
    
    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()
    
    # Trim leading/trailing spaces in text columns
    df['query'] = df['query'].astype(str).str.strip()
    df['intent'] = df['intent'].astype(str).str.strip().str.lower()
    
    # Check dataset size
    print(f"📊 Dataset size: {len(df)} samples")
    print(f"\n📈 Intent distribution:\n{df['intent'].value_counts()}\n")
    
    # WARNING: Check if dataset is too small
    if len(df) < 100:
        print("⚠️  WARNING: Dataset is very small (<100 samples)!")
        print("   Recommendation: Collect at least 50-100 samples per intent class")
        print("   Current model will have poor generalization.\n")
    
    X = df['query']
    y = df['intent']
    
    # Check class balance
    min_class_count = df['intent'].value_counts().min()
    if min_class_count < 5:
        print(f"⚠️  WARNING: Some classes have <5 samples (min={min_class_count})")
        print("   This will cause poor performance. Consider:")
        print("   1. Collecting more data for underrepresented classes")
        print("   2. Using stratified split to ensure each class appears in train/test\n")
    
    # Split dataset with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y  # Ensures balanced class distribution
    )
    
    print(f"🔀 Split: {len(X_train)} train, {len(X_test)} test samples")
    print(f"   Test set distribution:\n{pd.Series(y_test).value_counts()}\n")
    
    # TF-IDF Vectorization with reduced features for small datasets
    max_features = min(500, len(X_train) * 10)  # Adaptive feature limit
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),  # Include bigrams for better context
        min_df=1,  # Keep all terms (important for small datasets)
        max_df=0.8  # Remove very common terms
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    print(f"🔤 TF-IDF features: {X_train_vec.shape[1]}")
    print(f"   Feature-to-sample ratio: {X_train_vec.shape[1]/len(X_train):.2f}:1")
    if X_train_vec.shape[1] > len(X_train):
        print(f"   ⚠️  WARNING: More features than samples - risk of overfitting!\n")
    
    # Model Training
    model = MultinomialNB(alpha=1.0)  # Smoothing helps with small datasets
    model.fit(X_train_vec, y_train)
    
    # Cross-validation on training set
    cv_scores = cross_val_score(model, X_train_vec, y_train, cv=min(5, len(X_train)), scoring='accuracy')
    print(f"🔄 Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    
    # Test set evaluation
    y_pred = model.predict(X_test_vec)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✅ Test Accuracy: {test_accuracy:.3f}")
    
    # Detailed metrics
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))
    
    print("\n🔍 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    cm_df = pd.DataFrame(cm, index=model.classes_, columns=model.classes_)
    print(cm_df)
    
    # Show misclassifications
    print("\n❌ Misclassified examples:")
    misclassified = X_test[y_test != y_pred]
    for i, (query, true, pred) in enumerate(zip(misclassified, y_test[y_test != y_pred], y_pred[y_test != y_pred])):
        if i < 5:  # Show first 5
            print(f"   '{query}' -> Predicted: {pred}, Actual: {true}")
    
    # Save artifacts
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"\n💾 Model saved to {MODEL_PATH}")
    print(f"💾 Vectorizer saved to {VECTORIZER_PATH}")
    
    return model, vectorizer, X_test, y_test, y_pred, df

# ===============================
# 🔍 Predict Intent
# ===============================
def predict_intent(text):
    """Predict intent for a single query"""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Model files not found. Train the model first.")
    
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    
    text_vec = vectorizer.transform([text])
    prediction = model.predict(text_vec)[0]
    probabilities = model.predict_proba(text_vec)[0]
    
    # Get confidence scores for all classes
    intent_scores = dict(zip(model.classes_, probabilities))
    
    return {
        'intent': prediction,
        'confidence': max(probabilities),
        'all_scores': intent_scores
    }

# ===============================
# 🚀 Run
# ===============================
## For now, 34 entries will give less accuracy and other entries will be lower too.
## Creatre a better csv file, with 500+ records.
# Error 2: Issues regrading filling f1-score and other parameters. Fixed now.
if __name__ == "__main__":
    print("="*60)
    print("🤖 Training Intent Detection Model")
    print("="*60 + "\n")
    
    model, vectorizer, X_test, y_test, y_pred, df = train_intent_model()
    
    # Test predictions (FIXED: matching indices)
    print("\n" + "="*60)
    print("🧪 Sample Predictions on Test Set")
    print("="*60)
    
    for i in range(min(5, len(X_test))):
        query = X_test.iloc[i]
        true_label = y_test.iloc[i]
        pred_label = y_pred[i]
        match = "✓" if true_label == pred_label else "✗"
        print(f"{match} Query: '{query}'")
        print(f"  Predicted: {pred_label} | Actual: {true_label}\n")
    
    # Interactive testing
    print("="*60)
    print("💬 Try your own queries (type 'quit' to exit)")
    print("="*60)
    
    while True:
        user_input = input("\nEnter query: ").strip()
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        if not user_input:
            continue
        
        result = predict_intent(user_input)
        print(f"🎯 Intent: {result['intent']} (confidence: {result['confidence']:.2%})")
        print(f"   All scores: {', '.join([f'{k}: {v:.2%}' for k, v in sorted(result['all_scores'].items(), key=lambda x: x[1], reverse=True)])}")