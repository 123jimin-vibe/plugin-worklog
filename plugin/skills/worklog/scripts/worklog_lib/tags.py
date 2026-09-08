"""Tag identity and lossless CSV description handling."""

import csv
import io
from pathlib import Path


def normalize_tag(value: str) -> str:
    if not isinstance(value, str) or not (name := value.strip().casefold()):
        raise ValueError("tag name must be a non-empty string after normalization")
    return name


def read_tags(path: Path, *, raw: bytes | None = None) -> dict[str, str]:
    """Read a database once, or parse bytes retained by its mutation caller."""
    tags = {}
    try:
        stream = io.StringIO((path.read_bytes() if raw is None else raw).decode("utf-8"), newline="")
        rows = csv.reader(stream, strict=True)
        if next(rows, None) != ["tag", "description"]:
            raise ValueError("expected exactly the columns tag,description")
        for row in rows:
            if len(row) != 2:
                raise ValueError(f"CSV line {rows.line_num}: expected two columns")
            name = normalize_tag(row[0])
            if name in tags:
                raise ValueError(f"CSV line {rows.line_num}: duplicate normalized tag {name!r}")
            tags[name] = row[1]
    except (ValueError, csv.Error) as exc:
        raise ValueError(f"{path}: {exc}") from exc
    return tags


def render_tags(tags: dict[str, str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(["tag", "description"])
    for name in sorted(tags):
        writer.writerow([name, tags[name]])
    return stream.getvalue().encode("utf-8")
