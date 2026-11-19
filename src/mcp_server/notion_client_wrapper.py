"""Thin, typed wrapper over the Notion API. Named *_wrapper to avoid any
ambiguity with the `notion_client` pip package it imports.

Notion's API moved to a "data sources" model: a database can hold multiple
data sources, and querying/creating pages targets a data_source_id, not the
database_id directly. A plain single-source database (what this project
uses) always has exactly one data source — we resolve it once per run and
cache it, rather than looking it up on every call."""

from __future__ import annotations

import logging

from notion_client import APIResponseError, Client
from notion_client import errors as notion_errors

from .models import AddPaperResult, PaperRecord, ProcessedIds

logger = logging.getLogger(__name__)

_RELEVANCE_OPTIONS = {"High", "Medium", "Low", "Needs Review"}
_data_source_id_cache: dict[str, str] = {}


def _client(token: str) -> Client:
    return Client(auth=token)


def _data_source_id(client: Client, database_id: str) -> str:
    cached = _data_source_id_cache.get(database_id)
    if cached:
        return cached
    db = client.databases.retrieve(database_id=database_id)
    sources = db.get("data_sources") or []
    if not sources:
        raise ValueError(f"Notion database {database_id} has no data sources")
    data_source_id = sources[0]["id"]
    _data_source_id_cache[database_id] = data_source_id
    return data_source_id


def add_paper(token: str, database_id: str, record: PaperRecord) -> AddPaperResult:
    relevance = record.relevance if record.relevance in _RELEVANCE_OPTIONS else "Needs Review"
    try:
        client = _client(token)
        data_source_id = _data_source_id(client, database_id)
        client.pages.create(
            parent={"type": "data_source_id", "data_source_id": data_source_id},
            properties={
                "Title": {"title": [{"text": {"content": record.title[:2000]}}]},
                "ArxivID": {"rich_text": [{"text": {"content": record.arxiv_id}}]},
                "Link": {"url": record.link},
                "Summary": {"rich_text": [{"text": {"content": record.summary[:2000]}}]},
                "Datasets": {"rich_text": [{"text": {"content": record.datasets[:2000]}}]},
                "Result": {"rich_text": [{"text": {"content": record.result[:2000]}}]},
                "Relevance": {"select": {"name": relevance}},
                "Status": {"select": {"name": "Unread"}},
            },
        )
        return AddPaperResult(ok=True, arxiv_id=record.arxiv_id)
    except APIResponseError as e:
        logger.warning("notion add_paper failed for %s: %s", record.arxiv_id, e)
        return AddPaperResult(ok=False, arxiv_id=record.arxiv_id, error=str(e))
    except notion_errors.RequestTimeoutError as e:
        return AddPaperResult(ok=False, arxiv_id=record.arxiv_id, error=f"timeout: {e}")
    except ValueError as e:
        return AddPaperResult(ok=False, arxiv_id=record.arxiv_id, error=str(e))


def list_processed(token: str, database_id: str) -> ProcessedIds:
    ids: set[str] = set()
    try:
        client = _client(token)
        data_source_id = _data_source_id(client, database_id)
        cursor: str | None = None
        while True:
            kwargs = {"start_cursor": cursor} if cursor else {}
            page = client.data_sources.query(data_source_id=data_source_id, page_size=100, **kwargs)
            for row in page.get("results", []):
                prop = row.get("properties", {}).get("ArxivID", {})
                rich_text = prop.get("rich_text", [])
                if rich_text:
                    ids.add(rich_text[0]["text"]["content"])
            if not page.get("has_more"):
                break
            cursor = page.get("next_cursor")
        return ProcessedIds(arxiv_ids=ids)
    except APIResponseError as e:
        logger.warning("notion list_processed failed: %s", e)
        return ProcessedIds(arxiv_ids=ids, error=str(e))
    except ValueError as e:
        return ProcessedIds(arxiv_ids=ids, error=str(e))
