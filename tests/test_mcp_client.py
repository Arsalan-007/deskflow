"""Regression test for a real bug: mcp's stdio_client does NOT inherit the
parent process's environment by default, so secrets set only via env vars
(no .env file on disk, e.g. GitHub Actions) never reached the spawned MCP
server unless explicitly forwarded."""

import asyncio
import os
from unittest.mock import AsyncMock, patch

from agent.mcp_client import DeskflowMCPClient


def test_stdio_server_params_forward_full_environment():
    captured = {}

    def fake_stdio_server_params(**kwargs):
        captured.update(kwargs)
        return kwargs

    async def run():
        with (
            patch("agent.mcp_client.StdioServerParameters", side_effect=fake_stdio_server_params),
            patch("agent.mcp_client.stdio_client") as fake_stdio_client,
            patch("agent.mcp_client.ClientSession") as fake_session_cls,
        ):
            fake_stdio_client.return_value.__aenter__ = AsyncMock(return_value=(None, None))
            fake_stdio_client.return_value.__aexit__ = AsyncMock(return_value=False)
            fake_session = AsyncMock()
            fake_session_cls.return_value.__aenter__ = AsyncMock(return_value=fake_session)
            fake_session_cls.return_value.__aexit__ = AsyncMock(return_value=False)

            async with DeskflowMCPClient():
                pass

    asyncio.run(run())

    assert "env" in captured
    # A sentinel from this process's real environment must be present —
    # proves os.environ was actually forwarded, not just PATH/HOME.
    sentinel_key = next(iter(os.environ))
    assert captured["env"].get(sentinel_key) == os.environ[sentinel_key]
