# main.py
from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

from app.agents.graph import build_graph

app = FastAPI(title="Customer Support Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Your own secret — only you (and your widget) know this
WIDGET_SECRET = os.getenv("WIDGET_SECRET")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    intent: str
    order_id: str | None = None


@app.get("/")
def serve_widget():
    return FileResponse("app/templates/index.html")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, x_widget_key: str = Header(default=None)):
    # Reject the request if the secret key doesn't match
    if x_widget_key != WIDGET_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = graph.invoke({
        "user_message": request.message,
        "intent": None,
        "order_id": None,
        "response": None,
    })
    return ChatResponse(
        response=result["response"],
        intent=result["intent"],
        order_id=result.get("order_id"),
    )