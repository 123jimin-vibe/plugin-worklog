"""Read-only orientation over declared worklog state."""

import fnmatch
from collections import defaultdict
from pathlib import Path

from .context import RESOLVED, find_cycle, graph, relation_ids
from .markers import markers
from .task_command import unresolved


def run_status(context, args):
    messages, errors = [], list(context.errors)
    entities = [entity for entity in context.store.entities if entity.id is None or entity.id in context.store.by_id]
    by_key = {e.id or str(e.path): e for e in entities}
    adjacent, children, governed_by = defaultdict(set), defaultdict(list), defaultdict(list)
    for entity in entities:
        key = entity.id or str(entity.path)
        try:
            if entity.type == "ref" and "parent" in entity.fields:
                raise ValueError(f"{entity.path}: references do not participate in entity hierarchy")
            for field in ("parent", "blocked_by", "modifies"):
                for ref in relation_ids(entity, field):
                    target = context.resolve(ref)
                    expected = "spec" if field == "modifies" else "task" if field == "blocked_by" else entity.type
                    if target.type != expected:
                        raise ValueError(f"{key}: invalid {field} reference {ref}")
                    adjacent[key].add(ref)
                    adjacent[ref].add(key)
                    if field == "parent":
                        children[ref].append(key)
                    if field == "modifies":
                        governed_by[ref].append(key)
        except ValueError as exc:
            errors.append(str(exc))
    for relation in ("parent", "blocked_by"):
        edges, relation_errors = graph(context, relation)
        errors.extend(relation_errors)
        cyclic = find_cycle(edges)
        if cyclic:
            errors.append(f"{relation} cycle: " + " -> ".join(cyclic))

    selected = set()
    for raw in args.entities:
        try:
            selected.add(context.resolve(raw).id)
        except ValueError as exc:
            errors.append(str(exc))
    for raw in args.path or []:
        path = Path(raw)
        if path.is_absolute():
            try:
                raw = path.relative_to(context.project).as_posix()
            except ValueError:
                errors.append(f"{raw}: path is outside project")
                continue
        else:
            raw = path.as_posix().removeprefix("./")
        for key, entity in by_key.items():
            relative = entity.path.relative_to(context.project).as_posix()
            if raw == relative or relative.startswith(raw.rstrip("/") + "/"):
                selected.add(key)
            if entity.type == "spec":
                patterns = entity.fields.get("paths", [])
                if not isinstance(patterns, list) or any(not isinstance(p, str) for p in patterns):
                    errors.append(f"{key}: paths must be an array of strings")
                    continue
                if any(fnmatch.fnmatchcase(raw, pattern) or pattern.startswith(raw.rstrip("/") + "/") for pattern in patterns):
                    selected.add(key)
    if not args.entities and not args.path:
        selected = {key for key, entity in by_key.items() if not entity.archived}
    todo = list(selected)
    while todo:
        key = todo.pop()
        for ref in adjacent[key]:
            if ref not in selected:
                selected.add(ref)
                todo.append(ref)
    messages.append(f"Project: {context.project}; declared state for orientation, not certification.")
    for key in sorted(selected):
        entity = by_key[key]
        messages.append(f"{key}: {entity.fields['title']} [{entity.type}" + (", archived/history" if entity.archived else "") + "]")
        messages.append(f"  Path: {entity.path.relative_to(context.project)}")
        try:
            messages.append("  " + context.mode_message(entity))
            for field in ("parent", "blocked_by", "modifies"):
                refs = relation_ids(entity, field)
                if refs:
                    messages.append(f"  {field}: " + ", ".join(refs))
            if children[key]:
                messages.append("  children: " + ", ".join(sorted(children[key])))
            if governed_by[key]:
                messages.append("  governing tasks: " + ", ".join(sorted(governed_by[key])))
            if entity.type == "task":
                status = entity.fields.get("status")
                waiting = unresolved(context, entity)
                if entity.archived:
                    actions = "none; archived tasks are terminal"
                elif status == "pending":
                    actions = "block, cancel" if waiting else "start, block, cancel"
                elif status == "active":
                    actions = "block, cancel" if waiting else "block, finish (caller verification and spec write-back required), cancel"
                elif status == "blocked":
                    actions = "cancel; resolve blocker" if waiting else "resume (checked blocker required), cancel"
                elif status in RESOLVED:
                    actions = "finish" if status == "done" else "cancel"
                    actions += " (archive after close-out preflight)"
                else:
                    raise ValueError(f"{key}: invalid task status {status!r}")
                messages.append(f"  status: {status}; unresolved dependencies: {', '.join(waiting) or 'none'}")
                messages.append(f"  next: {actions}")
            for marker, line, heading in markers(entity.body):
                messages.append(f"  {marker}: body line {line}: {heading}")
        except ValueError as exc:
            errors.append(str(exc))
    if context.tag_error:
        errors.append(context.tag_error)
    elif context.database is None:
        messages.append("Tag database missing (informational).")
    else:
        messages.extend(context.tag_advice(context.refs.keys()))
        messages.extend(f"Unused tag (advisory): {name}" for name in sorted(context.database.keys() - context.refs.keys()))
    messages.append("No worklog changes.")
    return messages, list(dict.fromkeys(errors))
