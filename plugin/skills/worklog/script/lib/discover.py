# @worklog s0010
"""Entity discovery and tag loading for worklog."""

import csv
import io
import pathlib
from dataclasses import dataclass, field
from typing import Iterable

from .constants import ARCHIVE_DIRS, ENTITY_DIRS
from .parse import Entity, parse_frontmatter


@dataclass
class Tag:
    """A tag parsed from tags.csv."""

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


def load_tags(worklog_root: str | pathlib.Path) -> list[Tag]:
    """Parse tags.csv and return a list of Tag objects.

    Expects a CSV file with a header row containing at least ``tag``
    and ``description`` columns.
    """
    root = pathlib.Path(worklog_root)
    tags_path = root / "tags.csv"

    if not tags_path.exists():
        return []

    text = tags_path.read_text(encoding="utf-8")
    reader = csv.DictReader(io.StringIO(text))
    tags: list[Tag] = []

    for row in reader:
        name = row.get("tag", "").strip()
        description = row.get("description", "").strip()
        if name:
            tags.append(Tag(name=name, description=description))

    return tags
