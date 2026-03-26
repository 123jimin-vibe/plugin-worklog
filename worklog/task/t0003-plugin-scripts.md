+++
id = "t0003"
title = "Implement plugin scripts"
tags = ["tooling"]
status = "pending"
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

- `parse_frontmatter(path) → dict` — extract TOML between `+++` fences.
- Entity type inferred from ID prefix (`s` → spec, `t` → task, `d` → decision).

### lib/discover.py — entity discovery

- `discover_entities(worklog_root) → list[dict]` — walk `spec/` (recursive), `task/`, `decision/`, `archive/task/` and return parsed frontmatter + file path for each entity.
- `load_tags(worklog_root) → set[str]` — parse `tags.md` and return the set of known tags.

### validate.py

Checks all entities under `-w` for:

- Valid TOML frontmatter between `+++` fences.
- Required fields present per entity type:
  - Spec: `id`, `title`, `tags`. Optional: `paths`, `parent`.
  - Task: `id`, `title`, `tags`, `status`, `modifies`. Optional: `blocked_by`.
  - Decision: `id`, `title`, `relates_to`. Optional: `supersedes`.
- ID format matches prefix (`sNNNN`, `tNNNN`, `dNNNN`).
- Filename starts with ID (`{id}-*.md`).
- Status values valid: `pending`, `active`, `done`, `blocked`, `cancelled`.
- Dangling refs: `modifies` → spec exists, `blocked_by` → task exists, `relates_to` → spec exists, `supersedes` → decision exists.
- Tags in frontmatter exist in `tags.md` index (per s0015).
- No duplicate IDs across files.
- Scans both active directories and `archive/task/`.

### next_id.py

Positional arg: entity type (`spec`, `task`, `decision`). Scans all files (active + archive), prints the next available 4-digit ID.

```
python next_id.py spec    → s0017
python next_id.py task    → t0005
python next_id.py decision → d0002
```

### drift.py

For each spec with a `paths` field:

1. Get spec's last-touched commit: `git log -1 --format=%H -- <spec-file>`.
2. Diff against HEAD: `git diff <commit>..HEAD -- <glob patterns>`.
3. Report non-empty diffs as potential drift.

### search.py

Query entities by combinable filters (AND logic):

- `--tag <tag>` — entities with matching tag.
- `--status <status>` — tasks with matching status.
- `--modifies <spec-id>` — tasks that modify a given spec.
- `--type <entity-type>` — filter to spec, task, or decision.
- `--relates-to <spec-id>` — decisions related to a given spec.

### list.py

List entities with optional filtering and grouping. Default output: one line per entity with ID, title, and status (for tasks).

- `--type <entity-type>` — show only specs, tasks, or decisions.
- `--group-by <field>` — group output by `type`, `status`, or `tag`.
- `--sort <field>` — sort by `id` (default) or `title`.
- `--archived` — include archived entities (excluded by default).

```
python list.py                        → all active entities, sorted by ID
python list.py --type task            → active tasks only
python list.py --type task --group-by status → tasks grouped by status
python list.py --archived             → include archived entities
```

## Test Plan

Build a temporary fixture worklog — a small directory tree with known-good and known-bad entities — and run each script against it, checking exit codes and output. No mocking; scripts operate on real files and (for drift) a real git repo.

Fixture contents: a valid spec, task, and decision (happy-path baseline); a task in `archive/task/` (verifies archive scanning); a `tags.md` with a known tag set; deliberately broken entities for error-path tests (one per validation rule).

Testing approach defined in s0017.

### lib/parse.py

| Case | Input | Expected |
|------|-------|----------|
| Valid frontmatter | File with `+++` fences and valid TOML | Returns dict with parsed fields |
| Missing closing fence | File with opening `+++` but no closing | Raises or returns error |
| Empty frontmatter | File with `+++\n+++` and no fields | Returns empty dict |
| No frontmatter | Plain markdown file | Raises or returns error |
| Multiline TOML values | Array field like `tags = ["a", "b"]` | Parsed correctly as list |
| Entity type from ID | `id = "s0001"` | Type inferred as `spec` |
| Entity type from ID | `id = "t0001"` | Type inferred as `task` |
| Entity type from ID | `id = "d0001"` | Type inferred as `decision` |
| Unknown ID prefix | `id = "x0001"` | Raises or returns unknown |
| Content after frontmatter | Body text below closing `+++` | Body ignored, frontmatter parsed |

### lib/discover.py

| Case | Input | Expected |
|------|-------|----------|
| Standard layout | Entities in `spec/`, `task/`, `decision/` | All discovered |
| Recursive spec dirs | Specs in `spec/entity/`, `spec/workflow/` | All found |
| Archive scanning | Task in `archive/task/` | Included in results |
| Empty worklog | No entity files | Returns empty list |
| Non-entity files | README.md in `spec/` | Skipped (no valid frontmatter or wrong extension) |
| Mixed valid/invalid | Some parseable, some broken | Valid ones returned, broken ones reported |
| load_tags happy path | Standard `tags.md` with table | Returns set of tag strings |
| load_tags empty | `tags.md` with no rows | Returns empty set |
| load_tags missing | No `tags.md` file | Raises or returns empty set |

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
| Unknown tag | Tag not in `tags.md` | Reports unknown tag |
| Duplicate IDs | Two files with same ID | Reports duplicate |
| Archived entity refs | Active task blocked_by archived task | No error (ref is valid) |
| Multiple errors | Several broken entities | All errors reported, not just first |

### next_id.py

| Case | Input | Expected |
|------|-------|----------|
| Normal sequence | Existing s0001, s0003, s0010 | Prints `s0017` (next after highest) |
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
| `--relates-to s0007` | Decisions | Only decisions relating to s0007 |
| Combined filters | `--tag tooling --status pending` | AND logic applied |
| No matches | `--tag nonexistent` | Empty output, exit 0 |
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
| Empty result | `--type decision` on worklog with no decisions | Empty output, exit 0 |

## Dangers

1. **validate silently passes bad input.** A missing or buggy check lets broken worklogs look clean. Mitigation: test fixture must include at least one failing case per validation rule — untested rules don't exist.
2. **TOML parsing edge cases.** Multiline strings, special characters, or trailing whitespace in frontmatter trip up hand-rolled parsers. Mitigation: use `tomllib`, don't regex-parse values.
3. **Path separator differences.** Scripts run on Windows (this repo) and potentially Unix. Hardcoded `/` or `\` breaks cross-platform. Mitigation: use `pathlib` throughout, never string-concatenate paths.
4. **drift.py depends on git state.** Running outside a git repo, in a shallow clone, or with no commits will fail. Mitigation: detect and report gracefully rather than stack-tracing.
5. **drift.py false positives.** Whitespace-only or formatting-only changes flag as drift. git diff doesn't know what's semantic. Mitigation: document the limitation; consider `--stat` summary mode.
6. **next_id.py gap-filling ambiguity.** "Next available" could mean fill gaps or increment past highest. Gap-filling risks colliding with intentionally deleted entities. Safer default: increment past highest.
7. **lib/discover.py must recurse into subdirectories.** Specs live in `spec/entity/`, `spec/workflow/`, not just `spec/`. The task says "recursive" but this is easy to miss in implementation.
8. **list.py vs search.py overlap.** Both filter entities. list.py is for quick overview (grouping, sorting, human-readable). search.py is for precise queries (combinable field filters, machine-friendly). If the boundary blurs, one script absorbs the other and gets too complex.
