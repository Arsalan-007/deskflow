"""Independently re-check the model's own extraction before it's trusted.

Three lessons applied here, pulled from a diagnosed bug class in
langgraph-verify-agent's claim-verification step:
  1. An explicit "not stated" always passes grounding — abstaining is a
     correct answer, not a verification failure.
  2. (handled upstream, in llm.py) constrained/structured output instead of
     regex-extracting JSON from free text.
  3. Grounding is a token-overlap check against the abstract, not an exact
     verbatim substring match — real paraphrasing shouldn't register as
     "unsupported".
"""

from __future__ import annotations

import re

ALLOWED_RELEVANCE = {"High", "Medium", "Low"}
ALLOWED_CONFIDENCE = {"high", "low"}
NOT_STATED = "not stated"
GROUNDING_OVERLAP_THRESHOLD = 0.6

_STOPWORDS = {
    "a", "an", "the", "of", "on", "in", "to", "for", "and", "or", "is", "are",
    "with", "by", "at", "as", "its", "this", "that", "we", "our",
}


def _significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in _STOPWORDS}


def _is_grounded(phrase: str, abstract: str) -> bool:
    if phrase.strip().lower() == NOT_STATED:
        return True
    words = _significant_words(phrase)
    if not words:
        return False
    overlap = len(words & _significant_words(abstract)) / len(words)
    return overlap >= GROUNDING_OVERLAP_THRESHOLD


def verify_extraction(abstract: str, extraction: dict) -> tuple[bool, list[str]]:
    """Returns (verified, errors). Never raises on malformed input — a
    missing/wrong-typed field is just another verification error."""
    errors: list[str] = []

    relevance = extraction.get("relevance")
    if relevance not in ALLOWED_RELEVANCE:
        errors.append(f"relevance must be one of {sorted(ALLOWED_RELEVANCE)}, got {relevance!r}")

    confidence = extraction.get("confidence")
    if confidence not in ALLOWED_CONFIDENCE:
        errors.append(f"confidence must be one of {sorted(ALLOWED_CONFIDENCE)}, got {confidence!r}")

    for field in ("datasets", "result"):
        value = extraction.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} must be a non-empty string (or exactly {NOT_STATED!r})")
        elif not _is_grounded(value, abstract):
            errors.append(f"{field} ({value!r}) is not grounded in the abstract — looks invented")

    summary = extraction.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        errors.append("summary must be a non-empty string")

    return (len(errors) == 0, errors)


def final_relevance(extraction: dict) -> str:
    """Low-confidence relevance calls are flagged for human review rather
    than silently trusted at face value."""
    if extraction.get("confidence") == "low":
        return "Needs Review"
    return extraction.get("relevance", "Needs Review")
