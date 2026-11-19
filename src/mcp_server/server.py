"""The DeskFlow MCP server. Standalone and self-contained: it only needs the
four secrets below (from .env), nothing from `agent/` — the agent is a
*client* of this server, not the other way around.

Run directly for Inspector testing:
    npx @modelcontextprotocol/inspector python -m mcp_server.server
"""

from __future__ import annotations

import os
from datetime import datetime

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer

from . import arxiv_client, notion_client_wrapper, telegram_client
from .models import AddPaperResult, FetchResult, PaperRecord, ProcessedIds, TelegramResult

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

mcp = MCPServer("deskflow")


@mcp.tool()
def arxiv_fetch(topics: list[str], since: datetime) -> FetchResult:
    """Fetch new arXiv papers for the given topics published since `since`."""
    return arxiv_client.fetch(topics, since)


@mcp.tool()
def notion_add_paper(paper: PaperRecord) -> AddPaperResult:
    """Write one paper record as a new row in the Notion papers database."""
    if not (NOTION_TOKEN and NOTION_DATABASE_ID):
        return AddPaperResult(ok=False, arxiv_id=paper.arxiv_id, error="NOTION_TOKEN/NOTION_DATABASE_ID not configured")
    return notion_client_wrapper.add_paper(NOTION_TOKEN, NOTION_DATABASE_ID, paper)


@mcp.tool()
def notion_list_processed() -> ProcessedIds:
    """List the arXiv IDs already logged in the Notion database (for dedup)."""
    if not (NOTION_TOKEN and NOTION_DATABASE_ID):
        return ProcessedIds(error="NOTION_TOKEN/NOTION_DATABASE_ID not configured")
    return notion_client_wrapper.list_processed(NOTION_TOKEN, NOTION_DATABASE_ID)


@mcp.tool()
def telegram_send(message: str) -> TelegramResult:
    """Send a message to the configured Telegram chat."""
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return TelegramResult(ok=False, error="TELEGRAM_BOT_TOKEN/TELEGRAM_CHAT_ID not configured")
    return telegram_client.send(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)


if __name__ == "__main__":
    mcp.run()
