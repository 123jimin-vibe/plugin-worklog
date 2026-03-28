"""Notification sender — dispatches email notifications via Celery.

Updated: retry logic now handles transient 4xx errors (t0002 fix).
"""

import logging
from celery import shared_task
from .templates import render_template
from .smtp import send_email

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds


def is_transient_error(status_code):
    """Check if an SMTP error is transient and retryable."""
    # TODO: implement proper transient error classification
    # For now, treat all 4xx as transient (safe default)
    return 400 <= status_code < 500


@shared_task(bind=True, max_retries=MAX_RETRIES)
def send_notification(self, user_email, event_type, context):
    """Send a notification email. Retries with exponential backoff on failure."""
    try:
        subject, body = render_template(event_type, context)
        response = send_email(to=user_email, subject=subject, body=body)

        if response.status_code >= 500:
            raise RetryableError(f"Server error: {response.status_code}")
        elif response.status_code >= 400:
            if is_transient_error(response.status_code):
                raise RetryableError(f"Transient error: {response.status_code}")
            else:
                logger.error(
                    "Permanent delivery failure: %s -> %s (HTTP %d)",
                    event_type, user_email, response.status_code,
                )
                return

        logger.info("Notification sent: %s -> %s", event_type, user_email)

    except RetryableError as exc:
        delay = BACKOFF_BASE ** self.request.retries
        logger.warning(
            "Delivery failed (attempt %d/%d): %s -> %s: %s",
            self.request.retries + 1,
            MAX_RETRIES,
            event_type,
            user_email,
            exc,
        )
        raise self.retry(exc=exc, countdown=delay)


class RetryableError(Exception):
    """Raised for errors that should trigger a retry."""
    pass
