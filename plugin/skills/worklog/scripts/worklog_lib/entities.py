"""Read entity metadata without rewriting existing documents."""

import os
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .filesystem import is_link
from .identity import ENTITY_TYPES, PREFIX_TO_TYPE, normalize_id


@dataclass
class Entity:
    path: Path
    type: str
    fields: dict
    body: str
    archived: bool = False

    @property
    def id(self) -> str | None:
        return self.fields.get("id")

    @property
    def tags(self) -> tuple[str, ...]:
        return tuple(self.fields.get("tags", ()))


@dataclass
class EntityStore:
    entities: list[Entity] = field(default_factory=list)
    by_id: dict[str, Entity] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def _closing_fence(lines: list[str]) -> int | None:
    # Only locate the boundary here; tomllib remains responsible for TOML syntax.
    # A fence-like line inside a multiline string is part of the field value.
    quote = None
    for number in range(1, len(lines)):
        line = lines[number]
        if quote is None and line.strip() == "+++":
            return number
        pos = 0
        while pos < len(line):
            char = line[pos]
            if quote is None:
                if char == "#":
                    break
                if char in ("'", '"'):
                    quote = char * 3 if line.startswith(char * 3, pos) else char
                    pos += len(quote)
                    continue
            elif quote[0] == '"' and char == "\\":
                pos += 2
                continue
            elif line.startswith(quote, pos):
                pos += len(quote)
                if len(quote) == 3:
                    # Four/five closing quotes include one/two literal quotes.
                    while pos < len(line) and line[pos] == quote[0]:
                        pos += 1
                quote = None
                continue
            pos += 1
        if quote is not None and len(quote) == 1:
            # Single-line strings cannot consume the following fence on bad input.
            quote = None
    return None


def read_entity(path: Path, entity_type: str, *, archived: bool = False) -> Entity:
    """Read fenced TOML and preserve body whitespace and unknown metadata."""
    text = path.read_bytes().decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "+++":
        raise ValueError(f"{path}: missing opening +++ frontmatter fence")
    end = _closing_fence(lines)
    if end is None:
        raise ValueError(f"{path}: missing closing +++ frontmatter fence")
    try:
        data = tomllib.loads("".join(lines[1:end]))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"{path}: invalid TOML: {exc}") from exc
    if not isinstance(data.get("title"), str):
        raise ValueError(f"{path}: title must be a string")
    if entity_type == "ref" and "id" in data:
        raise ValueError(f"{path}: references do not have entity IDs")
    if entity_type != "ref":
        identity = normalize_id(data.get("id"))
        if data["id"] != identity or PREFIX_TO_TYPE[identity[0]] != entity_type:
            raise ValueError(f"{path}: ID must be standard form for {entity_type}")
        if not re.match(re.escape(identity) + r"\b", path.name):
            raise ValueError(f"{path}: filename must start with {identity} and a word boundary")
    tags = data.get("tags", [])
    if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
        raise ValueError(f"{path}: tags must be an array of strings")
    return Entity(path, entity_type, data, "".join(lines[end + 1:]), archived)


def discover_entities(root: Path) -> EntityStore:
    """Scan current types recursively and task archives flat, collecting errors."""
    store = EntityStore()
    duplicates: set[str] = set()

    def add(path: Path, kind: str, archived: bool):
        try:
            entity = read_entity(path, kind, archived=archived)
            store.entities.append(entity)
            if entity.id is not None:
                identity = normalize_id(entity.id)
                if identity in store.by_id or identity in duplicates:
                    store.errors.append(f"{path}: duplicate entity ID {identity}")
                    store.by_id.pop(identity, None)
                    duplicates.add(identity)
                else:
                    store.by_id[identity] = entity
        except (OSError, UnicodeError, ValueError) as exc:
            store.errors.append(str(exc))

    for kind, archived in [(kind, False) for kind in ENTITY_TYPES] + [("task", True)]:
        directory = root / ("archive/task" if archived else kind)
        if not directory.exists():
            continue
        if not directory.is_dir():
            store.errors.append(f"{directory}: expected a directory")
            continue
        for current, dirs, files in os.walk(directory, onerror=lambda exc: store.errors.append(str(exc))):
            dirs.sort()
            for name in dirs[:]:
                path = Path(current) / name
                try:
                    if is_link(path):
                        store.errors.append(f"{path}: linked entity directory cannot be scanned safely")
                        dirs.remove(name)
                except OSError as exc:
                    store.errors.append(str(exc))
                    dirs.remove(name)
            if archived:
                if dirs:
                    store.errors.extend(f"{Path(current) / name}: task archive must be flat" for name in dirs)
                dirs[:] = []
            for name in sorted(files):
                if name.endswith(".md"):
                    add(Path(current) / name, kind, archived)
    return store
