from __future__ import annotations

from typing import TypedDict


class PaperState(TypedDict):
    arxiv_id: str
    title: str
    abstract: str
    link: str
    summary: str
    datasets: str
    result: str
    relevance: str
    confidence: str
    verified: bool
    verification_errors: list[str]
    retries: int
