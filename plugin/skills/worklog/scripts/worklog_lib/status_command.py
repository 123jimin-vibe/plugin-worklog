"""Read-only orientation over an explicitly selected relationship working set."""

import fnmatch
import re
from collections import defaultdict
from pathlib import Path

from .context import RESOLVED, find_cycle, relation_ids
from .identity import normalize_id
from .markers import markers
from .tags import normalize_tag
from .task_command import unresolved


def path_key(path, kind):
    if kind == "ref":
        return str(path)
    match = re.match(r"([stnd][0-9]+)\b", path.name)
    return normalize_id(match[1]) if match else str(path)


def run_status(context, args):
    messages, errors = [], []
    global_scope = not args.entities and not args.path
    requested_paths = []
    for raw in args.path or []:
        try:
            path = Path(raw)
            full = (context.project / path).resolve()
            requested_paths.append(full.relative_to(context.project).as_posix())
        except ValueError:
            errors.append(f"{raw}: path is outside project")

    # Reverse relationship discovery needs metadata, but not reference contents.
    refs_only = not args.entities and requested_paths and all(
        raw == "worklog/ref" or raw.startswith("worklog/ref/") for raw in requested_paths)
    kinds = () if refs_only else ("spec", "task", "note", "decision")
    entities, scan_errors = context.scan(kinds, metadata=True)
    if global_scope:
        references, reference_errors = context.scan(("ref",), metadata=True)
        entities.extend(references)
        scan_errors.extend(reference_errors)
        errors.extend(scan_errors)

    by_key = {path_key(entity.path, entity.type): entity for entity in entities}
    adjacent, children, governed_by = defaultdict(set), defaultdict(list), defaultdict(list)
    problems = defaultdict(list)
    relation_edges = {"parent": {}, "blocked_by": {}}
    for key, entity in by_key.items():
        if entity.type == "ref" and "parent" in entity.fields:
            problems[key].append(f"{key}: references do not participate in entity hierarchy")
        for field in ("parent", "blocked_by", "modifies"):
            try:
                refs = relation_ids(entity, field)
                if refs and ((field == "parent" and entity.type not in ("spec", "task", "note")) or
                             (field in ("blocked_by", "modifies") and entity.type != "task")):
                    raise ValueError(f"{key}: {field} is unavailable for {entity.type}")
                if field in relation_edges:
                    relation_edges[field][key] = refs
                for ref in refs:
                    expected = "s" if field == "modifies" else "t" if field == "blocked_by" else key[0]
                    if ref[0] != expected:
                        raise ValueError(f"{key}: invalid {field} reference {ref}")
                    adjacent[key].add(ref)
                    adjacent[ref].add(key)
                    if field == "parent":
                        children[ref].append(key)
                    if field == "modifies":
                        governed_by[ref].append(key)
            except ValueError as exc:
                problems[key].append(str(exc))

    selected = set()
    for raw in args.entities:
        try:
            selected.add(context.resolve(raw).id)
        except ValueError as exc:
            errors.append(str(exc))
    for raw in requested_paths:
        # Filenames can select a malformed record too; its error is then relevant.
        path_kinds = ("ref",) if raw == "worklog/ref" or raw.startswith("worklog/ref/") else kinds
        if raw in ("worklog", "."):
            path_kinds = (*kinds, "ref")
        for kind in path_kinds:
            entries, listing_errors = context.catalog(kind)
            for path, _, old in entries:
                relative = path.relative_to(context.project).as_posix()
                if raw == relative or relative.startswith(raw.rstrip("/") + "/") or raw == ".":
                    try:
                        entity = context.load(path, kind, old, metadata=True)
                        key = path_key(path, kind)
                        by_key[key] = entity
                        selected.add(key)
                    except ValueError as exc:
                        errors.append(str(exc))
            if raw == f"worklog/{kind}" or raw == "worklog":
                errors.extend(listing_errors)
        if not raw.startswith("worklog/") and not refs_only:
            for key, entity in by_key.items():
                if entity.type != "spec":
                    continue
                patterns = entity.fields.get("paths", [])
                if not isinstance(patterns, list) or any(not isinstance(p, str) for p in patterns):
                    problems[key].append(f"{key}: paths must be an array of strings")
                    continue
                if any(fnmatch.fnmatchcase(raw, pattern) or pattern.startswith(raw.rstrip("/") + "/") for pattern in patterns):
                    selected.add(key)
    if global_scope:
        selected = {key for key, entity in by_key.items() if not entity.archived}
    todo = list(selected)
    while todo:
        for ref in adjacent[todo.pop()]:
            if ref not in selected:
                selected.add(ref)
                todo.append(ref)
    for relation, edges in relation_edges.items():
        cyclic = find_cycle({key: refs for key, refs in edges.items() if key in selected})
        if cyclic:
            errors.append(f"{relation} cycle: " + " -> ".join(cyclic))

    messages.append(f"Project: {context.project}; declared state for orientation, not certification.")
    selected_tags = set()
    for key in sorted(selected):
        errors.extend(problems[key])
        try:
            candidate = by_key.get(key)
            if candidate is not None and candidate.type == "ref":
                entity = context.load(candidate.path, "ref")
            else:
                entity = context.resolve(key)
            messages.append(f"{key}: {entity.fields['title']} [{entity.type}" + (", archived/history" if entity.archived else "") + "]")
            messages.append(f"  Path: {entity.path.relative_to(context.project)}")
            messages.append("  " + context.mode_message(entity))
            for field in ("parent", "blocked_by", "modifies"):
                refs = relation_ids(entity, field)
                if refs:
                    if ((field == "parent" and entity.type not in ("spec", "task", "note")) or
                            (field in ("blocked_by", "modifies") and entity.type != "task")):
                        raise ValueError(f"{key}: {field} is unavailable for {entity.type}")
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
            normalized = [normalize_tag(tag) for tag in entity.tags]
            if len(normalized) != len(set(normalized)):
                raise ValueError(f"{key}: duplicate normalized entity tags")
            selected_tags.update(normalized)
            patterns = entity.fields.get("paths", [])
            if entity.type == "spec" and (not isinstance(patterns, list) or any(not isinstance(p, str) for p in patterns)):
                raise ValueError(f"{key}: paths must be an array of strings")
        except ValueError as exc:
            errors.append(str(exc))
    try:
        if global_scope:
            if context.tag_error:
                errors.append(context.tag_error)
            elif context.database is None:
                messages.append("Tag database missing (informational).")
            else:
                refs = context.tag_references()
                messages.extend(context.tag_advice(refs.keys()))
                messages.extend(f"Unused tag (advisory): {name}" for name in sorted(context.database.keys() - refs.keys()))
        else:
            messages.extend(context.tag_advice(selected_tags))
    except ValueError as exc:
        errors.append(str(exc))
    messages.append("No worklog changes.")
    return messages, list(dict.fromkeys(errors))
