+++
id = "s0010"
title = "Tooling"
tags = ["tooling"]
paths = ["plugin/skills/worklog/script/**"]
+++

# Tooling

Scripts that automate worklog operations, bundled with the plugin at `plugin/skills/worklog/script/`. Python. Accept `-w PATH` for worklog root (default: `./worklog`). Shared logic (parsing, discovery) lives under `lib/`. Each tool gets its own spec when introduced.

No tools implemented yet.

## Anticipated Changes

- next-id: Next available ID for a given entity type.
- validate: Dangling refs, invalid statuses, missing required fields.
- drift: Spec-code drift report for specs with `paths`.
- search: Query entities by tag, status, or relationship.
- list: List entities with optional grouping and sorting.

## Dangers

- Tools that silently pass on invalid input create false confidence in worklog integrity.
- Drift detection that produces too many false positives gets ignored.
