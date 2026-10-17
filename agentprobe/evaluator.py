from uuid import uuid4
from .models import EvaluationRequest, EvaluationResult


def evaluate(request: EvaluationRequest) -> EvaluationResult:
    """Compute transparent, deterministic checks; no LLM judge is implied."""
    expected = request.expected
    output = request.output
    if expected:
        matches = sum(output.get(key) == value for key, value in expected.items())
        exact_match = float(matches == len(expected))
        required_key_match = matches / len(expected)
    else:
        exact_match = 0.0
        required_key_match = 0.0

    return EvaluationResult(
        evaluation_id=str(uuid4()),
        agent_name=request.agent_name,
        exact_match=exact_match,
        required_key_match=round(required_key_match, 4),
        latency_ms=request.latency_ms,
        passed=bool(expected) and required_key_match == 1.0,
        details={
            "expected_keys": list(expected.keys()),
            "matched_keys": [key for key, value in expected.items() if output.get(key) == value],
            "missing_or_mismatched_keys": [
                key for key, value in expected.items() if output.get(key) != value
            ],
            "tags": request.tags,
        },
    )
