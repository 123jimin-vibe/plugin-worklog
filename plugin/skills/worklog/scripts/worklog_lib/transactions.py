"""Preflighted file changes with staged writes and rollback on caught failures."""

import os
import tempfile
from pathlib import Path

from .filesystem import is_link
from .initialization import RollbackError


def commit_changes(root: Path, changes: dict[Path, bytes | None], expected=None):
    """Apply one operation; None deletes a source after its replacement is ready."""
    originals, metadata, staged, applied, directories = {}, {}, {}, [], []
    root = root.absolute()
    for path in changes:
        if not path.absolute().is_relative_to(root):
            raise ValueError(f"{path}: change escapes worklog")
        for ancestor in (path, *path.parents):
            if ancestor.exists() or ancestor.is_symlink():
                if is_link(ancestor):
                    raise ValueError(f"{ancestor}: linked mutation path")
            if ancestor == root:
                break
        originals[path] = path.read_bytes() if path.exists() else None
        if originals[path] is not None:
            metadata[path] = path.stat()
        if expected is not None and path in expected and originals[path] != expected[path]:
            raise ValueError(f"{path}: changed since preflight; retry after review")
    changes = {path: data for path, data in changes.items() if data != originals[path]}
    try:
        for path, data in changes.items():
            if data is None:
                continue
            missing = []
            parent = path.parent
            while not parent.exists():
                missing.append(parent)
                parent = parent.parent
            for directory in reversed(missing):
                directory.mkdir()
                directories.append(directory)
            fd, name = tempfile.mkstemp(prefix=".worklog-", dir=path.parent)
            staged[path] = Path(name)
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
            if originals[path] is not None:
                os.chmod(name, path.stat().st_mode)
        # Publish replacements before removals; a failed removal restores both sides.
        for path in sorted(changes, key=lambda p: changes[p] is None):
            if changes[path] is None:
                path.unlink()
            elif originals[path] is None:
                # Hard-link publication is exclusive, unlike replace on a new target.
                os.link(staged[path], path)
            else:
                os.replace(staged[path], path)
            applied.append(path)
    except BaseException as exc:
        errors = []
        for path in reversed(applied):
            try:
                if originals[path] is None:
                    path.unlink()
                else:
                    path.write_bytes(originals[path])
                    os.chmod(path, metadata[path].st_mode)
                    os.utime(path, ns=(metadata[path].st_atime_ns, metadata[path].st_mtime_ns))
            except OSError as failure:
                errors.append(f"{path}: {failure}")
        if errors:
            raise RollbackError(f"{exc}\nRollback incomplete:\n" + "\n".join(errors)) from exc
        raise
    finally:
        cleanup_errors = []
        for path in staged.values():
            try:
                path.unlink(missing_ok=True)
            except OSError as exc:
                cleanup_errors.append(f"{path}: {exc}")
        for directory in reversed(directories):
            try:
                if not any(directory.iterdir()):
                    directory.rmdir()
            except OSError as exc:
                cleanup_errors.append(f"{directory}: {exc}")
        if cleanup_errors:
            raise RollbackError("Temporary-path cleanup failed; file changes may remain:\n" + "\n".join(cleanup_errors))
