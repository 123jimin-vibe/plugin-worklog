"""Task lifecycle transitions and closure with preflighted archival."""

from .context import RESOLVED, relation_ids
from .editing import edit_fields
from .identity import normalize_id
from .initialization import RollbackError
from .markers import markers
from .transactions import commit_changes

TRANSITIONS = {
    "start": ({"pending"}, "active"),
    "block": ({"pending", "active"}, "blocked"),
    "resume": ({"blocked"}, "active"),
    "finish": ({"active", "done"}, "done"),
    "cancel": ({"pending", "active", "blocked", "cancelled"}, "cancelled"),
}


def unresolved(context, entity):
    result = []
    for identity in relation_ids(entity, "blocked_by"):
        dependency = context.resolve(identity)
        if dependency.type != "task":
            raise ValueError(f"blocked_by {identity} is not a task")
        if dependency.fields.get("status") not in RESOLVED:
            result.append(identity)
    return result


def run_task(context, args):
    context.require_configuration()
    messages, errors, seen = [], [], set()
    allowed, target_status = TRANSITIONS[args.action]
    for index, raw in enumerate(args.entities):
        try:
            identity = normalize_id(raw)
            if identity in seen:
                continue
            seen.add(identity)
            entity = context.resolve(identity)
            if entity.type != "task":
                raise ValueError("task command requires task IDs")
            policy = context.mode_message(entity)
            if "modifies" not in entity.fields:
                raise ValueError("task is missing required modifies field")
            status = entity.fields.get("status")
            if entity.archived:
                if args.action in ("finish", "cancel") and status == target_status:
                    messages.append(f"Unchanged {identity}: already {status} and archived")
                    continue
                raise ValueError("archived tasks are terminal; create another task")
            if status not in allowed:
                raise ValueError(f"cannot {args.action} a {status} task")
            if args.action in ("start", "resume", "finish"):
                waiting = unresolved(context, entity)
                if waiting:
                    raise ValueError("unresolved dependencies: " + ", ".join(waiting))
            reason = getattr(args, "reason", None)
            checked = getattr(args, "checked", None)
            if args.action == "block" and not (reason and reason.strip()):
                raise ValueError("block requires a non-empty --reason")
            if args.action == "resume" and not (checked and checked.strip()):
                raise ValueError("resume requires a non-empty --checked description")
            if args.action == "cancel" and status != "cancelled" and not (reason and reason.strip()):
                raise ValueError("new cancellation requires a non-empty --reason")
            closing = args.action in ("finish", "cancel")
            governed = []
            if closing:
                for spec_id in relation_ids(entity, "modifies"):
                    spec = context.resolve(spec_id)
                    if spec.type != "spec":
                        raise ValueError(f"modifies {spec_id} is not a spec")
                    if any(marker in ("NEEDS APPROVAL", "NEEDS REVIEW") for marker, _, _ in markers(spec.body)):
                        raise ValueError(f"{spec_id}: spec content needs approval; resolve required review before closure")
                    governed.append(f"{spec_id} ({context.mode_message(spec)})")
            append = ""
            if args.action == "block":
                append = f"Block reason: {reason}"
            elif args.action == "resume":
                append = f"Resume check: {checked}"
            elif args.action == "cancel" and status != "cancelled":
                append = f"Cancellation reason: {reason}"
            raw_bytes = entity.path.read_bytes()
            content = edit_fields(raw_bytes, {"status": target_status}, append)
            changes, expected = {entity.path: content}, {entity.path: raw_bytes}
            destination = entity.path
            if closing:
                destination = context.root / "archive/task" / entity.path.name
                changes = {destination: content, entity.path: None}
                expected[destination] = None
            commit_changes(context.root, changes, expected)
            entity.fields["status"] = target_status
            entity.path = destination
            entity.archived = closing
            messages.append(f"Updated {identity}: {target_status}" + (f"; archived at {destination}" if closing else "") + f"; {policy}")
            if closing:
                messages.append(f"{identity}: caller is responsible for verification and spec write-back before closure; command success is not proof of completion. Governing specs: " + (", ".join(governed) or "none"))
        except RollbackError as exc:
            errors.append(f"task {raw}: rollback incomplete; inspect files: {exc}")
            errors.extend(f"task {remaining}: not attempted after rollback failure" for remaining in args.entities[index + 1:])
            return messages, errors
        except (ValueError, OSError) as exc:
            errors.append(f"task {raw}: failed; no changes for this target: {exc}")
    return messages, errors
