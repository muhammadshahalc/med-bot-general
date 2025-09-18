

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from contextlib import asynccontextmanager
from chatbot.llm import create_llm
from chatbot.config import Config
import os
from dotenv import load_dotenv

# Load environment only in local dev
if os.getenv("RENDER") is None:
    load_dotenv()

# Request + Response models
class QueryRequest(BaseModel):
    message: str

class QueryResponse(BaseModel):
    answer: str
    success: bool

# Initialize FastAPI app
app = FastAPI(title="Medical Chatbot API")

# Enable CORS (optional: you can restrict to your website later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to ["https://yourwebsite.com"] in production
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

# Global vars
llm = None
AUTHORIZATION_API_KEY = os.getenv("AUTHORIZATION_API_KEY")  # renamed key

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm
    llm = create_llm()
    yield

app.router.lifespan_context = lifespan

# Root endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Medical Chatbot API 🚑"}

# Chat endpoint with API key authentication
@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(
    request: QueryRequest,
    x_authorization_api_key: str = Header(...)  # new header name
):
    if x_authorization_api_key != AUTHORIZATION_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if llm is None:
        raise HTTPException(status_code=500, detail="LLM not initialized")

    try:
        # Only system prompt + current user message (no memory)
        conversation = f"System: {Config.SYSTEM_PROMPT}\n\n"
        conversation += f"User: {request.message}\nBot:"

        # Call LLM
        response = llm.invoke(conversation)
        answer = response.content if hasattr(response, "content") else str(response)

        return QueryResponse(answer=answer, success=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
