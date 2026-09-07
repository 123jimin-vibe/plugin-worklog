"""Per-invocation discovery, policies, relationships and tag diagnostics."""

from collections import defaultdict
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from .configuration import DEFAULT_MODES, MODES, read_configuration
from .entities import discover_entities
from .filesystem import is_link
from .identity import normalize_id
from .tags import normalize_tag, read_tags

RESOLVED = {"done", "cancelled"}


class Context:
    def __init__(self, project):
        self.project = Path(project).expanduser().resolve()
        self.root = self.project / "worklog"
        if not self.root.is_dir() or is_link(self.root):
            raise ValueError(f"{self.root}: existing unlinked worklog required; use init after adoption")
        self.store = discover_entities(self.root)
        self.errors = list(self.store.errors)
        self.config = {}
        self.configuration_error = None
        path = self.root / "project.toml"
        try:
            if path.exists():
                self.config = read_configuration(path)
        except (OSError, ValueError) as exc:
            self.configuration_error = str(exc)
            self.errors.append(str(exc))
        self.refs = defaultdict(list)
        for entity in self.store.entities:
            try:
                tags = [normalize_tag(tag) for tag in entity.tags]
                if len(set(tags)) != len(tags):
                    raise ValueError("duplicate normalized entity tags")
                for tag in tags:
                    self.refs[tag].append(entity)
            except ValueError as exc:
                self.errors.append(f"{entity.path}: {exc}")
        self.database = None
        self.tag_error = None
        path = self.root / "tags.csv"
        if path.exists():
            try:
                self.database = read_tags(path)
            except (OSError, ValueError, UnicodeError) as exc:
                self.tag_error = str(exc)

    def require_readable(self):
        if self.errors:
            raise ValueError("\n".join(self.errors))

    def require_configuration(self):
        if self.configuration_error:
            raise ValueError(self.configuration_error)

    def resolve(self, raw):
        identity = normalize_id(raw)
        if identity not in self.store.by_id:
            raise ValueError(f"{identity}: missing or ambiguous entity")
        return self.store.by_id[identity]

    def mode(self, entity_or_type):
        if isinstance(entity_or_type, str):
            kind, fields = entity_or_type, {}
        else:
            kind, fields = entity_or_type.type, entity_or_type.fields
        if kind not in DEFAULT_MODES:
            return None
        mode = fields.get("agent_mode", self.config.get(kind, {}).get("agent_mode", DEFAULT_MODES[kind]))
        if not isinstance(mode, str) or mode not in MODES:
            raise ValueError(f"{kind}: invalid agent_mode {mode!r}")
        return mode

    def mode_message(self, entity_or_type):
        mode = self.mode(entity_or_type)
        guidance = {
            None: "Agent mode does not apply.",
            "read_only": "Agents must not edit; humans may edit.",
            "propose": "Agents need content approval or scoped edit permission; invocation does not establish approval.",
            "draft": "Unapproved agent-authored content needs NEEDS APPROVAL.",
            "autonomous": "Agents may edit without routine approval.",
        }
        return f"agent_mode={mode}: {guidance[mode]}" if mode else guidance[None]

    def tag_advice(self, names):
        if self.tag_error:
            return [f"Tag database error: {self.tag_error}"]
        if self.database is None:
            return ["Tag database missing (informational); no database created."]
        return [f"Unknown tag (advisory): {name}" for name in sorted(set(names) - self.database.keys())]


def relation_ids(entity, name):
    values = entity.fields.get(name, [])
    if name == "parent":
        values = [] if "parent" not in entity.fields else [values]
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise ValueError(f"{entity.id}: invalid {name} values")
    return [normalize_id(value) for value in values]


def graph(context, name):
    edges, errors = {}, []
    for entity in context.store.by_id.values():
        if name == "blocked_by" and entity.type != "task":
            continue
        try:
            refs = relation_ids(entity, name)
            if name == "parent" and refs and entity.type not in DEFAULT_MODES:
                raise ValueError(f"{entity.id}: parent is unavailable for {entity.type}")
            for ref in refs:
                target = context.resolve(ref)
                if target.type != entity.type:
                    raise ValueError(f"{entity.id}: {name} must refer to {entity.type}")
            edges[entity.id] = refs
        except ValueError as exc:
            errors.append(str(exc))
    return edges, errors


def reachable(edges, starts):
    seen, todo = set(), list(starts)
    while todo:
        identity = todo.pop()
        if identity not in seen:
            seen.add(identity)
            todo.extend(edges.get(identity, []))
    return seen


def find_cycle(edges):
    """Return one detected cycle, or an empty list for an acyclic graph."""
    try:
        TopologicalSorter(edges).prepare()
    except CycleError as exc:
        return list(reversed(exc.args[1]))
    return []
