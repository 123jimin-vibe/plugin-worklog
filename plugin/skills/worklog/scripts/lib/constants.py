# @worklog s0010
"""Shared constants for worklog entity types."""

import re

ID_PREFIX_TO_TYPE = {
    "s": "spec",
    "t": "task",
    "d": "decision",
}

TYPE_TO_PREFIX = {v: k for k, v in ID_PREFIX_TO_TYPE.items()}

TYPE_TO_BUCKET = {"spec": "specs", "task": "tasks", "decision": "decisions"}

ENTITY_DIRS = list(ID_PREFIX_TO_TYPE.values())

ARCHIVE_DIRS = [
    "archive/task",
]

TASK_STATUSES = {"pending", "active", "done", "blocked", "cancelled"}

REQUIRED_FIELDS = {
    "spec": ["tags"],
    "task": ["tags", "status", "modifies"],
    "decision": ["relates_to"],
}

ID_PATTERN = re.compile(r"^([std])(\d+)$")


def parse_id(raw):
    """Parse an entity ID string into (prefix, number) or None."""
    m = ID_PATTERN.match(raw)
    if m:
        return m.group(1), int(m.group(2))
    return None


def normalize_id(raw):
    """Normalize an entity ID to canonical 4-digit zero-padded form.

    ``s1`` → ``s0001``, ``s00001`` → ``s0001``.  Returns the original
    string unchanged if it does not look like an entity ID.
    """
    parsed = parse_id(raw)
    if parsed is None:
        return raw
    prefix, num = parsed
    return f"{prefix}{num:04d}"
