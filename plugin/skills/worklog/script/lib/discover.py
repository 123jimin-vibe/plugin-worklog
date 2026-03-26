# @worklog s0010
"""Entity discovery and tag loading for worklog."""

import pathlib
import re
from dataclasses import dataclass, field
from typing import Iterable

from .constants import ARCHIVE_DIRS, ENTITY_DIRS
from .parse import Entity, parse_frontmatter


@dataclass
class Tag:
    """A tag parsed from tags.md."""

    name: str
    description: str


@dataclass
class EntityStore:
    """Result of discovering entities in a worklog directory.

    ``entities`` is iterable but not necessarily indexable — callers
    that need random access should collect into their own list.
    """

    entities: Iterable[Entity] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def discover_entities(worklog_root: str | pathlib.Path) -> EntityStore:
    """Walk worklog directories and parse all entity files.

    Scans ``spec/`` (recursive), ``task/``, ``decision/``, and
    ``archive/task/``.  Parse errors are collected in ``errors``
    rather than aborting.
    """
    root = pathlib.Path(worklog_root)
    entities: list[Entity] = []
    errors: list[str] = []

    dirs_to_scan: list[tuple[pathlib.Path, bool]] = []
    for d in ENTITY_DIRS:
        p = root / d
        if p.is_dir():
            recursive = d == "spec"
            dirs_to_scan.append((p, recursive))
    for d in ARCHIVE_DIRS:
        p = root / d
        if p.is_dir():
            dirs_to_scan.append((p, False))

    for directory, recursive in dirs_to_scan:
        if recursive:
            md_files = sorted(directory.rglob("*.md"))
        else:
            md_files = sorted(directory.glob("*.md"))

        for md_file in md_files:
            try:
                entity = parse_frontmatter(md_file)
                entities.append(entity)
            except Exception as exc:
                errors.append(f"{md_file}: {exc}")

    return EntityStore(entities=entities, errors=errors)


_TAG_ROW_PATTERN = re.compile(
    r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|$"
)


def load_tags(worklog_root: str | pathlib.Path) -> list[Tag]:
    """Parse tags.md and return a list of Tag objects.

    Each row in the markdown table produces a Tag with name and
    description.  The header and separator rows are skipped.
    """
    root = pathlib.Path(worklog_root)
    tags_path = root / "tags.md"

    if not tags_path.exists():
        return []

    text = tags_path.read_text(encoding="utf-8")
    tags: list[Tag] = []

    for line in text.splitlines():
        m = _TAG_ROW_PATTERN.match(line)
        if m:
            name = m.group(1).strip()
            description = m.group(2).strip()
            tags.append(Tag(name=name, description=description))

    return tags
