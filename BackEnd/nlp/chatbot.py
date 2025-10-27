import pickle
import random
import json
from preprocess import clean_text

# load model
with open("BackEnd/models/intent_model.pkl", "rb") as f:
    vectorizer, model = pickle.load(f)

# load intents
with open("BackEnd/data/intents.json", "r") as f:
    intents = json.load(f)["intents"]

def predict_intent(text):
    cleaned = clean_text(text)
    X = vectorizer.transform([cleaned])
    tag = model.predict(X)[0]
    return tag

def get_response(tag):
    for intent in intents:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "Sorry, I didn't understand that."

def chat():
    print("🤖 Chatbot is ready! Type 'quit' to exit.")
    while True:
        msg = input("You: ")
        if msg.lower() == "quit":
            break
        tag = predict_intent(msg)
        response = get_response(tag)
        print("Bot:", response)

if __name__ == "__main__":
    chat()
