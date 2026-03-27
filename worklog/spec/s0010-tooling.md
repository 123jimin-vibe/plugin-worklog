+++
id = "s0010"
title = "Tooling"
tags = ["tooling"]
paths = ["plugin/skills/worklog/script/**"]
+++

# Tooling

Scripts that automate worklog operations, bundled with the plugin at `plugin/skills/worklog/script/`. Python. Accept `-w PATH` for worklog root (default: `./worklog`). Shared logic (parsing, discovery) lives under `lib/`.

## Shared library

`lib/constants.py` — shared constants. Entity type mappings (`ID_PREFIX_TO_TYPE`, `TYPE_TO_PREFIX`, `TYPE_TO_BUCKET`), directory lists (`ENTITY_DIRS`, `ARCHIVE_DIRS`), task-specific statuses (`TASK_STATUSES`), required fields per entity type (`REQUIRED_FIELDS`), ID pattern and helpers (`ID_PATTERN`, `parse_id`, `normalize_id`). ID format is prefix letter + one or more digits (e.g. `s0001`). `normalize_id` converts shorthand like `s1` to canonical `s0001` form.

`lib/parse.py` — frontmatter parsing. `parse_frontmatter(path)` extracts TOML between `+++` fences and returns an `Entity` object with `id`, `title`, `type` (inferred from ID prefix), `tags`, `path`, `archived`, and `fields` (remaining frontmatter).

`lib/discover.py` — entity discovery and tag loading. `discover_entities(worklog_root)` walks entity directories and returns an `EntityStore` with `specs`, `tasks`, `decisions` (separate lists), `entities` (chained iterable of all), and `errors` (list of parse failures). Entities from archive directories have `archived=True`. `load_tags(worklog_root)` parses `tags.csv` and returns a list of `Tag` objects with `name` and `description`.

## Scripts

`validate.py` — dangling refs, invalid statuses, missing required fields, ID format, duplicate IDs, unknown tags.

`next_id.py` — next available ID for a given entity type.

TODO: drift — spec-code drift report for specs with `paths`.

`search.py` — query entities by tag, status, or relationship. ID arguments are normalized (e.g. `s1` matches `s0001`). Prints `(none)` when no matches.

`list.py` — list entities with optional grouping and sorting. Prints `(none)` when no matches.

## Anticipated Changes

- Per-script specs when complexity warrants it.
- Alternative discovery backends (SQLite, cached index) behind the `EntityStore` interface.

## Dangers

- Tools that silently pass on invalid input create false confidence in worklog integrity.
- Drift detection that produces too many false positives gets ignored.
- `EntityStore` callers that assume `list` semantics (indexing, `len()`) will break when the backend changes.
