+++
id = "t0003"
title = "Implement plugin scripts"
tags = ["tooling"]
status = "done"
modifies = ["s0010"]
+++

# Implement plugin scripts

Implement the scripts listed in s0010 Anticipated Changes: validate, next-id, drift, search, list. Python, bundled at `plugin/skills/worklog/script/`, accepting `-w PATH` for worklog root (default `./worklog`). Shared logic (frontmatter parsing, entity discovery) lives under `lib/`.

## Files

```
plugin/skills/worklog/script/
├── __init__.py
├── lib/
│   ├── __init__.py
│   ├── parse.py
│   └── discover.py
├── validate.py
├── next_id.py
├── drift.py
├── search.py
└── list.py
```

### lib/parse.py — frontmatter parsing

Dataclass:

```python
@dataclass
class Entity:
    id: str
    title: str
    type: str           # "spec", "task", "decision" — inferred from ID prefix
    tags: list[str]
    path: Path          # filesystem path to the source file
    fields: dict        # all remaining frontmatter fields (status, modifies, paths, ...)
```

- `parse_frontmatter(path) → Entity` — extract TOML between `+++` fences, infer entity type from ID prefix (`s` → spec, `t` → task, `d` → decision), return a populated `Entity`.

### lib/discover.py — entity discovery

Dataclass:

```python
@dataclass
class Tag:
    name: str
    description: str    # from tags.csv; empty string if absent
```

Protocol — `discover_entities` returns a list today but the interface should not assume a flat-file walk is the only backend. Future implementations may read from SQLite, a bead store, or a cached index. Callers should depend on the minimal interface: `store.entities` is iterable (not necessarily indexable), each element exposes the documented attributes. Code that needs random access should collect into its own list.

```python
@dataclass
class EntityStore:
    entities: Iterable[Entity]
    errors: list[str]   # parse/discovery errors encountered
```

- `discover_entities(worklog_root) → EntityStore` — walk `spec/` (recursive), `task/`, `decision/`, `archive/task/`, parse each file, and return an `EntityStore`. Parse errors are collected in `errors` rather than aborting.
- `load_tags(worklog_root) → list[Tag]` — parse `tags.csv` and return a list of `Tag` objects with names and descriptions. Standalone; not bundled into `EntityStore`.

### validate.py

Check all entities for structural correctness.

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-w` | path | `./worklog` | Worklog root directory. |

**Checks:**

- Valid TOML frontmatter between `+++` fences.
- Required fields present per entity type:
  - Spec: `id`, `title`, `tags`. Optional: `paths`, `parent`.
  - Task: `id`, `title`, `tags`, `status`, `modifies`. Optional: `blocked_by`.
  - Decision: `id`, `title`, `relates_to`. Optional: `tags`, `supersedes`.
- ID format matches prefix + digits (`s` + digits, `t` + digits, `d` + digits).
- Filename starts with ID (`{id}-*.md`).
- Task status values valid: `pending`, `active`, `done`, `blocked`, `cancelled`.
- Dangling refs: `modifies` → spec exists, `blocked_by` → task exists, `relates_to` → spec exists, `supersedes` → decision exists.
- Tags in frontmatter exist in `tags.csv` index (per s0015).
- No duplicate IDs across files.
- Scans both active directories and `archive/task/`.

**Exit:** 0 if no errors, non-zero if any check fails. All errors printed, not just first.

### next_id.py

Print the next available ID for a given entity type (4-digit zero-padded by convention).

**Flags and args:**

| Flag/Arg | Type | Default | Description |
|----------|------|---------|-------------|
| `-w` | path | `./worklog` | Worklog root directory. |
| `<type>` | positional | *(required)* | Entity type: `spec`, `task`, or `decision`. |

Scans active directories and `archive/task/`. Next ID is one past the highest existing (no gap-filling).

**Exit:** 0 on success (prints ID to stdout), non-zero on invalid or missing type argument.

### drift.py

Report specs whose governed source files changed after the spec was last touched.

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-w` | path | `./worklog` | Worklog root directory. |

**Behavior:** For each spec with a `paths` field:

1. Get spec's last-touched commit: `git log -1 --format=%H -- <spec-file>`.
2. Diff against HEAD: `git diff <commit>..HEAD -- <glob patterns>`.
3. Report non-empty diffs as potential drift.

Specs without `paths` are skipped. Specs not yet committed are skipped or warned.

**Exit:** 0 if no drift detected, non-zero if any spec has drift.

### search.py

Query entities by combinable filters (AND logic).

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-w` | path | `./worklog` | Worklog root directory. |
| `--tag` | string | *(none)* | Filter to entities with this tag. |
| `--status` | string | *(none)* | Filter to tasks with this status. |
| `--modifies` | string | *(none)* | Filter to tasks that modify a given spec ID. |
| `--type` | string | *(none)* | Filter to entity type: `spec`, `task`, or `decision`. |
| `--relates-to` | string | *(none)* | Filter to decisions related to a given spec ID. |

Multiple filters are combined with AND. Prints matching entity IDs and titles to stdout. When no entities match, prints `(none)` to stdout.

**Exit:** 0 always (empty result is not an error, non-zero reserved for bad args or missing worklog).

### list.py

List entities with optional filtering, grouping, and sorting. Default: one line per active entity, sorted by ID.

**Flags:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `-w` | path | `./worklog` | Worklog root directory. |
| `--type` | string | *(none)* | Show only `spec`, `task`, or `decision`. |
| `--group-by` | string | *(none)* | Group output by `type`, `status`, or `tag`. |
| `--sort` | string | `id` | Sort by `id` or `title`. |
| `--archived` | flag | off | Include archived entities in output. |

When `--group-by tag`, multi-tagged entities appear under each tag. Tasks include status in output. When no entities match, prints `(none)` to stdout.

**Exit:** 0 always (empty result is not an error, non-zero reserved for bad args or missing worklog).

## Test Plan

Build a temporary fixture worklog — a small directory tree with known-good and known-bad entities — and run each script against it, checking exit codes and output. No mocking; scripts operate on real files and (for drift) a real git repo.

Fixture contents: a valid spec, task, and decision (happy-path baseline); a task in `archive/task/` (verifies archive scanning); a `tags.csv` with a known tag set; deliberately broken entities for error-path tests (one per validation rule).

Testing approach defined in s0017. Tests verify attributes and behavior via duck typing (e.g. `result.id`, `result.type`), not concrete class identity.

### lib/parse.py

| Case | Input | Expected |
|------|-------|----------|
| Valid frontmatter | File with `+++` fences and valid TOML | Returns `Entity` with correct `id`, `title`, `tags`, `path` |
| Fields dict | Spec with `paths` and `parent` | Extra fields in `entity.fields` |
| Missing closing fence | File with opening `+++` but no closing | Raises or returns error |
| Empty frontmatter | File with `+++\n+++` and no fields | Raises (missing required `id`) |
| No frontmatter | Plain markdown file | Raises or returns error |
| Multiline TOML values | Array field like `tags = ["a", "b"]` | `entity.tags` is a list |
| Entity type from ID | `id = "s0001"` | `entity.type == "spec"` |
| Entity type from ID | `id = "t0001"` | `entity.type == "task"` |
| Entity type from ID | `id = "d0001"` | `entity.type == "decision"` |
| Unknown ID prefix | `id = "x0001"` | Raises or returns unknown |
| Content after frontmatter | Body text below closing `+++` | Body ignored, `Entity` populated from frontmatter only |
| Path stored | Any valid file | `entity.path` matches the input path |

### lib/discover.py

| Case | Input | Expected |
|------|-------|----------|
| Standard layout | Entities in `spec/`, `task/`, `decision/` | `store.entities` contains all three |
| Recursive spec dirs | Specs in `spec/entity/`, `spec/workflow/` | All found in `store.entities` |
| Archive scanning | Task in `archive/task/` | Included in `store.entities` |
| Empty worklog | No entity files | `store.entities` is empty |
| Non-entity files | README.md in `spec/` | Skipped, not in `store.entities` |
| Mixed valid/invalid | Some parseable, some broken | Valid in `store.entities`, broken in `store.errors` |
| load_tags happy path | Standard `tags.csv` with table | Returns `Tag` objects with names and descriptions |
| load_tags description | Tag row with description text | `tag.description` contains the text |
| load_tags empty | `tags.csv` with no rows | Returns empty list |
| load_tags missing | No `tags.csv` file | Raises or returns empty list |

### validate.py

| Case | Input | Expected |
|------|-------|----------|
| Clean worklog | All valid entities | Exit 0, no errors |
| Malformed TOML | Missing closing `+++` | Reports parse error with file path |
| Missing required field | Task without `status` | Reports which field, which file |
| Bad ID format | `s00a1` | Reports format violation |
| Filename/ID mismatch | File `t0002-foo.md` with `id = "t0003"` | Reports mismatch |
| Invalid status | `status = "wip"` | Reports invalid value |
| Dangling `modifies` | Task modifies `s9999` | Reports dangling ref |
| Dangling `blocked_by` | Task blocked by `t9999` | Reports dangling ref |
| Dangling `relates_to` | Decision relates to `s9999` | Reports dangling ref |
| Dangling `supersedes` | Decision supersedes `d9999` | Reports dangling ref |
| Unknown tag | Tag not in `tags.csv` | Reports unknown tag |
| Duplicate IDs | Two files with same ID | Reports duplicate |
| Archived entity refs | Active task blocked_by archived task | No error (ref is valid) |
| Multiple errors | Several broken entities | All errors reported, not just first |

### next_id.py

| Case | Input | Expected |
|------|-------|----------|
| Normal sequence | Existing s0001, s0003, s0010 | Prints `s0011` (next after highest) |
| Empty type | No specs exist | Prints `s0001` |
| Includes archive | Archived t0004 exists | Next task ID accounts for it |
| Invalid type arg | `python next_id.py banana` | Error message, non-zero exit |
| No args | No positional arg | Usage message, non-zero exit |

### drift.py

| Case | Input | Expected |
|------|-------|----------|
| No drift | Spec paths unchanged since spec commit | Clean report for that spec |
| Drift present | File under spec's paths changed after spec commit | Reports the spec and changed files |
| No `paths` field | Spec without paths | Skipped silently |
| Spec never committed | New spec file not yet in git | Handled gracefully (skip or warn) |
| Glob patterns | Paths with `**` wildcards | Expanded correctly by git diff |

### search.py

| Case | Input | Expected |
|------|-------|----------|
| `--tag tooling` | Mix of tagged entities | Only entities tagged `tooling` |
| `--status pending` | Tasks in various statuses | Only pending tasks |
| `--modifies s0001` | Tasks modifying different specs | Only tasks modifying s0001 |
| `--type spec` | All entity types | Only specs |
| `--relates-to s0010` | Decisions | Only decisions relating to s0010 |
| Combined filters | `--tag tooling --status pending` | AND logic applied |
| No matches | `--tag nonexistent` | Prints `(none)`, exit 0 |
| No filters | No args | All entities (or usage error — design call needed) |

### list.py

| Case | Input | Expected |
|------|-------|----------|
| Default | No args | All active entities, one per line, sorted by ID |
| Filter by type | `--type task` | Only tasks |
| Group by status | `--type task --group-by status` | Tasks grouped under status headings |
| Group by tag | `--group-by tag` | Entities under each tag (entity appears under multiple tags if multi-tagged) |
| Sort by title | `--sort title` | Alphabetical by title |
| Excludes archive | Default | Archived entities absent |
| Includes archive | `--archived` | Archived entities present, marked as archived |
| Empty result | `--type decision` on worklog with no decisions | Prints `(none)`, exit 0 |

## Dangers

1. **validate silently passes bad input.** A missing or buggy check lets broken worklogs look clean. Mitigation: test fixture must include at least one failing case per validation rule — untested rules don't exist.
2. **TOML parsing edge cases.** Multiline strings, special characters, or trailing whitespace in frontmatter trip up hand-rolled parsers. Mitigation: use `tomllib`, don't regex-parse values.
3. **Path separator differences.** Scripts run on Windows (this repo) and potentially Unix. Hardcoded `/` or `\` breaks cross-platform. Mitigation: use `pathlib` throughout, never string-concatenate paths.
4. **drift.py depends on git state.** Running outside a git repo, in a shallow clone, or with no commits will fail. Mitigation: detect and report gracefully rather than stack-tracing.
5. **drift.py false positives.** Whitespace-only or formatting-only changes flag as drift. git diff doesn't know what's semantic. Mitigation: document the limitation; consider `--stat` summary mode.
6. **next_id.py gap-filling ambiguity.** "Next available" could mean fill gaps or increment past highest. Gap-filling risks colliding with intentionally deleted entities. Safer default: increment past highest.
7. **lib/discover.py must recurse into subdirectories.** Specs live in `spec/entity/`, `spec/workflow/`, not just `spec/`. The task says "recursive" but this is easy to miss in implementation.
8. **list.py vs search.py overlap.** Both filter entities. list.py is for quick overview (grouping, sorting, human-readable). search.py is for precise queries (combinable field filters, machine-friendly). If the boundary blurs, one script absorbs the other and gets too complex.
