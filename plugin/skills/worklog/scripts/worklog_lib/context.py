"""Per-invocation, demand-driven entity and policy access."""

import re
from collections import defaultdict
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from .configuration import DEFAULT_MODES, MODES, read_configuration
from .entities import entity_paths, read_entity, validate_entity
from .filesystem import is_link
from .identity import ENTITY_TYPES, PREFIX_TO_TYPE, normalize_id
from .tags import normalize_tag, read_tags

RESOLVED = {"done", "cancelled"}


class Context:
    def __init__(self, project):
        self.project = Path(project).expanduser().resolve()
        self.root = self.project / "worklog"
        if not self.root.is_dir() or is_link(self.root):
            raise ValueError(f"{self.root}: existing unlinked worklog required; use init after adoption")
        self._catalogs = {}
        self._paths = defaultdict(list)
        self._name_errors = {}
        self._cache = {}
        self._locations = {}
        self._config_loaded = False
        self._config = {}
        self._configuration_error = None
        self._database_loaded = False
        self._database = None
        self._database_raw = None
        self._tag_error = None

    def catalog(self, kind):
        """Discover filenames of one type; task identity includes its archive."""
        if kind not in self._catalogs:
            paths, errors = entity_paths(self.root, (kind,))
            self._catalogs[kind] = {entry[0]: entry for entry in paths}, errors
            name_errors = []
            if kind != "ref":
                for path, _, archived in paths:
                    match = re.match(r"([stnd][0-9]+)\b", path.name)
                    identity = normalize_id(match[1]) if match else None
                    if identity is None or match[1] != identity or PREFIX_TO_TYPE[identity[0]] != kind:
                        name_errors.append(f"{path}: filename must start with a standard {kind} ID")
                    else:
                        self._paths[identity].append((path, kind, archived))
            self._name_errors[kind] = name_errors
        paths, errors = self._catalogs[kind]
        return paths.values(), errors

    def identities(self, kind):
        _, errors = self.catalog(kind)
        errors = errors + self._name_errors[kind]
        if errors:
            raise ValueError("\n".join(errors))
        return tuple(identity for identity in self._paths if PREFIX_TO_TYPE[identity[0]] == kind)

    def load(self, path, kind, archived=False, *, metadata=False):
        if path not in self._cache:
            try:
                if is_link(path):
                    raise ValueError(f"{path}: linked entity file cannot be read safely")
                self._cache[path] = read_entity(path, kind, archived=archived, validate=False)
                self._locations[id(self._cache[path])] = path
            except (OSError, UnicodeError, ValueError) as exc:
                self._cache[path] = ValueError(f"{path}: {exc}")
        entity = self._cache[path]
        if isinstance(entity, ValueError):
            raise entity
        if not metadata:
            validate_entity(entity)
        return entity

    def resolve(self, raw):
        identity = normalize_id(raw)
        kind = PREFIX_TO_TYPE[identity[0]]
        _, errors = self.catalog(kind)
        if errors:
            raise ValueError("\n".join(errors))
        paths = self._paths.get(identity, ())
        if len(paths) != 1:
            raise ValueError(f"{identity}: missing or ambiguous entity")
        return self.load(*paths[0])

    def scan(self, kinds=None, archived=True, metadata=False):
        entities, errors = [], []
        for kind in ENTITY_TYPES if kinds is None else kinds:
            paths, listing_errors = self.catalog(kind)
            errors.extend(listing_errors)
            for path, _, old in paths:
                if old and not archived:
                    continue
                try:
                    entity = self.load(path, kind, old, metadata=metadata)
                    if not metadata and entity.id is not None and len(self._paths.get(entity.id, ())) != 1:
                        raise ValueError(f"{path}: duplicate entity ID {entity.id}")
                    entities.append(entity)
                except ValueError as exc:
                    errors.append(str(exc))
        return entities, errors

    def register(self, entity):
        previous = self._locations.get(id(entity), entity.path)
        self._cache.pop(previous, None)
        self._cache[entity.path] = entity
        self._locations[id(entity)] = entity.path
        self.catalog(entity.type)
        paths, _ = self._catalogs[entity.type]
        if previous == entity.path and entity.path in paths:
            return
        paths.pop(previous, None)
        entry = entity.path, entity.type, entity.archived
        paths[entity.path] = entry
        if entity.type != "ref":
            match = re.match(r"([stnd][0-9]+)\b", entity.path.name)
            if match:
                identity = normalize_id(match[1])
                entries = [item for item in self._paths.get(identity, ()) if item[0] != previous]
                entries.append(entry)
                self._paths[identity] = entries

    def require_configuration(self):
        if not self._config_loaded:
            self._config_loaded = True
            path = self.root / "project.toml"
            try:
                if path.exists():
                    self._config = read_configuration(path, kinds=())
            except (OSError, UnicodeError, ValueError) as exc:
                self._configuration_error = str(exc)
        if self._configuration_error:
            raise ValueError(self._configuration_error)

    def mode(self, entity_or_type):
        if isinstance(entity_or_type, str):
            kind, fields = entity_or_type, {}
        else:
            kind, fields = entity_or_type.type, entity_or_type.fields
        if kind not in DEFAULT_MODES:
            return None
        if "agent_mode" in fields:
            mode = fields["agent_mode"]
        else:
            self.require_configuration()
            table = self._config.get(kind, {})
            if not isinstance(table, dict):
                raise ValueError(f"{self.root / 'project.toml'}: {kind} must be a policy table")
            mode = table.get("agent_mode", DEFAULT_MODES[kind])
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

    def _load_database(self):
        if not self._database_loaded:
            self._database_loaded = True
            path = self.root / "tags.csv"
            try:
                self._database_raw = path.read_bytes()
                self._database = read_tags(path, raw=self._database_raw)
            except FileNotFoundError:
                pass
            except (OSError, UnicodeError, ValueError) as exc:
                self._tag_error = str(exc)

    @property
    def database(self):
        self._load_database()
        return self._database

    @property
    def database_raw(self):
        self._load_database()
        return self._database_raw

    @property
    def tag_error(self):
        self._load_database()
        return self._tag_error

    def tag_references(self):
        entities, errors = self.scan(metadata=True)
        refs = defaultdict(list)
        for entity in entities:
            try:
                values = entity.fields.get("tags", [])
                if not isinstance(values, list):
                    raise ValueError("tags must be an array of strings")
                tags = [normalize_tag(tag) for tag in values]
                if len(set(tags)) != len(tags):
                    raise ValueError("duplicate normalized entity tags")
                for tag in tags:
                    refs[tag].append(entity)
            except ValueError as exc:
                errors.append(f"{entity.path}: {exc}")
        if errors:
            raise ValueError("\n".join(errors))
        return refs

    def tag_advice(self, names):
        names = set(names)
        if not names:
            return []
        if self.tag_error:
            raise ValueError(self.tag_error)
        if self.database is None:
            return ["Tag database missing (informational); no database created."]
        return [f"Unknown tag (advisory): {name}" for name in sorted(names - self.database.keys())]


def relation_ids(entity, name):
    values = entity.fields.get(name, [])
    if name == "parent":
        values = [] if "parent" not in entity.fields else [values]
    if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
        raise ValueError(f"{entity.id}: invalid {name} values")
    return [normalize_id(value) for value in values]


def graph(context, name, starts):
    """Follow only edges needed by this operation, using current cached fields."""
    edges, errors, seen = {}, [], set()
    todo = list(starts)
    while todo:
        identity = normalize_id(todo.pop())
        if identity in seen:
            continue
        seen.add(identity)
        try:
            entity = context.resolve(identity)
            refs = relation_ids(entity, name)
            if name == "parent" and refs and entity.type not in DEFAULT_MODES:
                raise ValueError(f"{identity}: parent is unavailable for {entity.type}")
            if name == "blocked_by" and entity.type != "task":
                raise ValueError(f"{identity}: blocked_by is unavailable for {entity.type}")
            for ref in refs:
                if PREFIX_TO_TYPE[ref[0]] != entity.type:
                    raise ValueError(f"{identity}: {name} must refer to {entity.type}")
            edges[identity] = refs
            todo.extend(refs)
        except ValueError as exc:
            errors.append(str(exc))
    return edges, errors


def find_cycle(edges):
    """Return one detected cycle, or an empty list for an acyclic graph."""
    try:
        TopologicalSorter(edges).prepare()
    except CycleError as exc:
        return list(reversed(exc.args[1]))
    return []
