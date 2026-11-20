"""Provider-agnostic LLM calls. `complete_json` uses constrained/structured
output at the SDK level rather than asking the model to "please reply with
only JSON" and regex-parsing the result — the latter is a documented,
reproduced failure mode in langgraph-verify-agent (trailing prose containing a
stray bracket breaks a naive `\\[.*\\]` regex extraction)."""

from __future__ import annotations

import json
import time
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


class GeminiGenerator:
    # Free tier is 15 requests/minute (per the account's own rate-limit page,
    # not a guessed number). Self-pacing avoids burning the retry budget and
    # wall-clock time on 429s that are entirely predictable in advance.
    _MIN_INTERVAL_SECONDS = 4.5

    def __init__(self, model: str, api_key: str) -> None:
        from google import genai

        self._client = genai.Client(api_key=api_key)
        self._model = model
        self._last_call_at: float | None = None

    def _pace(self) -> None:
        if self._last_call_at is not None:
            elapsed = time.monotonic() - self._last_call_at
            if elapsed < self._MIN_INTERVAL_SECONDS:
                time.sleep(self._MIN_INTERVAL_SECONDS - elapsed)
        self._last_call_at = time.monotonic()

    def complete_json(self, system: str, user: str, schema: dict) -> dict:
        from google.genai import types

        self._pace()
        resp = self._client.models.generate_content(
            model=self._model,
            contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system,
                response_mime_type="application/json",
                response_json_schema=schema,
                temperature=0,
                # Without a timeout, a rate-limited/overloaded response can
                # leave the SDK's internal retry logic hanging far longer
                # than any one extraction call should reasonably take.
                http_options=types.HttpOptions(timeout=30_000),
            ),
        )
        return json.loads(resp.text)


def get_generator() -> Generator:
    provider = settings.llm_provider.lower()
    if provider == "ollama":
        return OllamaGenerator(model=settings.ollama_model, host=settings.ollama_host)
    if provider == "gemini":
        return GeminiGenerator(model=settings.gemini_model, api_key=settings.gemini_api_key)
    raise ValueError(f"Unknown LLM_PROVIDER: {provider!r} (expected 'ollama' or 'gemini')")
