import os
from datetime import datetime
from fastapi import FastAPI
from .evaluator import evaluate
from .models import EvaluationRequest, EvaluationResult
from .store import TraceStore

app = FastAPI(title="AgentProbe", version="0.1.0", description="AI agent evaluation starter API")
store = TraceStore(
    mongo_uri=os.getenv("MONGODB_URI") or None,
    database=os.getenv("MONGODB_DATABASE", "agentprobe"),
)


@app.get("/health")
def health():
    return {"status": "ok", "service": "agentprobe"}


@app.post("/evaluations", response_model=EvaluationResult)
def create_evaluation(request: EvaluationRequest):
    result = evaluate(request)
    record = result.model_dump(mode="json")
    store.add(record)
    return result


@app.get("/evaluations")
def list_evaluations(limit: int = 50):
    safe_limit = max(1, min(limit, 200))
    return store.recent(safe_limit)
