+++
id = "s0010"
title = "Tooling"
tags = ["tooling"]
paths = ["plugin/skills/worklog/scripts/**"]
+++

# Tooling

Scripts that automate worklog operations, bundled with the plugin at `plugin/skills/worklog/scripts/`. Python. Accept `-w PATH` for worklog root (default: `./worklog`). Shared logic (parsing, discovery) lives under `lib/`.

## Shared library

`lib/constants.py` — shared constants. Entity type mappings (`ID_PREFIX_TO_TYPE`, `TYPE_TO_PREFIX`, `TYPE_TO_BUCKET`), directory lists (`ENTITY_DIRS`, `ARCHIVE_DIRS`), task-specific statuses (`TASK_STATUSES`), required fields per entity type (`REQUIRED_FIELDS`), ID pattern and helpers (`ID_PATTERN`, `parse_id`, `normalize_id`). ID format is prefix letter + one or more digits (e.g. `s0001`). `normalize_id` converts shorthand like `s1` to canonical `s0001` form.

`lib/parse.py` — frontmatter parsing. `parse_frontmatter(path)` extracts TOML between `+++` fences and returns an `Entity` object with `id`, `title`, `type` (inferred from ID prefix), `tags`, `path`, `archived`, `fields` (remaining frontmatter), and `body` (markdown after the closing fence).

`lib/discover.py` — entity discovery and tag loading. `discover_entities(worklog_root)` walks entity directories and returns an `EntityStore` with `specs`, `tasks`, `decisions` (separate lists), `entities` (chained iterable of all), and `errors` (list of parse failures). Entities from archive directories have `archived=True`. `load_tags(worklog_root)` parses `tags.csv` and returns a list of `Tag` objects with `name` and `description`.

`lib/gitdrift.py` — git-based drift classification shared by `drift.py` and `archive.py`. `find_repo_root(path)` locates the enclosing repo; `classify_spec(repo_root, spec)` returns `unmonitored` (no `paths`), `unverifiable` (spec not committed), `drifted`, or `clean`.

## Scripts

`validate.py` — dangling refs, invalid statuses, missing required fields, ID format, duplicate IDs, unknown tags. Also: archived tasks must be terminal (`done`/`cancelled`), cancelled tasks must carry an explanation in their body, and `blocked_by` chains must be acyclic.

`next_id.py` — next available ID for a given entity type.

`drift.py` — spec-code drift report for specs with `paths`. Compares the spec's last commit against the working tree, so uncommitted changes register. Specs it cannot check — those without `paths` (unmonitored) or not yet committed (unverifiable) — are reported on stderr, never silently skipped; the actionable drift list is stdout.

`search.py` — query entities by tag, status, or relationship (`--modifies`, `--relates-to`, `--blocked-by`). ID arguments are normalized (e.g. `s1` matches `s0001`). Archived entities are excluded unless `--archived`. Prints `(none)` when no matches.

`list.py` — list entities with optional grouping and sorting. Under `--group-by status`, status-less entities (specs, decisions) group under `(no status)`. Prints `(none)` when no matches.

`archive.py` — archive one or more `done` or `cancelled` tasks. Prints each spec in `modifies` in full with its drift classification (the archive-time consistency check), then moves the files into `archive/task/` on `--confirm` — `git mv` when tracked, plain move otherwise. Refuses non-terminal tasks and cancelled tasks without an explanation. With multiple IDs each task is handled independently — a task that fails its gate is reported and left in place while the rest archive, and the command exits non-zero if any task could not be archived. Specs shared across the batch are surfaced once.

## Anticipated Changes

- Per-script specs when complexity warrants it.
- Alternative discovery backends (SQLite, cached index) behind the `EntityStore` interface.

## Dangers

- Tools that silently pass on invalid input create false confidence in worklog integrity.
- Drift detection that produces too many false positives gets ignored.
- Drift's baseline is the spec's last commit, so any edit to the spec file — even a typo fix — resets the watermark and can mask real code drift until the next check.
- `EntityStore` callers that assume `list` semantics (indexing, `len()`) will break when the backend changes.
