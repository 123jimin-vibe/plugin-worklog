+++
id = "s0013"
title = "Entity: Decision"
tags = ["entity"]
paths = ["worklog/decision/**"]
+++

# Entity: Decision

Permanent record of why a choice was made. Decisions are append-only — they are never edited or archived, only superseded by a new decision.

## Location

`worklog/decision/`

## Frontmatter

TOML fenced with `+++`. Required fields:

| Field        | Type       | Description                                           |
|--------------|------------|-------------------------------------------------------|
| `id`         | string     | Unique identifier, format `dNNNN`.                    |
| `title`      | string     | Human-readable name.                                  |
| `relates_to` | string[]   | Spec IDs this decision concerns.                      |

Optional fields:

| Field        | Type       | Description                                           |
|--------------|------------|-------------------------------------------------------|
| `supersedes` | string[]   | Decision IDs this decision replaces.                  |

## Body

Free-form markdown below the frontmatter. Should answer:

- **Context** — what situation prompted the decision.
- **Choice** — what was decided.
- **Rationale** — why this option over alternatives.
- **Consequences** — expected impact, trade-offs accepted.

## Relationships

| Direction | Relationship  | Target   |
|-----------|---------------|----------|
| Outbound  | `relates_to`  | Spec     |
| Outbound  | `supersedes`  | Decision |
| Inbound   | `supersedes`  | Decision |

Inbound `supersedes` is not stored on the superseded decision. Reverse lookup via grep.

## Allowed Actions

| Action | When |
|--------|------|
| Create | Non-trivial choice made, design flaw discovered, post-mortem required, requirement changed, cost/benefit abandonment. |

This is the only allowed action. Decisions are immutable after creation.

## Forbidden Actions

- Edit. A decision that needs correction is superseded by a new decision, never modified in place.
- Archive. Decisions are permanent records with no lifecycle.
- Delete. Historical record must be preserved.

## Mandatory Creation

A decision record is **required** (not discretionary) in these cases:

- Hotfix deployed (post-mortem: root cause, what went wrong).
- Hotfix bypasses normal review (documents why).
- Task cancelled due to requirement change.
- Refactor abandoned because cost exceeds benefit.

## Anticipated Changes

- Structured fields for context/choice/rationale/consequences instead of free-form body.
- Link from decision back to the task that prompted it.

## Dangers

- Skipping decision records for hotfixes because the fix is already deployed — the post-mortem is the point.
- Editing a decision instead of superseding it destroys the historical record.
- Decisions without `relates_to` float free of spec governance and become hard to discover.
