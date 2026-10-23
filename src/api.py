
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.router import route_request
from src.analytics import get_analytics

app = FastAPI(
    title="AI Model Router & Cost Optimizer",
    description="Routes AI requests and tracks usage metrics.",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "message": "AI Model Router API is running",
        "status": "healthy",
    }


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        return route_request(request.prompt)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


@app.get("/analytics")
def analytics():
    return get_analytics()
