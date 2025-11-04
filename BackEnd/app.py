# backend/app.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from nlp.response_manager import generate_response

app = FastAPI(title="E-Com Support Chatbot API")

# Enable CORS for your frontend later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return {"status": "Chatbot backend is running 🚀"}

@app.post("/chat")
async def chat_endpoint(request: Request):
    data = await request.json()
    user_id = data.get("user_id", "anonymous")
    text = data.get("message", "")
    response = generate_response(user_id, text)
    return {"reply": response}
@app.get("/")
def root():
    return {"message": "Chatbot backend is running! Visit /docs for API testing."}
