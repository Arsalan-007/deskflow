"""Typed I/O for every MCP tool. Every tool returns one of these — never raises
across the MCP boundary; failures are a typed `error` field instead."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class Paper(BaseModel):
    arxiv_id: str
    title: str
    abstract: str
    link: str
    published: datetime
    authors: list[str] = []
    topics: list[str] = []


class FetchResult(BaseModel):
    papers: list[Paper] = []
    error: str | None = None


class PaperRecord(BaseModel):
    """What gets written to Notion for one paper."""

    arxiv_id: str
    title: str
    link: str
    summary: str
    datasets: str
    result: str
    relevance: str  # High | Medium | Low | Needs Review


class AddPaperResult(BaseModel):
    ok: bool
    arxiv_id: str
    error: str | None = None


class ProcessedIds(BaseModel):
    arxiv_ids: set[str] = set()
    error: str | None = None


class TelegramResult(BaseModel):
    ok: bool
    error: str | None = None
