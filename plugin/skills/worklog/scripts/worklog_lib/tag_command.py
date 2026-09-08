"""Tag database operations and coordinated reference renames."""

from .editing import edit_fields
from .tags import normalize_tag, render_tags
from .transactions import commit_changes


def run_tag(context, args):
    if context.tag_error:
        raise ValueError(context.tag_error)
    if context.database is None:
        raise ValueError("Tag database missing; run init to create it from existing tags")
    database = dict(context.database)
    messages = []
    if args.action == "list":
        for name in sorted(database):
            messages.append(f"{name}: {database[name]}")
        try:
            refs = context.tag_references()
        except (ValueError, OSError) as exc:
            return messages + ["No worklog changes."], [f"Tag usage is incomplete: {exc}"]
        for name in sorted(refs.keys() - database.keys()):
            messages.append(f"Unknown tag (advisory): {name}: " + ", ".join(str(e.path) for e in refs[name]))
        for name in sorted(database.keys() - refs.keys()):
            messages.append(f"Unused tag (advisory): {name}")
        return messages + ["No worklog changes."], []
    name = normalize_tag(args.tag)
    changes, expected, changed_entities = {}, {}, []
    if args.action == "add":
        if name in database:
            raise ValueError(f"Tag already registered: {name}")
        database[name] = args.description or ""
    else:
        if name not in database:
            raise ValueError(f"Tag is not registered: {name}")
        if args.action == "remove":
            references = context.tag_references().get(name, [])
            if references:
                raise ValueError(f"Tag {name} is referenced by:\n" + "\n".join(str(e.path) for e in references))
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
                for entity in context.tag_references().get(name, []):
                    values = [new if normalize_tag(tag) == name else normalize_tag(tag) for tag in entity.tags]
                    if len(values) != len(set(values)):
                        raise ValueError(f"{entity.path}: rename would duplicate tag {new}")
                    raw = entity.raw
                    content = edit_fields(raw, {"tags": values})
                    policy = context.mode_message(entity)
                    if content != raw:
                        changes[entity.path] = content
                        expected[entity.path] = raw
                        changed_entities.append((entity, values, content))
                        messages.append(f"Updated {entity.id or 'reference'}: {entity.path}; {policy}")
    path = context.root / "tags.csv"
    content = render_tags(database)
    if content != context.database_raw:
        expected[path] = context.database_raw
        changes[path] = content
    if changes:
        commit_changes(context.root, changes, expected)
        for entity, values, raw in changed_entities:
            entity.fields["tags"] = values
            entity.raw = raw
            context.register(entity)
    return [f"Tag {args.action} succeeded: {name}", *messages], []
