"""Preflight and create only the missing worklog structure."""

import stat
from dataclasses import dataclass
from pathlib import Path

from .configuration import default_configuration, read_configuration
from .entities import discover_entities
from .filesystem import is_link
from .identity import ENTITY_TYPES
from .tags import normalize_tag, read_tags, render_tags


class PreflightError(ValueError):
    def __init__(self, errors: list[str]):
        super().__init__("\n".join(errors))


class RollbackError(OSError):
    """A write failed and some newly created paths could not be removed."""


@dataclass
class InitResult:
    project: Path
    message: str
    created: list[Path]
    existing: list[Path]


def _preflight_paths(root: Path) -> tuple[list[Path], list[Path], list[str]]:
    directories = [root, *(root / kind for kind in ENTITY_TYPES), root / "archive", root / "archive/task"]
    files = [root / "project.toml", root / "tags.csv"]
    missing, existing, errors, blocked = [], [], [], []
    for path in directories + files:
        if any(parent in path.parents for parent in blocked):
            continue
        try:
            info = path.lstat()
            linked = is_link(path)
        except FileNotFoundError:
            missing.append(path)
            continue
        except OSError as exc:
            errors.append(f"{path}: {exc}")
            blocked.append(path)
            continue
        # Linked required paths can redirect creation outside the worklog.
        correct_type = stat.S_ISDIR(info.st_mode) if path in directories else stat.S_ISREG(info.st_mode)
        if linked or not correct_type:
            expected = "directory" if path in directories else "regular file"
            errors.append(f"{path}: expected an unlinked {expected}")
            blocked.append(path)
        else:
            existing.append(path)
    return missing, existing, errors


def initialize(project: Path) -> InitResult:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise PreflightError([f"{project}: project must be an existing directory"])
    root = project / "worklog"
    missing, existing, errors = _preflight_paths(root)
    if errors:
        raise PreflightError(errors)

    store = discover_entities(root)
    errors.extend(store.errors)
    names: set[str] = set()
    for entity in store.entities:
        seen: set[str] = set()
        for tag in entity.tags:
            try:
                name = normalize_tag(tag)
                if name in seen:
                    raise ValueError(f"duplicate normalized tag {name!r}")
                seen.add(name)
                names.add(name)
            except ValueError as exc:
                errors.append(f"{entity.path}: {exc}")

    for path, reader in ((root / "project.toml", read_configuration), (root / "tags.csv", read_tags)):
        if path in existing:
            try:
                reader(path)
            except (OSError, UnicodeError, ValueError) as exc:
                errors.append(f"{path}: {exc}")
    if errors:
        raise PreflightError(errors)

    contents = {
        root / "project.toml": default_configuration(),
        root / "tags.csv": render_tags(dict.fromkeys(names, "")),
    }
    created: list[Path] = []
    try:
        for path in missing:
            if path in contents:
                # Exclusive creation never overwrites a path appearing after preflight.
                with path.open("xb") as stream:
                    created.append(path)
                    stream.write(contents[path])
            else:
                path.mkdir()
                created.append(path)
    except BaseException as exc:
        cleanup_errors = []
        for path in reversed(created):
            try:
                if path in contents:
                    path.unlink()
                else:
                    path.rmdir()
            except OSError as cleanup_exc:
                cleanup_errors.append(f"{path}: {cleanup_exc}")
        if cleanup_errors:
            raise RollbackError(f"{exc}\nCould not remove newly created paths:\n" + "\n".join(cleanup_errors)) from exc
        raise

    message = "Worklog already initialized."
    if created:
        message = "Worklog initialized." if root in created else "Worklog structure completed."
    return InitResult(project, message, created, existing)
