# @worklog s0010
"""Unified priority view: open tasks and UNIMPLEMENTED spec items (s0016)."""

import argparse
import pathlib
import re

from lib.constants import normalize_id
from lib.discover import discover_entities

OPEN_STATUSES = {"pending", "active", "blocked"}

# Bare token is a marker; backticked is a mention (s0016 marker convention).
_MARKER = re.compile(r"(?<!`)\bUNIMPLEMENTED\b(?!`)")
_LIST_PREFIX = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s*")
_EXCERPT_MAX = 72


def _priority(entity):
    """Return the entity's triage priority, or None when untriaged/invalid."""
    value = entity.fields.get("priority")
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _marker_excerpt(line):
    text = _MARKER.sub("", line, count=1)
    text = _LIST_PREFIX.sub("", text)
    text = re.sub(r"\s+", " ", text).strip(" -—–:*_")
    if len(text) > _EXCERPT_MAX:
        text = text[: _EXCERPT_MAX - 1].rstrip() + "…"
    return text or "(unlabeled item)"


def _spec_markers(spec):
    return [
        _marker_excerpt(line)
        for line in spec.body.splitlines()
        if _MARKER.search(line)
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Unified priority view over open tasks and UNIMPLEMENTED spec items."
    )
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    args = parser.parse_args(argv)

    store = discover_entities(pathlib.Path(args.w))

    open_tasks = [
        t for t in store.tasks
        if not t.archived and t.fields.get("status") in OPEN_STATUSES
    ]

    covering = {}
    for task in open_tasks:
        for ref in task.fields.get("modifies", []):
            covering.setdefault(normalize_id(ref), []).append(task)

    triaged = []  # (priority, id, line)
    untriaged = []

    for task in open_tasks:
        prio = _priority(task)
        line = f"{task.id}  {task.title}  [{task.fields.get('status')}]"
        if prio is None:
            untriaged.append(line)
        else:
            triaged.append((prio, task.id, f"p{prio}  {line}"))

    for spec in store.specs:
        if spec.archived:
            continue
        markers = _spec_markers(spec)
        if not markers:
            continue
        covers = covering.get(spec.id, [])
        prios = [p for p in (_priority(t) for t in covers) if p is not None]
        for excerpt in markers:
            if prios:
                best = min(prios)
                via = ", ".join(t.id for t in covers if _priority(t) == best)
                triaged.append((best, spec.id, f"p{best}  {spec.id}  {excerpt}  (via {via})"))
            elif covers:
                ids = ", ".join(t.id for t in covers)
                untriaged.append(f"{spec.id}  {excerpt}  (tasks: {ids})")
            else:
                untriaged.append(f"{spec.id}  {excerpt}")

    if not triaged and not untriaged:
        print("(none)")
        return

    if triaged:
        triaged.sort(key=lambda item: (item[0], item[1]))
        print("Triaged:")
        for _, _, line in triaged:
            print(f"  {line}")
    if untriaged:
        if triaged:
            print()
        print("Untriaged:")
        for line in untriaged:
            print(f"  {line}")


if __name__ == "__main__":
    main()
