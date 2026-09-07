"""Create entities and edit supported fields with independent target outcomes."""

import re

from .context import find_cycle, graph, reachable
from .editing import edit_fields, encode_value
from .entities import Entity
from .identity import normalize_id
from .initialization import RollbackError
from .tags import normalize_tag
from .transactions import commit_changes

FIELDS = {
    "title": ("scalar", {"spec", "task", "note"}, True),
    "tags": ("list", {"spec", "task", "note"}, False),
    "parent": ("scalar", {"spec", "task", "note"}, False),
    "paths": ("list", {"spec"}, False),
    "modifies": ("list", {"task"}, True),
    "blocked_by": ("list", {"task"}, False),
}


def field_values(context, kind, name, values):
    if not isinstance(values, list):
        raise ValueError(f"{name}: an array of values is required")
    if name not in FIELDS or kind not in FIELDS[name][1]:
        raise ValueError(f"{name}: field is unavailable for {kind}; id, status and agent_mode are protected")
    cardinality = FIELDS[name][0]
    if cardinality == "scalar" and len(values) != 1:
        raise ValueError(f"{name}: exactly one value required")
    if any(not isinstance(value, str) for value in values):
        raise ValueError(f"{name}: string values required")
    if name == "title" and not values[0].strip():
        raise ValueError("title must not be empty")
    if name == "tags":
        values = [normalize_tag(value) for value in values]
    if name in ("parent", "modifies", "blocked_by"):
        values = [normalize_id(value) for value in values]
        expected = kind if name == "parent" else "spec" if name == "modifies" else "task"
        for value in values:
            if context.resolve(value).type != expected:
                raise ValueError(f"{name}: {value} must be a {expected}")
    if len(values) != len(set(values)):
        raise ValueError(f"{name}: duplicate values")
    return values[0] if cardinality == "scalar" else values


def next_identity(context, kind):
    prefix = {"spec": "s", "task": "t", "note": "n"}[kind]
    digits = [identity[1:].lstrip("0") or "0" for identity in context.store.by_id if identity.startswith(prefix)]
    return increment_identity(prefix + (max(digits, key=lambda value: (len(value), value)) if digits else "0"))


def increment_identity(identity):
    prefix, number = identity[0], list(identity[1:])
    pos = len(number) - 1
    while pos >= 0 and number[pos] == "9":
        number[pos] = "0"
        pos -= 1
    if pos < 0:
        number.insert(0, "1")
    else:
        number[pos] = str(int(number[pos]) + 1)
    return prefix + "".join(number).zfill(4)


def run_create(context, args):
    context.require_readable()
    common = {}
    for field, option in (("parent", args.parent), ("tags", args.tag), ("paths", args.paths),
                          ("modifies", args.modifies), ("blocked_by", args.blocked_by)):
        if option is not None:
            common[field] = field_values(context, args.kind, field, [option] if field == "parent" else option)
    messages, errors = [], []
    mode = context.mode(args.kind)
    identity = next_identity(context, args.kind)
    for index, title in enumerate(args.titles):
        try:
            field_values(context, args.kind, "title", [title])
            fields = {"id": identity, "title": title, **common}
            if args.kind == "task":
                fields.update(status="pending")
                fields.setdefault("modifies", [])
            slug = re.sub(r"[^\w]+", "-", title, flags=re.UNICODE).replace("_", "-").strip("-").lower()[:80] or "entity"
            path = context.root / args.kind / f"{identity}-{slug}.md"
            heading = title.replace("\r", " ").replace("\n", " ")
            marker = " (NEEDS APPROVAL)" if mode != "autonomous" else ""
            body = f"\n# {heading}{marker}\n"
            content = "+++\n" + "\n".join(f"{key} = {encode_value(value)}" for key, value in fields.items()) + "\n+++\n" + body
            commit_changes(context.root, {path: content.encode("utf-8")}, {path: None})
            entity = Entity(path, args.kind, fields, body)
            context.store.entities.append(entity)
            context.store.by_id[identity] = entity
            messages.append(f"Created {identity} {title!r}: {path}; {context.mode_message(entity)}")
            identity = increment_identity(identity)
        except RollbackError as exc:
            errors.append(f"create {title!r}: rollback incomplete; inspect files: {exc}")
            errors.extend(f"create {remaining!r}: not attempted after rollback failure" for remaining in args.titles[index + 1:])
            return messages, errors
        except (ValueError, OSError) as exc:
            errors.append(f"create {title!r}: failed; no changes for this target: {exc}")
    messages.extend(context.tag_advice(common.get("tags", [])))
    return messages, errors


def run_field(context, args):
    context.require_configuration()
    if args.field not in FIELDS:
        raise ValueError(f"{args.field}: unsupported or protected field; use task for status, edit agent_mode deliberately under its approval rules")
    cardinality, kinds, required = FIELDS[args.field]
    if args.action in ("add", "remove") and cardinality != "list":
        raise ValueError(f"{args.field}: add/remove require a list field")
    if args.action == "unset" and required:
        raise ValueError(f"{args.field}: required field cannot be unset")
    # All targets receive the same new edges. Cache reachability once per kind.
    forbidden = set()
    if args.field in ("parent", "blocked_by") and args.action in ("set", "add"):
        edges, graph_errors = graph(context, args.field)
        if graph_errors or find_cycle(edges):
            raise ValueError("Existing relationship errors must be resolved before adding edges: " + "; ".join(graph_errors or ["cycle"]))
        starts = [normalize_id(value) for value in args.value]
        forbidden = reachable(edges, starts)
    messages, errors, seen, advice_tags = [], [], set(), set()
    for index, raw in enumerate(args.entities):
        try:
            identity = normalize_id(raw)
            if identity in seen:
                continue
            seen.add(identity)
            entity = context.resolve(identity)
            if entity.archived or entity.type not in kinds:
                raise ValueError("only supported current entities may be changed")
            policy = context.mode_message(entity)
            if identity in forbidden:
                raise ValueError(f"{args.field}: change would create a cycle")
            if args.action == "unset":
                value = None
            else:
                incoming = field_values(context, entity.type, args.field, args.value)
                if args.action in ("add", "remove"):
                    current = entity.fields.get(args.field, [])
                    current = field_values(context, entity.type, args.field, current)
                    if args.action == "add":
                        value = list(dict.fromkeys(current + incoming))
                    else:
                        remove = set(incoming)
                        value = [item for item in current if item not in remove]
                else:
                    value = incoming
            raw_bytes = entity.path.read_bytes()
            updated = edit_fields(raw_bytes, {args.field: value})
            commit_changes(context.root, {entity.path: updated}, {entity.path: raw_bytes})
            if value is None:
                entity.fields.pop(args.field, None)
            else:
                entity.fields[args.field] = value
            if args.field == "tags":
                advice_tags.update(value or [])
            state = "Unchanged" if updated == raw_bytes else "Updated"
            messages.append(f"{state} {identity}: {args.field}; {policy}")
        except RollbackError as exc:
            errors.append(f"field {raw}: rollback incomplete; inspect files: {exc}")
            errors.extend(f"field {remaining}: not attempted after rollback failure" for remaining in args.entities[index + 1:])
            return messages, errors
        except (ValueError, OSError) as exc:
            errors.append(f"field {raw}: failed; no changes for this target: {exc}")
    if args.field == "tags":
        messages.extend(context.tag_advice(advice_tags))
    return messages, errors
