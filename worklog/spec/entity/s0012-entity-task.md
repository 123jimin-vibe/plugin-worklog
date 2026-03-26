+++
id = "s0012"
title = "Entity: Task"
tags = ["entity", "methodology"]
+++

# Entity: Task

Atomic unit of work. Tracks what is being done, why, and what it affects.

## Location

- Active: `worklog/task/`
- Archived: `worklog/task/archive/`

## Frontmatter

TOML fenced with `+++`. Required fields:

| Field        | Type       | Description                                              |
|--------------|------------|----------------------------------------------------------|
| `id`         | string     | Unique identifier, format `tNNNN`.                       |
| `title`      | string     | Human-readable name.                                     |
| `tags`       | string[]   | Classification (e.g. `bugfix`, `greenfield`).            |
| `status`     | string     | One of: `pending`, `active`, `done`, `blocked`.          |
| `modifies`   | string[]   | Spec IDs this task changes behavior under. May be empty for chore tasks that touch no spec. |
| `blocked_by` | string[]   | Task IDs that must complete first. Optional — omit when not blocked. |

## Status Lifecycle

```
pending → active → done → (archived)
              ↘ blocked → active
any status → cancelled → (deleted or kept with decision)
```

- `pending` — created, not yet started.
- `active` — work in progress.
- `blocked` — waiting on another task (`blocked_by`). Returns to `active` when unblocked.
- `done` — complete. Move to `archive/`.
- `cancelled` — work abandoned. Accompanied by a decision record.

## Body

Free-form markdown below frontmatter. Used for scope description, findings (investigation), and notes accumulated during work. Mark unapproved or planned items with `TODO`.

## Creation

1. Identify work to be done.
2. Define scope — what changes, which specs are affected.
3. Set `modifies` to affected spec IDs. Use empty `modifies` only for chores that touch no spec-governed behavior.
4. User confirms scope.
5. Status starts as `pending`.

## Re-scoping

When scope changes mid-flight: update body and `modifies`, get user confirmation if scope expanded. If the task has grown too large, split it.

## Forbidden

- Archive a hotfix task without a linked decision record (post-mortem).
- Cancel without a decision record explaining why.
- Point `modifies` at a nonexistent spec.
- Work that changes spec-governed behavior without a covering spec in `modifies`.
- Present unapproved scope as decided.

## Anticipated Changes

- `type` field (greenfield, bugfix, refactor, investigation, chore, hotfix) for workflow classification.
- `triggered_by` field for external references (issue tracker, security advisory).
- Originated-from link back to investigation tasks that spawned follow-up work.

## Dangers

- Tasks with empty `modifies` that actually change spec-governed behavior escape governance silently.
- Archiving without verifying the spec is still consistent with the completed work.
- Hotfix tasks look identical to normal tasks — no urgency signal.
