from fastapi.testclient import TestClient
from agentprobe.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_list_evaluation():
    response = client.post("/evaluations", json={
        "agent_name": "support",
        "output": {"category": "billing"},
        "expected": {"category": "billing"},
        "latency_ms": 80,
    })
    assert response.status_code == 200
    assert response.json()["passed"] is True
    assert client.get("/evaluations?limit=10").status_code == 200
