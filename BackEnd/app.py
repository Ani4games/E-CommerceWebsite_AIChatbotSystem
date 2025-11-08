# backend/app.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from nlp.response_manager import generate_response
from fastapi.responses import JSONResponse
from json import JSONDecodeError

app = FastAPI(title="E-Com Support Chatbot API")

class ChatRequest(BaseModel):
    user_id: str
    message: str


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

# @app.post("/chat")
# async def chat_endpoint(request: Request):
#     data = await request.json()
#     user_id = data.get("user_id", "anonymous")
#     text = data.get("message", "")
#     response = generate_response(user_id, text)
#     return {"reply": response}

# Main chatbot endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint to process user messages and return chatbot responses.
    """
    try:
        # Extract user message from request
        user_id = request.user_id
        message = request.message

        # Generate chatbot response (from NLP module)
        response = generate_response(user_id, message)

        return {"response": response}

    except JSONDecodeError:
        return JSONResponse(
            content={"error": "Invalid or empty JSON body"},
            status_code=400
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Server error: {str(e)}"},
            status_code=500
        )
@app.get("/")
def root():
    return {"message": "Chatbot backend is running! Visit /docs for API testing."}

# Run manually (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)