# backend/nlp/entity_model.py
import os
import pickle
import spacy
import re
from spacy.training import Example

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/entity_model.pkl")

def train_entity_model():
    """
    Trains a very simple custom NER model to detect PRODUCT and ORDER_ID entities.
    """
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    ner.add_label("PRODUCT")
    ner.add_label("ORDER_ID")

    TRAIN_DATA = [
        ("Where is my order for shoes?", {"entities": [(21, 26, "PRODUCT")]}),
        ("Track my order #12345", {"entities": [(15, 21, "ORDER_ID")]}),
        ("Cancel my order #67890", {"entities": [(16, 22, "ORDER_ID")]}),
        ("I want refund for jacket", {"entities": [(20, 26, "PRODUCT")]}),
    ]

    optimizer = nlp.initialize()
    for epoch in range(20):
        losses = {}
        for text, annotations in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotations)
            nlp.update([example], sgd=optimizer, losses=losses)
        print(f"Epoch {epoch+1} Losses: {losses}")

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(nlp, f)

    print(f"✅ Entity model saved at {MODEL_PATH}")


# ------------------------
# Entity extraction function
# ------------------------
_nlp_model = None  # cached model

def extract_entities(text):
    """
    Extracts PRODUCT and ORDER_ID entities from text using trained model.
    Falls back to regex extraction if model not found.
    """
    global _nlp_model

    if _nlp_model is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                _nlp_model = pickle.load(f)
        else:
            print("⚠️ Entity model not found. Using regex fallback.")
            _nlp_model = None

    entities = []
    if _nlp_model:
        doc = _nlp_model(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Fallback regex extraction (in case model fails)
    if not entities:
        order_match = re.search(r"#\d{4,6}", text)
        if order_match:
            entities.append((order_match.group(), "ORDER_ID"))
        if any(word in text.lower() for word in ["shoes", "jacket", "item", "product"]):
            entities.append(("product", "PRODUCT"))

    return entities


if __name__ == "__main__":
    train_entity_model()
    print(extract_entities("Track my order #12345 for shoes."))
