"""Notification sender — dispatches email notifications via Celery."""

import logging
from celery import shared_task
from .templates import render_template
from .smtp import send_email

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds


@shared_task(bind=True, max_retries=MAX_RETRIES)
def send_notification(self, user_email, event_type, context):
    """Send a notification email. Retries with exponential backoff on failure."""
    try:
        subject, body = render_template(event_type, context)
        send_email(to=user_email, subject=subject, body=body)
        logger.info("Notification sent: %s -> %s", event_type, user_email)
    except Exception as exc:
        delay = BACKOFF_BASE ** self.request.retries
        logger.warning(
            "Notification failed (attempt %d/%d): %s -> %s: %s",
            self.request.retries + 1,
            MAX_RETRIES,
            event_type,
            user_email,
            exc,
        )
        raise self.retry(exc=exc, countdown=delay)
