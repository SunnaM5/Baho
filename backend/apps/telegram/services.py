from __future__ import annotations

import logging
from typing import Any
import requests
from django.conf import settings
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(requests.RequestException,),
    retry_kwargs={"max_retries": 5},
    retry_backoff=True,
    retry_backoff_max=300
)
def send_telegram_message_task(self, text: str, photo_url: str | None = None) -> bool:
    """
    Asynchronous Celery task for Telegram notification delivery with exponential backoff.
    Gracefully handles missing credentials, invalid URLs, and network drops without breaking orders.
    """
    bot_token = getattr(settings, "TELEGRAM_BOT_TOKEN", None) or getattr(settings, "BOT_TOKEN", None) or getattr(settings, "TELEGRAM_TOKEN", None)
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", None) or getattr(settings, "CHAT_ID", None)

    if not bot_token or not chat_id:
        logger.warning("Telegram Bot Token or Chat ID not configured in environment settings.")
        return False

    try:
        if photo_url and photo_url.startswith("http"):
            url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
            payload = {
                "chat_id": chat_id,
                "photo": photo_url,
                "caption": text,
                "parse_mode": "HTML",
            }
        else:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            }

        response = requests.post(url, json=payload, timeout=10)
        
        # If sending photo failed (e.g. invalid photo URL or unreachable localhost image), fallback to text message
        if response.status_code != 200 and photo_url:
            logger.warning(f"Telegram sendPhoto failed with status {response.status_code}. Retrying text message fallback.")
            fallback_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            fallback_payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
            }
            response = requests.post(fallback_url, json=fallback_payload, timeout=10)

        response.raise_for_status()
        logger.info(f"Telegram notification sent successfully to chat {chat_id}")
        return True

    except requests.RequestException as exc:
        logger.error(f"Failed to send Telegram notification: {exc}")
        raise exc
