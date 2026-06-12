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
| `priority`   | int        | Optional. Triage rank for the backlog view (s0016): non-negative, 0 most urgent. Absent = untriaged. |

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

Completion is a write-back, not a check. When status reaches `done`: fold the new current state into every spec in `modifies` — or confirm the existing wording already covers it — and remove `UNIMPLEMENTED` markers the work resolved. The write-back asserts only what the delivered work verifiably does, not what the task intended — re-read the governing spec and the delivered work; where delivery is stubbed or partial, the spec keeps or gains markers instead of asserting the behavior. Only then move the file to `worklog/archive/task/`.

Archived tasks and decisions are history, not reference: future agents read specs, so state recorded only in a task body, a decision, or external docs is lost. A constraint introduced by a decision is also written into the spec; the decision keeps the why.

The write-back is not delegatable and not skippable, even if the user claims to have reviewed or already updated the specs. The `archive.py` script (s0010) surfaces each governing spec and its drift — run it without `--confirm` first; confirm only after the write-back.

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
- Originated-from link back to investigation tasks that spawned follow-up work.

## Dangers

See s0019 (Agent Pitfalls).
