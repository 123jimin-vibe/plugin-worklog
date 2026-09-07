"""Tag database operations and coordinated reference renames."""

from .editing import edit_fields
from .tags import normalize_tag, render_tags
from .transactions import commit_changes


def run_tag(context, args):
    context.require_readable()
    if context.tag_error:
        raise ValueError(context.tag_error)
    if context.database is None:
        raise ValueError("Tag database missing; run init to create it from existing tags")
    database = dict(context.database)
    messages = []
    if args.action == "list":
        for name in sorted(database):
            messages.append(f"{name}: {database[name]}")
        for name in sorted(context.refs.keys() - database.keys()):
            messages.append(f"Unknown tag (advisory): {name}: " + ", ".join(str(e.path) for e in context.refs[name]))
        for name in sorted(database.keys() - context.refs.keys()):
            messages.append(f"Unused tag (advisory): {name}")
        return messages + ["No worklog changes."], []
    name = normalize_tag(args.tag)
    changes, expected = {}, {}
    if args.action == "add":
        if name in database:
            raise ValueError(f"Tag already registered: {name}")
        database[name] = args.description or ""
    else:
        if name not in database:
            raise ValueError(f"Tag is not registered: {name}")
        if args.action == "remove":
            if context.refs[name]:
                raise ValueError(f"Tag {name} is referenced by:\n" + "\n".join(str(e.path) for e in context.refs[name]))
            del database[name]
        else:
            if args.name is None and args.description is None:
                raise ValueError("tag update requires --name, --description, or both")
            new = normalize_tag(args.name) if args.name is not None else name
            if new != name and new in database:
                raise ValueError(f"Tag already registered: {new}")
            description = database.pop(name)
            database[new] = args.description if args.description is not None else description
            if new != name:
                for entity in context.refs[name]:
                    values = [new if normalize_tag(tag) == name else normalize_tag(tag) for tag in entity.tags]
                    if len(values) != len(set(values)):
                        raise ValueError(f"{entity.path}: rename would duplicate tag {new}")
                    raw = entity.path.read_bytes()
                    changes[entity.path] = edit_fields(raw, {"tags": values})
                    expected[entity.path] = raw
                    messages.append(f"Updated {entity.id or 'reference'}: {entity.path}; {context.mode_message(entity)}")
    path = context.root / "tags.csv"
    expected[path] = path.read_bytes()
    changes[path] = render_tags(database)
    commit_changes(context.root, changes, expected)
    return [f"Tag {args.action} succeeded: {name}", *messages], []
