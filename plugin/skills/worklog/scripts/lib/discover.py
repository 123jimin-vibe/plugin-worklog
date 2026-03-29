# @worklog s0010
"""Entity discovery and tag loading for worklog."""

import csv
import io
import itertools
import pathlib
from dataclasses import dataclass, field

from .constants import ARCHIVE_DIRS, ENTITY_DIRS
from .parse import Entity, parse_frontmatter


@dataclass
class Tag:
    """A tag parsed from tags.csv."""

    name: str
    description: str


@dataclass
class EntityStore:
    """Result of discovering entities in a worklog directory."""

    specs: list[Entity] = field(default_factory=list)
    tasks: list[Entity] = field(default_factory=list)
    decisions: list[Entity] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def entities(self):
        """All entities across types."""
        return itertools.chain(self.specs, self.tasks, self.decisions)


def discover_entities(worklog_root: str | pathlib.Path) -> EntityStore:
    """Walk worklog directories and parse all entity files.

    Scans ``spec/`` (recursive), ``task/``, ``decision/``, and
    ``archive/task/``.  Parse errors are collected in ``errors``
    rather than aborting.
    """
    root = pathlib.Path(worklog_root)
    store = EntityStore()

    _TYPE_TO_BUCKET = {
        "spec": store.specs,
        "task": store.tasks,
        "decision": store.decisions,
    }

    dirs_to_scan: list[tuple[pathlib.Path, bool, bool]] = []
    for d in ENTITY_DIRS:
        p = root / d
        if p.is_dir():
            recursive = d == "spec"
            dirs_to_scan.append((p, recursive, False))
    for d in ARCHIVE_DIRS:
        p = root / d
        if p.is_dir():
            dirs_to_scan.append((p, False, True))

    for directory, recursive, archived in dirs_to_scan:
        if recursive:
            md_files = sorted(directory.rglob("*.md"))
        else:
            md_files = sorted(directory.glob("*.md"))

        for md_file in md_files:
            try:
                entity = parse_frontmatter(md_file)
                entity.archived = archived
                bucket = _TYPE_TO_BUCKET.get(entity.type)
                if bucket is not None:
                    bucket.append(entity)
            except Exception as exc:
                store.errors.append(f"{md_file}: {exc}")

    return store


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
