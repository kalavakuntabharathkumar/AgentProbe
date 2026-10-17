import os
from typing import Any


def call_openai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """Optional provider adapter; requires OPENAI_API_KEY."""
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(model=model, input=prompt)
    return response.output_text


def call_anthropic(prompt: str, model: str = "claude-3-5-haiku-latest") -> str:
    """Optional provider adapter; requires ANTHROPIC_API_KEY."""
    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if getattr(block, "type", "") == "text")
