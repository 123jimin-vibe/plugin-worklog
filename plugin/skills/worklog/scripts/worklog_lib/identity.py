"""Entity types and interoperable ID normalization."""

import re

PREFIX_TO_TYPE = {"s": "spec", "t": "task", "n": "note", "d": "decision"}
ENTITY_TYPES = (*PREFIX_TO_TYPE.values(), "ref")
ID_PATTERN = re.compile(r"([stnd])([0-9]+)\Z")


def normalize_id(value: str) -> str:
    """Normalize without integer conversion, including arbitrarily long IDs."""
    match = ID_PATTERN.fullmatch(value) if isinstance(value, str) else None
    if match is None:
        raise ValueError(f"Invalid entity ID: {value!r}")
    digits = match[2].lstrip("0") or "0"
    return match[1] + digits.zfill(4)
