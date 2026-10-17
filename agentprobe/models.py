from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field


class EvaluationRequest(BaseModel):
    agent_name: str = Field(min_length=1, max_length=120)
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)
    expected: dict[str, Any] = Field(default_factory=dict)
    latency_ms: float = Field(default=0, ge=0)
    tags: list[str] = Field(default_factory=list)


class EvaluationResult(BaseModel):
    evaluation_id: str
    agent_name: str
    exact_match: float
    required_key_match: float
    latency_ms: float
    passed: bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    details: dict[str, Any] = Field(default_factory=dict)
