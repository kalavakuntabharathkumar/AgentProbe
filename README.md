# AgentProbe — AI Agent Evaluation Library

AgentProbe is a small, extensible evaluation harness for comparing AI-agent outputs against expected outcomes. It includes a FastAPI service, deterministic local metrics, optional MongoDB trace persistence, and an optional Qdrant retrieval adapter.

> **Honest portfolio note:** this starter project does not claim PyPI publication, 340 stars, 2,100 downloads, external contributors, 1.5 million traces, 38% savings, or any benchmark accuracy. Those figures must only be used if you actually measure and verify them.

## Features
- Score individual agent runs using exact-match, required-key, and latency metrics.
- Store evaluation traces in MongoDB when `MONGODB_URI` is configured.
- Optional Qdrant vector search adapter for retrieving similar trace IDs.
- Optional OpenAI and Anthropic adapters; API keys are only required when calling those providers.
- FastAPI endpoints for health, evaluating a run, and listing recent evaluations.
- Pytest suite for deterministic behavior.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
uvicorn agentprobe.api:app --reload
```
Windows PowerShell activation: `.venv\\Scripts\\Activate.ps1`.

Open `http://127.0.0.1:8000/docs`.

## Evaluate a run
```bash
curl -X POST http://127.0.0.1:8000/evaluations \
  -H 'Content-Type: application/json' \
  -d '{
    "agent_name": "support-triage",
    "input": {"message": "I was charged twice"},
    "output": {"category": "billing", "priority": "high"},
    "expected": {"category": "billing"},
    "latency_ms": 240
  }'
```

## Optional environment
Copy `.env.example` to `.env` and configure only the services you want to use. The API works without MongoDB or Qdrant; in-memory storage is used for local development.

## Project layout
- `agentprobe/evaluator.py`: deterministic metrics and result schema
- `agentprobe/store.py`: in-memory/MongoDB persistence abstraction
- `agentprobe/retrieval.py`: optional Qdrant similarity-search adapter
- `agentprobe/providers.py`: OpenAI and Anthropic wrappers
- `agentprobe/api.py`: HTTP endpoints
- `agentprobe/cli.py`: evaluate a JSON file from the command line
- `tests/`: deterministic unit and API tests

## Production hardening ideas
Add dataset versioning, blind evaluation sets, rubric-based model judges, prompt-injection tests, retries/backoff, PII redaction, provider cost accounting, async trace writes, access controls, and reproducible deployment configuration before using real support data.
