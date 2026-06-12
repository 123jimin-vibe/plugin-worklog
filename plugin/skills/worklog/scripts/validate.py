# @worklog s0010
"""Validate all worklog entities for structural correctness."""

import argparse
import pathlib
import sys

from lib.constants import ID_PATTERN, REQUIRED_FIELDS, TASK_STATUSES
from lib.discover import discover_entities, load_tags


def _detect_blocked_by_cycles(tasks, errors):
    """Append an error for each circular blocked_by chain among *tasks*."""
    # Adjacency restricted to existing task nodes; dangling refs are reported
    # elsewhere and must not crash the traversal.
    nodes = {t.id for t in tasks}
    adj = {
        t.id: [r for r in t.fields.get("blocked_by", []) if r in nodes]
        for t in tasks
    }

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in nodes}
    path = []
    seen_cycles = set()

    def visit(u):
        color[u] = GRAY
        path.append(u)
        for v in adj.get(u, []):
            if color[v] == GRAY:
                cycle = path[path.index(v):] + [v]
                key = frozenset(cycle)
                if key not in seen_cycles:
                    seen_cycles.add(key)
                    errors.append(f"blocked_by cycle: {' -> '.join(cycle)}")
            elif color[v] == WHITE:
                visit(v)
        path.pop()
        color[u] = BLACK

    for n in sorted(nodes):
        if color[n] == WHITE:
            visit(n)


def _validate_entity(entity, known_tags, id_index, errors):
    """Run all checks on a single entity, appending to *errors*."""
    eid = entity.id
    path = entity.path

    # ID format.
    if not ID_PATTERN.match(eid):
        errors.append(f"{path}: invalid ID format '{eid}'")

    # Filename starts with ID.
    if not path.stem.startswith(eid):
        errors.append(f"{path}: filename does not start with ID '{eid}'")

    # Required fields.  id and title are already enforced by parse_frontmatter;
    # the rest live in entity.fields or entity.tags.
    for field in REQUIRED_FIELDS.get(entity.type, []):
        if field == "tags":
            if not entity.tags:
                errors.append(f"{path}: missing required field 'tags'")
        elif field not in entity.fields:
            errors.append(f"{path}: missing required field '{field}'")

    # Valid status (task-specific).
    status = entity.fields.get("status")
    if status is not None and status not in TASK_STATUSES:
        errors.append(f"{path}: invalid status '{status}'")

    # Archived tasks must be terminal (done or cancelled).
    if entity.archived and entity.type == "task" and status is not None:
        if status not in ("done", "cancelled"):
            errors.append(f"{path}: archived task has non-terminal status '{status}'")

    # Cancelled tasks require an explanation in the body.
    if entity.type == "task" and status == "cancelled" and not entity.body.strip():
        errors.append(f"{path}: cancelled task has no explanation in its body")

    # Triage priority: tasks only, non-negative integer (s0016).
    priority = entity.fields.get("priority")
    if priority is not None:
        if entity.type != "task":
            errors.append(f"{path}: priority is only valid on tasks")
        elif isinstance(priority, bool) or not isinstance(priority, int) or priority < 0:
            errors.append(
                f"{path}: invalid priority '{priority}' (must be a non-negative integer)"
            )

    # Tags exist in index.
    if known_tags is not None:
        for tag in entity.tags:
            if tag not in known_tags:
                errors.append(f"{path}: unknown tag '{tag}'")

    # Dangling references.
    for ref in entity.fields.get("modifies", []):
        if ref not in id_index:
            errors.append(f"{path}: dangling modifies ref '{ref}'")

    for ref in entity.fields.get("blocked_by", []):
        if ref not in id_index:
            errors.append(f"{path}: dangling blocked_by ref '{ref}'")

    for ref in entity.fields.get("relates_to", []):
        if ref not in id_index:
            errors.append(f"{path}: dangling relates_to ref '{ref}'")

    for ref in entity.fields.get("supersedes", []):
        if ref not in id_index:
            errors.append(f"{path}: dangling supersedes ref '{ref}'")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate worklog entities.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)
    store = discover_entities(root)
    errors = list(store.errors)

    # Build ID index for dangling-ref checks.
    all_entities = list(store.entities)
    id_index = set()
    seen_ids = {}
    for entity in all_entities:
        if entity.id in seen_ids:
            errors.append(
                f"{entity.path}: duplicate ID '{entity.id}' "
                f"(also in {seen_ids[entity.id]})"
            )
        else:
            seen_ids[entity.id] = entity.path
        id_index.add(entity.id)

    # Load known tags (None if no tags file).
    tags = load_tags(root)
    known_tags = {t.name for t in tags} if tags else None

    for entity in all_entities:
        _validate_entity(entity, known_tags, id_index, errors)

    _detect_blocked_by_cycles(store.tasks, errors)

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
