"""Thin, typed wrapper over the public arXiv Atom API. No API key needed."""

from __future__ import annotations

import logging
from datetime import datetime
from xml.etree import ElementTree

import httpx

from .models import FetchResult, Paper

logger = logging.getLogger(__name__)

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
MAX_RESULTS_PER_TOPIC = 50


def _build_search_query(topic: str) -> str:
    # Quote multi-word topics so arXiv treats them as a phrase, not an OR of terms.
    phrase = topic.strip().replace('"', "")
    return f'all:"{phrase}"' if " " in phrase else f"all:{phrase}"


def _parse_entry(entry: ElementTree.Element, topic: str) -> Paper | None:
    try:
        raw_id = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
        # raw_id looks like http://arxiv.org/abs/2504.16109v1
        arxiv_id = raw_id.rsplit("/", 1)[-1].split("v")[0]
        title = (entry.findtext("atom:title", default="", namespaces=ATOM_NS) or "").strip()
        abstract = (entry.findtext("atom:summary", default="", namespaces=ATOM_NS) or "").strip()
        published_raw = entry.findtext("atom:published", default="", namespaces=ATOM_NS)
        if not (arxiv_id and title and published_raw):
            return None
        published = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
        authors = [
            (a.findtext("atom:name", default="", namespaces=ATOM_NS) or "").strip()
            for a in entry.findall("atom:author", ATOM_NS)
        ]
        return Paper(
            arxiv_id=arxiv_id,
            title=title,
            abstract=abstract,
            link=raw_id,
            published=published,
            authors=[a for a in authors if a],
            topics=[topic],
        )
    except (ValueError, KeyError):
        logger.warning("arxiv: skipping malformed entry", exc_info=True)
        return None


def fetch(topics: list[str], since: datetime) -> FetchResult:
    """Fetch recent papers for each topic, sorted newest-first, filtered to
    published >= since. Deduplicated across topics by arxiv_id."""
    seen: dict[str, Paper] = {}
    for topic in topics:
        params = {
            "search_query": _build_search_query(topic),
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "max_results": str(MAX_RESULTS_PER_TOPIC),
        }
        try:
            resp = httpx.get(ARXIV_API_URL, params=params, timeout=30.0)
            resp.raise_for_status()
        except httpx.HTTPError as e:
            return FetchResult(papers=list(seen.values()), error=f"arxiv fetch failed for '{topic}': {e}")

        try:
            root = ElementTree.fromstring(resp.text)
        except ElementTree.ParseError as e:
            return FetchResult(papers=list(seen.values()), error=f"arxiv response unparseable for '{topic}': {e}")

        for entry in root.findall("atom:entry", ATOM_NS):
            paper = _parse_entry(entry, topic)
            if paper is None or paper.published < since:
                continue
            if paper.arxiv_id in seen:
                # Same paper matched a different topic query too — keep both.
                seen[paper.arxiv_id].topics.append(topic)
            else:
                seen[paper.arxiv_id] = paper

    return FetchResult(papers=list(seen.values()))
