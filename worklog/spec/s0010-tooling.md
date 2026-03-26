+++
id = "s0010"
title = "Tooling"
tags = ["tooling"]
paths = ["plugin/skills/worklog/script/**"]
+++

# Tooling

Scripts that automate worklog operations, bundled with the plugin at `plugin/skills/worklog/script/`. Python. Accept `-w PATH` for worklog root (default: `./worklog`). Shared logic (parsing, discovery) lives under `lib/`.

## Shared library

`lib/parse.py` — frontmatter parsing. `parse_frontmatter(path)` extracts TOML between `+++` fences and returns an `Entity` object with `id`, `title`, `type` (inferred from ID prefix), `tags`, `path`, and `fields` (remaining frontmatter).

`lib/discover.py` — entity discovery and tag loading. `discover_entities(worklog_root)` walks entity directories and returns an `EntityStore` with `entities` (iterable) and `errors` (list of parse failures). `load_tags(worklog_root)` parses `tags.md` and returns a list of `Tag` objects with `name` and `description`.

Callers should depend on iteration over `store.entities`, not on random indexing — the backing store may change.

## Scripts

TODO: validate — dangling refs, invalid statuses, missing required fields.

TODO: next-id — next available ID for a given entity type.

TODO: drift — spec-code drift report for specs with `paths`.

TODO: search — query entities by tag, status, or relationship. Prints `(none)` when no matches.

TODO: list — list entities with optional grouping and sorting. Prints `(none)` when no matches.

## Anticipated Changes

- Per-script specs when complexity warrants it.
- Alternative discovery backends (SQLite, cached index) behind the `EntityStore` interface.

## Dangers

- Tools that silently pass on invalid input create false confidence in worklog integrity.
- Drift detection that produces too many false positives gets ignored.
- `EntityStore` callers that assume `list` semantics (indexing, `len()`) will break when the backend changes.
