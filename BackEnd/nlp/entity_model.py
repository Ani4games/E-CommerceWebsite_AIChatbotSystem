# backend/nlp/entity_model.py
import spacy
import pickle
#Error1: Unknown Functions, and argument of another data type with another data types
def train_entity_model():
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    ner.add_label("PRODUCT")
    ner.add_label("ORDER_ID")

    # Add training samples
    TRAIN_DATA = [
        ("Where is my order for shoes?", {"entities": [(21, 26, "PRODUCT")]}),
        ("Track my order #12345", {"entities": [(15, 21, "ORDER_ID")]})
    ]

    nlp.initialize()
    for epoch in range(20):
        for text, annotations in TRAIN_DATA:
            nlp.update([ (text, annotations) ])

    with open("../../models/entity_model.pkl", "wb") as f:
        pickle.dump(nlp, f)

def extract_entities(text):
    with open("../../models/entity_model.pkl", "rb") as f:
        nlp = pickle.load(f)
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
