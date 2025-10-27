# backend/nlp/knowledge_base.py
import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(__file__)
## Initial Errors: csv file reading issues
FAQ_PATH = os.path.join(BASE_DIR, "../data/faqs.csv")
VEC_PATH = os.path.join(BASE_DIR, "../models/faqs_vectorizer.pkl")

def build_knowledge_base():
    df = pd.read_csv(FAQ_PATH)
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(df["question"])
    joblib.dump((vectorizer, vectors, df), VEC_PATH)
    print("✅ Knowledge Base built and saved!")

def query_knowledge_base(query, threshold=0.3):
    vectorizer, vectors, df = joblib.load(VEC_PATH)
    q_vec = vectorizer.transform([query])
    sim = cosine_similarity(q_vec, vectors).flatten()
    idx = sim.argmax()
    if sim[idx] > threshold:
        return df.iloc[idx]["answer"]
    return None

if __name__ == "__main__":
    build_knowledge_base()
    print(query_knowledge_base("How do I cancel my purchase?"))
