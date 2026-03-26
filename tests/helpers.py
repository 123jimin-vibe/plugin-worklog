# @worklog s0017
"""Shared test helpers for worklog fixture creation.

Provides functions to create temporary worklog directories and populate them
with entity files for testing.
"""

import pathlib


def make_worklog(root):
    """Create the standard worklog subdirectory structure under *root*."""
    root = pathlib.Path(root)
    for d in ["spec", "task", "decision", "archive/task"]:
        (root / d).mkdir(parents=True, exist_ok=True)


def write_entity(root, entity_id, fields, body="", subdir=None):
    """Write a worklog entity file and return its path.

    Args:
        root: Worklog root directory.
        entity_id: Entity ID like "s0001", "t0001", "d0001".
        fields: Dict of TOML frontmatter fields.
        body: Optional markdown body after the frontmatter.
        subdir: Override the subdirectory (e.g. "archive/task", "spec/entity").
            Defaults to the standard directory for the entity type.
    """
    root = pathlib.Path(root)
    prefix = entity_id[0]
    if subdir is None:
        subdir = {"s": "spec", "t": "task", "d": "decision"}[prefix]
    slug = fields.get("title", "untitled").lower().replace(" ", "-")
    filename = f"{entity_id}-{slug}.md"
    path = root / subdir / filename
    lines = ["+++"]
    for k, v in fields.items():
        if isinstance(v, list):
            lines.append(f"{k} = {v}")
        elif isinstance(v, str):
            lines.append(f'{k} = "{v}"')
    lines.append("+++")
    if body:
        lines.append("")
        lines.append(body)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)


def write_tags(root, tags):
    """Write a tags.csv file with the given tag names and return its path."""
    root = pathlib.Path(root)
    lines = ["tag,description"]
    for tag in tags:
        lines.append(f'{tag},"Test tag."')
    path = root / "tags.csv"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(path)
