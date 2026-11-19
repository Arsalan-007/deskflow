"""Entry point for one full digest run. Invoked by GitHub Actions (on the
weekly schedule, or on-demand via workflow_dispatch from the dashboard) — no
persistent server: this process starts, does the work, and exits.

    python -m agent.run_digest
"""

from __future__ import annotations

import asyncio
import logging
import sys
from datetime import UTC, datetime, timedelta

from mcp_server.models import Paper, PaperRecord

from .config import project_config
from .llm import Generator, get_generator
from .mcp_client import DeskflowMCPClient
from .prompts import EXTRACTION_SCHEMA, build_extraction_prompt
from .state import PaperState
from .verify import final_relevance, verify_extraction

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

MAX_RETRIES = 2
RELEVANCE_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Needs Review": 3}


def _init_state(paper: Paper) -> PaperState:
    return PaperState(
        arxiv_id=paper.arxiv_id,
        title=paper.title,
        abstract=paper.abstract,
        link=paper.link,
        summary="",
        datasets="",
        result="",
        relevance="",
        confidence="",
        verified=False,
        verification_errors=[],
        retries=0,
    )


def extract_and_verify(generator: Generator, paper: Paper) -> PaperState:
    """One paper through extract -> verify -> bounded retry."""
    state = _init_state(paper)
    retry_errors: list[str] | None = None
    extraction: dict = {}

    while True:
        system, user = build_extraction_prompt(state["title"], state["abstract"], project_config, retry_errors)
        try:
            extraction = generator.complete_json(system, user, EXTRACTION_SCHEMA)
        except Exception:
            logger.warning("extraction call failed for %s", state["arxiv_id"], exc_info=True)
            extraction = {}

        verified, errors = verify_extraction(state["abstract"], extraction)
        state["summary"] = extraction.get("summary") or ""
        state["datasets"] = extraction.get("datasets") or ""
        state["result"] = extraction.get("result") or ""
        state["relevance"] = extraction.get("relevance") or ""
        state["confidence"] = extraction.get("confidence") or ""
        state["verified"] = verified
        state["verification_errors"] = errors

        if verified or state["retries"] >= MAX_RETRIES:
            break
        state["retries"] += 1
        retry_errors = errors

    state["relevance"] = final_relevance(extraction) if state["verified"] else "Needs Review"
    return state


def _format_digest(papers: list[Paper], states: dict[str, PaperState]) -> str:
    by_topic: dict[str, list[Paper]] = {}
    for p in papers:
        topic = p.topics[0] if p.topics else "other"
        by_topic.setdefault(topic, []).append(p)

    lines = [f"📚 DeskFlow digest — {len(papers)} new paper(s)\n"]
    for topic, group in by_topic.items():
        lines.append(f"\n*{topic}*")
        ranked = sorted(group, key=lambda p: RELEVANCE_ORDER.get(states[p.arxiv_id]["relevance"], 9))
        for p in ranked:
            s = states[p.arxiv_id]
            lines.append(f"[{s['relevance']}] {p.title}\n{s['summary']}\n{p.link}")
    return "\n".join(lines)


async def run() -> None:
    generator = get_generator()
    since = datetime.now(UTC) - timedelta(days=project_config.lookback_days)

    async with DeskflowMCPClient() as client:
        processed = await client.notion_list_processed()
        if processed.error:
            logger.warning("notion_list_processed error: %s", processed.error)

        fetched = await client.arxiv_fetch(project_config.topics, since)
        if fetched.error:
            logger.warning("arxiv_fetch error: %s", fetched.error)

        new_papers = [p for p in fetched.papers if p.arxiv_id not in processed.arxiv_ids]
        logger.info("fetched %d papers, %d new", len(fetched.papers), len(new_papers))

        states: dict[str, PaperState] = {}
        for paper in new_papers:
            state = extract_and_verify(generator, paper)
            states[paper.arxiv_id] = state
            record = PaperRecord(
                arxiv_id=paper.arxiv_id,
                title=paper.title,
                link=paper.link,
                summary=state["summary"],
                datasets=state["datasets"],
                result=state["result"],
                relevance=state["relevance"],
            )
            added = await client.notion_add_paper(record)
            if not added.ok:
                logger.warning("notion_add_paper failed for %s: %s", paper.arxiv_id, added.error)

        if not new_papers:
            logger.info("no new papers this run; skipping Telegram send")
            return

        digest = _format_digest(new_papers, states)
        sent = await client.telegram_send(digest)
        if not sent.ok:
            logger.error("telegram_send failed: %s", sent.error)
            sys.exit(1)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
