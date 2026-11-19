"""Provider-agnostic LLM calls. `complete_json` uses constrained/structured
output at the SDK level rather than asking the model to "please reply with
only JSON" and regex-parsing the result — the latter is a documented,
reproduced failure mode in langgraph-verify-agent (trailing prose containing a
stray bracket breaks a naive `\\[.*\\]` regex extraction)."""

from __future__ import annotations

import json
from typing import Protocol

from .config import settings


class Generator(Protocol):
    def complete_json(self, system: str, user: str, schema: dict) -> dict: ...


class OllamaGenerator:
    def __init__(self, model: str, host: str) -> None:
        import ollama

        self._client = ollama.Client(host=host)
        self._model = model

    def complete_json(self, system: str, user: str, schema: dict) -> dict:
        resp = self._client.chat(
            model=self._model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            format=schema,
            options={"temperature": 0},
        )
        return json.loads(resp["message"]["content"])


class AnthropicGenerator:
    def __init__(self, model: str, api_key: str) -> None:
        import anthropic

        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def complete_json(self, system: str, user: str, schema: dict) -> dict:
        # Tool-use with a single forced tool is Anthropic's structured-output
        # mechanism: the model's reply IS the validated tool input, not prose
        # to parse.
        tool_name = "emit_extraction"
        resp = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            system=system,
            messages=[{"role": "user", "content": user}],
            tools=[{"name": tool_name, "description": "Emit the structured extraction.", "input_schema": schema}],
            tool_choice={"type": "tool", "name": tool_name},
        )
        for block in resp.content:
            if block.type == "tool_use":
                return block.input
        raise RuntimeError("anthropic: model did not return a tool_use block")


def get_generator() -> Generator:
    provider = settings.llm_provider.lower()
    if provider == "ollama":
        return OllamaGenerator(model=settings.ollama_model, host=settings.ollama_host)
    if provider == "anthropic":
        return AnthropicGenerator(model=settings.anthropic_model, api_key=settings.anthropic_api_key)
    raise ValueError(f"Unknown LLM_PROVIDER: {provider!r} (expected 'ollama' or 'anthropic')")
