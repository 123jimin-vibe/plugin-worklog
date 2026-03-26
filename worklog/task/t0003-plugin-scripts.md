+++
id = "t0003"
title = "Implement plugin scripts"
tags = ["tooling"]
status = "pending"
modifies = ["s0010"]
+++

# Implement plugin scripts

Implement the scripts listed in s0010 Anticipated Changes: validate, next-id, drift, search. Python, bundled at `plugin/skills/worklog/script/`, accepting `-w PATH` for worklog root (default `./worklog`).

## Priority

1. **validate** — dangling refs, invalid statuses, missing required fields. Most impactful: prevents silent integrity erosion.
2. **next-id** — next available ID for a given entity type. Low complexity, high convenience.
3. **drift** — spec-code drift report for specs with `paths`.
4. **search** — query entities by tag, status, or relationship.

## Files

```
plugin/skills/worklog/script/
├── __init__.py
├── parse.py
├── validate.py
├── next_id.py
├── drift.py
└── search.py
```

### parse.py — shared frontmatter and discovery

- `parse_frontmatter(path) → dict` — extract TOML between `+++` fences.
- `discover_entities(worklog_root) → list[dict]` — walk `spec/` (recursive), `task/`, `decision/`, `archive/task/` and return parsed frontmatter + file path for each entity.
- Entity type inferred from ID prefix (`s` → spec, `t` → task, `d` → decision).

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
