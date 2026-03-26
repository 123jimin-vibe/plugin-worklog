# @worklog s0010
"""Shared constants for worklog entity types."""

ID_PREFIX_TO_TYPE = {
    "s": "spec",
    "t": "task",
    "d": "decision",
}

ENTITY_DIRS = list(ID_PREFIX_TO_TYPE.values())

ARCHIVE_DIRS = [
    "archive/task",
]
