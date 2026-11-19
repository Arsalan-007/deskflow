"""Thin, typed wrapper over the Telegram Bot API `sendMessage` call."""

from __future__ import annotations

import logging

import httpx

from .models import TelegramResult

logger = logging.getLogger(__name__)

TELEGRAM_MAX_MESSAGE_LEN = 4096


def send(bot_token: str, chat_id: str, text: str) -> TelegramResult:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # Telegram rejects messages over 4096 chars outright; truncate defensively
    # rather than let a long digest silently fail to send.
    body = text if len(text) <= TELEGRAM_MAX_MESSAGE_LEN else text[: TELEGRAM_MAX_MESSAGE_LEN - 1] + "…"
    try:
        resp = httpx.post(
            url,
            json={"chat_id": chat_id, "text": body, "disable_web_page_preview": True},
            timeout=15.0,
        )
        data = resp.json()
        if resp.status_code >= 400 or not data.get("ok"):
            logger.warning("telegram send failed: %s", data)
            return TelegramResult(ok=False, error=data.get("description", f"HTTP {resp.status_code}"))
        return TelegramResult(ok=True)
    except httpx.HTTPError as e:
        logger.warning("telegram send failed: %s", e)
        return TelegramResult(ok=False, error=str(e))
