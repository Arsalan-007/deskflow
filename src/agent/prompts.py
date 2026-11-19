"""Prompt + schema for the single structured extraction call per paper."""

from __future__ import annotations

from .config import ProjectConfig

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string", "description": "One-line summary of the paper's core idea."},
        "datasets": {"type": "string", "description": 'Datasets used, or the literal string "not stated".'},
        "result": {"type": "string", "description": 'Headline metric/result, or the literal string "not stated".'},
        "relevance": {"type": "string", "enum": ["High", "Medium", "Low"]},
        "confidence": {
            "type": "string",
            "enum": ["high", "low"],
            "description": "Your confidence in the relevance call above.",
        },
    },
    "required": ["summary", "datasets", "result", "relevance", "confidence"],
}

SYSTEM_TEMPLATE = """You extract structured facts from arXiv abstracts for a researcher. \
You never invent information. If the abstract does not state a field (datasets or \
result), you output exactly the string "not stated" for that field — never a plausible \
guess, never information from outside the abstract text.

Researcher's interests:
{research_interests}

Relevance rubric:
- High: {rubric_high}
- Medium: {rubric_medium}
- Low: {rubric_low}

If you are not confident in your relevance judgement, set confidence to "low" rather \
than guessing high confidence.

The summary field must contain only a one-line description of the paper's core idea — \
never the relevance label or your reasoning about relevance."""

USER_TEMPLATE = """Title: {title}

Abstract:
{abstract}"""

RETRY_SUFFIX = """

Your previous attempt failed verification for these reasons:
{errors}

Try again, correcting those specific issues. Remember: an unstated field must be \
exactly "not stated", not an invention."""


def build_extraction_prompt(
    title: str,
    abstract: str,
    config: ProjectConfig,
    retry_errors: list[str] | None = None,
) -> tuple[str, str]:
    system = SYSTEM_TEMPLATE.format(
        research_interests=config.research_interests.strip(),
        rubric_high=config.relevance_rubric.High,
        rubric_medium=config.relevance_rubric.Medium,
        rubric_low=config.relevance_rubric.Low,
    )
    user = USER_TEMPLATE.format(title=title, abstract=abstract)
    if retry_errors:
        user += RETRY_SUFFIX.format(errors="\n".join(f"- {e}" for e in retry_errors))
    return system, user
