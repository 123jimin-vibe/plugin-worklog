+++
id = "s0012"
title = "Entity: Task"
tags = ["entity", "methodology"]
+++

# Entity: Task

Atomic unit of work. Tracks what is being done, why, and what it affects.

## Location

- Active: `worklog/task/`
- Archived: `worklog/archive/task/`

## Frontmatter

TOML fenced with `+++`. Required fields:

| Field        | Type       | Description                                              |
|--------------|------------|----------------------------------------------------------|
| `id`         | string     | Unique identifier, format `t` + digits (e.g. `t0001`).  |
| `title`      | string     | Human-readable name.                                     |
| `tags`       | string[]   | Classification (e.g. `bugfix`, `greenfield`).            |
| `status`     | string     | One of: `pending`, `active`, `done`, `blocked`, `cancelled`. |
| `modifies`   | string[]   | Spec IDs whose governed behavior this task touches. May be empty for chore tasks outside all spec-governed behavior. |
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

Free-form markdown below frontmatter. Used for scope description, findings (investigation), and notes accumulated during work.

## Creation

1. Identify work to be done.
2. Define scope — what changes, which specs are affected.
3. Set `modifies` to affected spec IDs. Use empty `modifies` only for chores that touch no spec-governed behavior.
4. User confirms scope.
5. Status starts as `pending`.

## Re-scoping

When scope changes mid-flight: update body and `modifies`, get user confirmation if scope expanded. If the task has grown too large, split it.

Task scope is subordinate to the governing spec. When findings conflict with the spec, adjust task scope — not the spec. If the spec is suspected wrong, ask the user. Record the resolution via a decision if the spec changes.

## Archiving

When status reaches `done`: move file to `worklog/archive/task/`. Before moving, the agent verifies the governing spec is still consistent with the completed work — this check is not delegatable.

## Cancelling

When work is abandoned (requirements changed, cost exceeds benefit, feature unnecessary, approach wrong): set status to `cancelled`. A decision record is recommended when cancellation carries non-trivial context (requirement change after work began, design flaw discovered, cost/benefit abandonment) but is not required. A brief note in the task body explaining why is always sufficient. Cancelled tasks may be archived if they contain useful findings; otherwise deleted.

## Forbidden

- Cancel without any explanation (at minimum, note the reason in the task body).
- Point `modifies` at a nonexistent spec.
- Change spec-governed behavior without the governing spec in `modifies`.
- Present unapproved scope as decided.

## Anticipated Changes

- `type` field (greenfield, bugfix, refactor, investigation, chore, hotfix) for workflow classification.
- `triggered_by` field for external references (issue tracker, security advisory).
- Urgency marker to distinguish hotfix tasks from normal tasks.
- Originated-from link back to investigation tasks that spawned follow-up work.

## Dangers

See s0019 (Agent Pitfalls).
