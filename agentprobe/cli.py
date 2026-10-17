import argparse
import json
from pathlib import Path
from .evaluator import evaluate
from .models import EvaluationRequest


def main():
    parser = argparse.ArgumentParser(description="Evaluate one AgentProbe JSON fixture")
    parser.add_argument("fixture", type=Path, help="JSON file containing agent_name/output/expected")
    args = parser.parse_args()
    request = EvaluationRequest.model_validate_json(args.fixture.read_text())
    print(json.dumps(evaluate(request).model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    main()
