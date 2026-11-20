"""The agent talks to the MCP server as a real MCP client over stdio — not a
direct Python import — since demonstrating that integration path is the
point of this project."""

from __future__ import annotations

import json
import os
import sys
from contextlib import AsyncExitStack
from datetime import datetime

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_server.models import AddPaperResult, FetchResult, PaperRecord, ProcessedIds, TelegramResult


class DeskflowMCPClient:
    """Spawns the DeskFlow MCP server as a subprocess for the lifetime of one
    `async with` block and exposes its tools as typed async methods."""

    def __init__(self) -> None:
        self._stack = AsyncExitStack()
        self._session: ClientSession | None = None

    async def __aenter__(self) -> DeskflowMCPClient:
        # mcp's stdio_client does NOT inherit the parent's full environment
        # by default (only a safe allowlist like PATH/HOME) — this is the
        # same trust boundary as our own subprocess, not a third-party MCP
        # server, so explicitly forwarding os.environ is correct here. Without
        # it, the spawned server never sees NOTION_TOKEN etc. in environments
        # with no .env file on disk (e.g. GitHub Actions).
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_server.server"],
            env=dict(os.environ),
        )
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self._stack.aclose()

    async def _call(self, name: str, arguments: dict) -> dict:
        if self._session is None:
            raise RuntimeError("DeskflowMCPClient used outside `async with`")
        result = await self._session.call_tool(name, arguments=arguments)
        if result.is_error:
            text = result.content[0].text if result.content else "unknown MCP error"
            raise RuntimeError(f"MCP tool {name!r} failed: {text}")
        # shortcut: structured_content isn't guaranteed on every MCP SDK
        # version, so fall back to parsing the text content as JSON.
        if getattr(result, "structured_content", None):
            return result.structured_content
        return json.loads(result.content[0].text)

    async def arxiv_fetch(self, topics: list[str], since: datetime) -> FetchResult:
        raw = await self._call("arxiv_fetch", {"topics": topics, "since": since.isoformat()})
        return FetchResult.model_validate(raw)

    async def notion_add_paper(self, paper: PaperRecord) -> AddPaperResult:
        raw = await self._call("notion_add_paper", {"paper": paper.model_dump(mode="json")})
        return AddPaperResult.model_validate(raw)

    async def notion_list_processed(self) -> ProcessedIds:
        raw = await self._call("notion_list_processed", {})
        return ProcessedIds.model_validate(raw)

    async def telegram_send(self, message: str) -> TelegramResult:
        raw = await self._call("telegram_send", {"message": message})
        return TelegramResult.model_validate(raw)
