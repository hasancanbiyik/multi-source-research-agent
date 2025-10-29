from fastapi import FastAPI
from pydantic import BaseModel
from main import graph
import uvicorn
import time
from prometheus_fastapi_instrumentator import Instrumentator

# ---------- Request / Response Models ----------

class Query(BaseModel):
    question: str

class AskResponse(BaseModel):
    question: str
    final_answer: str | None
    google_analysis: str | None
    bing_analysis: str | None
    reddit_analysis: str | None
    selected_reddit_urls: list[str] | None
    latency_ms: float


# ---------- FastAPI App ----------

app = FastAPI(
    title="Multi-Source Research Agent API",
    description="A FastAPI interface for the multi-source research agent built with LangGraph + LLMs.",
    version="1.0.0",
)

# expose Prometheus-compatible metrics at /metrics
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# ---------- Routes ----------

@app.post("/ask", response_model=AskResponse)
async def ask_question(payload: Query):
    """
    Receives a user question, runs the LangGraph pipeline, and returns
    the synthesized answer plus source analyses and timing.
    """
    user_input = payload.question

    # Build state for pipeline (same structure as CLI)
    state = {
        "messages": [{"role": "user", "content": user_input}],
        "user_question": user_input,
        "google_results": None,
        "bing_results": None,
        "reddit_results": None,
        "selected_reddit_urls": None,
        "reddit_post_data": None,
        "google_analysis": None,
        "bing_analysis": None,
        "reddit_analysis": None,
        "final_answer": None,
    }

    start_time = time.time()
    final_state = graph.invoke(state)
    end_time = time.time()

    # Build structured response
    return AskResponse(
        question=user_input,
        final_answer=final_state.get("final_answer"),
        google_analysis=final_state.get("google_analysis"),
        bing_analysis=final_state.get("bing_analysis"),
        reddit_analysis=final_state.get("reddit_analysis"),
        selected_reddit_urls=final_state.get("selected_reddit_urls"),
        latency_ms=round((end_time - start_time) * 1000, 2),
    )


@app.get("/", tags=["meta"])
def root():
    """
    Basic welcome route.
    """
    return {
        "service": "multi-source-research-agent",
        "message": "See /docs for interactive API.",
    }


@app.get("/health", tags=["ops"])
def health_check():
    """
    Liveness / readiness probe.
    This is what you'd point monitoring / uptime checks at.
    """
    return {
        "status": "ok",
        "detail": "service is running",
    }


@app.get("/version", tags=["ops"])
def version_check():
    """
    Minimal metadata to help with debugging deployments.
    Also looks good to hiring managers.
    """
    return {
        "service": "multi-source-research-agent",
        "version": "1.0.0",
        "model_backend": "OpenAI GPT-4o via LangChain",
        "orchestrator": "LangGraph",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
