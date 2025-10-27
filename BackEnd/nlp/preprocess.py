"""
ML-Based E-Commerce Chatbot Project
Week 2 - Data Preprocessing Script
----------------------------------
Goal:
    1. Load customer query dataset
    2. Clean & preprocess the text
    3. Save cleaned output for NLP model training

Author: Anirudh Paliwal
Date: 2025-24-10
"""

# ==========================
# 🔧 1. Import Libraries
# ==========================
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK resources (only once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# ==========================
# 📂 2. Load Dataset
# ==========================
def load_data(file_path):
    """
    Reads a CSV file containing 'query' and 'response' columns.
    """
    df = pd.read_csv(file_path)
    print(f"✅ Loaded dataset with {len(df)} records.")
    return df


# ==========================
# 🧹 3. Text Cleaning
# ==========================
def clean_text(text):
    """
    Cleans text by removing unwanted symbols, URLs, and lowercasing.
    """
    text = re.sub(r"http\S+", "", text)        # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)    # Remove special characters
    text = text.lower()                        # Lowercase
    text = re.sub(r"\s+", " ", text).strip()   # Remove extra spaces
    return text


# ==========================
# ✂️ 4. Tokenization, Stopwords, Lemmatization
# ==========================
def preprocess_text(text):
    """
    Tokenizes, removes stopwords, and lemmatizes text.
    """
    tokens = nltk.word_tokenize(text)

    stop_words = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stop_words]

    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return " ".join(tokens)


# ==========================
# 💾 5. Main Preprocessing Pipeline
# ==========================
def preprocess_dataset(input_file, output_file):
    """
    Executes the full preprocessing pipeline:
        - Load dataset
        - Clean text
        - Tokenize + lemmatize
        - Save cleaned version
    """
    df = load_data(input_file)
    df["clean_query"] = df["query"].apply(lambda x: preprocess_text(clean_text(str(x))))
    df["clean_response"] = df["response"].apply(lambda x: preprocess_text(clean_text(str(x))))
    df.to_csv(output_file, index=False)
    print(f"💾 Cleaned data saved to {output_file}")


# ==========================
# 🚀 6. Run Script
# ==========================

## Problem 1: Can't find customer_queries.csv file
if __name__ == "__main__":
    input_file = "../data/customer_queries.csv"        # 🔹 Raw dataset
    output_file = "../data/cleaned_customer_queries.csv"  # 🔹 Processed output
    preprocess_dataset(input_file, output_file)
