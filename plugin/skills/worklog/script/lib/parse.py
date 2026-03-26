# @worklog s0010
"""Frontmatter parsing for worklog entities."""

import pathlib
from dataclasses import dataclass, field

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

from .constants import ID_PREFIX_TO_TYPE

@dataclass
class Entity:
    """A parsed worklog entity."""

    id: str
    title: str
    type: str
    tags: list[str]
    path: pathlib.Path
    fields: dict = field(default_factory=dict)


def parse_frontmatter(path: str | pathlib.Path) -> Entity:
    """Extract TOML frontmatter from a worklog entity file.

    Args:
        path: Filesystem path to the entity file.

    Returns:
        An Entity populated from the frontmatter.

    Raises:
        ValueError: If frontmatter fences are missing or malformed.
        KeyError: If required fields (id, title, tags) are absent.
    """
    path = pathlib.Path(path)
    text = path.read_text(encoding="utf-8")

    # Extract text between +++ fences.
    parts = text.split("+++")
    if len(parts) < 3:
        raise ValueError(f"{path}: missing or malformed +++ frontmatter fences")

    toml_text = parts[1]
    data = tomllib.loads(toml_text)

    entity_id = data.pop("id", None)
    if entity_id is None:
        raise KeyError(f"{path}: frontmatter missing required field 'id'")

    title = data.pop("title", None)
    if title is None:
        raise KeyError(f"{path}: frontmatter missing required field 'title'")

    tags = data.pop("tags", [])

    prefix = entity_id[0] if entity_id else ""
    entity_type = ID_PREFIX_TO_TYPE.get(prefix, "unknown")

    return Entity(
        id=entity_id,
        title=title,
        type=entity_type,
        tags=list(tags),
        path=path,
        fields=data,
    )
