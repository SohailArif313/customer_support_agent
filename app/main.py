from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.agents.graph import build_graph


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATE_DIR = BASE_DIR / "app" / "templates"


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Customer Support Agent",
    description="AI customer support agent built with FastAPI and LangGraph.",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this when deploying
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# LangGraph
# --------------------------------------------------

graph = build_graph()


# --------------------------------------------------
# Static Files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Customer's message",
    )


class ChatResponse(BaseModel):
    response: str
    intent: str
    order_id: str | None = None


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/", include_in_schema=False)
def serve_widget():
    """Serve the customer support chat interface."""
    return FileResponse(TEMPLATE_DIR / "index.html")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "customer-support-agent",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Process a customer message through the LangGraph agent."""

    try:
        result = graph.invoke(
            {
                "user_message": request.message,
                "intent": None,
                "order_id": None,
                "response": None,
            }
        )

        return ChatResponse(
            response=result["response"],
            intent=result["intent"],
            order_id=result.get("order_id"),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while processing the request.",
        ) from e