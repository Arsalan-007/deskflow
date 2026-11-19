from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import httpx

from mcp_server import arxiv_client, notion_client_wrapper, telegram_client
from mcp_server.models import PaperRecord

ATOM_SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <id>http://arxiv.org/abs/2504.16109v1</id>
    <title>TabPFN v2: Scaling Prior-Data Fitted Networks</title>
    <summary>A single pretrained transformer for tabular classification.</summary>
    <published>2025-04-20T12:00:00Z</published>
    <author><name>Alice Example</name></author>
  </entry>
  <entry>
    <!-- malformed: no id, no title -->
    <summary>Garbage entry missing required fields.</summary>
    <published>2025-04-20T12:00:00Z</published>
  </entry>
</feed>"""


def test_arxiv_fetch_parses_entries_and_skips_malformed():
    fake_resp = MagicMock()
    fake_resp.text = ATOM_SAMPLE
    fake_resp.raise_for_status = MagicMock()
    with patch("httpx.get", return_value=fake_resp):
        result = arxiv_client.fetch(["tabular deep learning"], since=datetime(2025, 1, 1, tzinfo=UTC))
    assert result.error is None
    assert len(result.papers) == 1
    assert result.papers[0].arxiv_id == "2504.16109"
    assert result.papers[0].topics == ["tabular deep learning"]


def test_arxiv_fetch_filters_by_since():
    fake_resp = MagicMock()
    fake_resp.text = ATOM_SAMPLE
    fake_resp.raise_for_status = MagicMock()
    with patch("httpx.get", return_value=fake_resp):
        result = arxiv_client.fetch(["tabular deep learning"], since=datetime(2026, 1, 1, tzinfo=UTC))
    assert result.papers == []


def test_arxiv_fetch_http_error_returns_typed_error_not_raise():
    with patch("httpx.get", side_effect=httpx.ConnectError("boom")):
        result = arxiv_client.fetch(["x"], since=datetime(2020, 1, 1, tzinfo=UTC))
    assert result.error is not None
    assert result.papers == []


def test_notion_add_paper_handles_4xx_gracefully():
    from notion_client import APIResponseError

    notion_client_wrapper._data_source_id_cache.clear()
    fake_client = MagicMock()
    fake_client.databases.retrieve.return_value = {"data_sources": [{"id": "ds1"}]}
    fake_client.pages.create.side_effect = APIResponseError(
        code="object_not_found",
        status=400,
        message="database not found",
        headers=httpx.Headers(),
        raw_body_text="",
    )
    record = PaperRecord(
        arxiv_id="1", title="t", link="l", summary="s", datasets="not stated", result="not stated", relevance="High"
    )
    with patch.object(notion_client_wrapper, "_client", return_value=fake_client):
        result = notion_client_wrapper.add_paper("tok", "db", record)
    assert result.ok is False
    assert result.error is not None


def test_notion_add_paper_no_data_sources_reports_typed_error():
    notion_client_wrapper._data_source_id_cache.clear()
    fake_client = MagicMock()
    fake_client.databases.retrieve.return_value = {"data_sources": []}
    record = PaperRecord(
        arxiv_id="2", title="t", link="l", summary="s", datasets="not stated", result="not stated", relevance="High"
    )
    with patch.object(notion_client_wrapper, "_client", return_value=fake_client):
        result = notion_client_wrapper.add_paper("tok", "db-empty", record)
    assert result.ok is False
    assert "no data sources" in result.error


def test_telegram_send_success():
    fake_resp = MagicMock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = {"ok": True}
    with patch("httpx.post", return_value=fake_resp):
        result = telegram_client.send("tok", "chat", "hello")
    assert result.ok is True


def test_telegram_send_api_error_returns_typed_error():
    fake_resp = MagicMock()
    fake_resp.status_code = 400
    fake_resp.json.return_value = {"ok": False, "description": "chat not found"}
    with patch("httpx.post", return_value=fake_resp):
        result = telegram_client.send("tok", "badchat", "hello")
    assert result.ok is False
    assert "chat not found" in result.error


def test_telegram_send_truncates_long_message():
    fake_resp = MagicMock()
    fake_resp.status_code = 200
    fake_resp.json.return_value = {"ok": True}
    captured = {}

    def fake_post(url, json, timeout):
        captured["text"] = json["text"]
        return fake_resp

    with patch("httpx.post", side_effect=fake_post):
        telegram_client.send("tok", "chat", "x" * 5000)
    assert len(captured["text"]) == telegram_client.TELEGRAM_MAX_MESSAGE_LEN
