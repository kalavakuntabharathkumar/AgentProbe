from agentprobe.evaluator import evaluate
from agentprobe.models import EvaluationRequest


def test_all_expected_keys_match():
    result = evaluate(EvaluationRequest(
        agent_name="triage",
        output={"category": "billing", "priority": "high"},
        expected={"category": "billing"},
        latency_ms=100,
    ))
    assert result.passed is True
    assert result.required_key_match == 1.0
    assert result.exact_match == 1.0


def test_mismatch_fails():
    result = evaluate(EvaluationRequest(
        agent_name="triage",
        output={"category": "technical"},
        expected={"category": "billing"},
    ))
    assert result.passed is False
    assert result.required_key_match == 0.0


def test_empty_expected_is_not_a_pass():
    result = evaluate(EvaluationRequest(agent_name="empty"))
    assert result.passed is False
    assert result.required_key_match == 0.0
