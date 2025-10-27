🧠 ML-Based E-Commerce Customer Support Chatbot

A machine learning–powered chatbot that can understand and respond to e-commerce customer queries.
Built with FastAPI (backend), Python NLP modules, and ready for integration with your frontend.

📁 Project Structure
chatbot_project/
│
├── backend/
│   ├── app.py                          # FastAPI backend (to be built in later weeks)
│   │
│   ├── nlp/                            # NLP + ML logic
│   │   ├── preprocess.py               # Week 2: text cleaning pipeline
│   │   ├── intent_model.py             # Week 3: intent classification model
│   │   └── entity_model.py             # Week 4: entity recognition (up next)
│   │
│   ├── data/
│   │   ├── customer_queries.csv        # Raw input dataset
│   │   ├── cleaned_customer_queries.csv# Preprocessed + labeled dataset
│   │   ├── intents.json                # Intent definitions (optional)
│   │   └── faqs.csv                    # FAQ data source
│   │
│   └── models/
│       ├── intent_model.pkl            # Trained ML model
│       └── vectorizer.pkl              # TF-IDF vectorizer
│
├── frontend/                           # Your existing frontend code
├── notebooks/                          # Experimental work
├── requirements.txt                    # Python dependencies
└── README.md                           # This file

⚙️ Setup Instructions
1️⃣ Create Environment
python -m venv venv
source venv/bin/activate      # (Linux/Mac)
venv\Scripts\activate         # (Windows)

2️⃣ Install Requirements

In your project root:

pip install -r requirements.txt

3️⃣ Download NLTK Resources (first time only)
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('stopwords')
>>> nltk.download('wordnet')
>>> exit()

🧹 Week 2 — Data Preprocessing

File: backend/nlp/preprocess.py

This cleans and lemmatizes your dataset.

▶️ Run
cd backend/nlp
python preprocess.py

💾 Output

backend/data/cleaned_customer_queries.csv
(cleaned and ready for training)

🧠 Week 3 — Intent Detection Model

File: backend/nlp/intent_model.py

This trains a TF-IDF + Naive Bayes classifier to predict user intents.

▶️ Run
cd backend/nlp
python intent_model.py

💾 Output Files

backend/models/intent_model.pkl

backend/models/vectorizer.pkl

🧩 Sample Output
✅ Accuracy: 0.90
💾 Model saved to ../models/intent_model.pkl
💾 Vectorizer saved to ../models/vectorizer.pkl

🗨️ Input: I want to cancel my order
🤖 Predicted Intent: order_cancel

🧩 Test Prediction Manually

You can directly import and test in Python:

from nlp.intent_model import predict_intent
print(predict_intent("I want to return my product"))


Output:

return_item

🧾 What’s Next
🔹 Week 4 — Entity Recognition (NER)

🎯 Goal

Enable the chatbot to:

Recognize key entities (product names, order IDs, dates, etc.)

Maintain context across messages

Generate dynamic, personalized responses

⚙️ Setup & Installation
1️⃣ Activate environment
cd chatbot_project
pip install -r requirements.txt

2️⃣ Train the entity recognition model
cd backend/nlp
python entity_model.py


This will create:

models/entity_model.pkl

🧠 Testing the System
🧾 Extract entities
python -i entity_model.py
>>> extract_entities("Track my order #12345 for shoes")
[('12345', 'ORDER_ID'), ('shoes', 'PRODUCT')]

🔁 Maintain context
python -i context_manager.py
>>> ctx = ContextManager()
>>> ctx.update_context("user1", "order_status", {"product": "shoes"})
>>> ctx.get_context("user1")
{'intent': 'order_status', 'entities': {'product': 'shoes'}}

💬 Generate responses
python -i response_manager.py
>>> generate_response("user1", "Track my order for shoes")
'Your shoes order is being processed.'

📘 Key Concepts Practiced
Concept	Description
NER (Named Entity Recognition)	Identifying named items (e.g., “order #12345”, “laptop”)
Context Management	Keeping track of the previous user message and intent
Response Generation	Dynamic replies using recognized entities
Integration Flow	Combines intent + entity + context for realistic customer support

🤖 Week 5 — Building the Chatbot Backend (FastAPI Integration)
🎯 Goal

This week, we transform your NLP chatbot logic into a fully functional backend API using FastAPI.
You’ll be able to send messages, get smart replies, and even retrain your models — all through HTTP endpoints.

⚙️ 1️⃣ Setup
Activate your environment and install required libraries:
cd chatbot_project
pip install fastapi uvicorn


(Other dependencies such as scikit-learn, spacy, and pandas should already be installed from previous weeks.)

🧠 2️⃣ Backend API (app.py)

Your backend/app.py file defines:

/health → Quick server check

/chat → Sends user messages and gets responses

/train → Optional retraining of NLP models

Run the server:
cd backend
uvicorn app:app --reload


Output:

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

🧪 3️⃣ Test the API

Visit 👉 http://127.0.0.1:8000/docs

You’ll see FastAPI’s Swagger UI — where you can send sample requests like:

/chat

POST Request Body

{
  "user_id": "user123",
  "message": "Where is my order for shoes?"
}


Response

{
  "reply": "Your shoes order is being processed."
}

/health
GET /health


Response

{"status": "Chatbot backend is running 🚀"}

/train (Optional)

If you added the training endpoint:

POST /train


Response

{"message": "Models retrained successfully ✅"}

💬 4️⃣ Example Integration with Frontend

When you connect your existing frontend, you’ll send chat messages to the backend like this:

const response = await fetch("http://127.0.0.1:8000/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ user_id: "u1", message: "Track my order" })
});
const data = await response.json();
console.log(data.reply);


Output on console:

Your order is being processed.

🧩 5️⃣ Key Concepts Practiced
Concept	Description
FastAPI	Create high-performance async REST APIs
CORS	Allow communication between backend & frontend
Model Serving	Load trained intent/entity models
Request/Response Cycle	Communicate using structured JSON data
Swagger UI	Test endpoints visually without code