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
| `modifies`   | string[]   | Spec IDs this task changes behavior under. May be empty for chore tasks that touch no spec (e.g. CI config, dependency updates). |
| `blocked_by` | string[]   | Task IDs that must complete before this task can proceed. Optional — omit when not blocked. |

## Status Lifecycle

```
pending → active → done → (archived)
              ↘ blocked → active
any status → cancelled → (deleted or kept with decision)
```

- `pending` — created, not yet started.
- `active` — work in progress.
- `blocked` — waiting on another task (`blocked_by`). Returns to `active` when unblocked.
- `done` — complete. Task is moved to `archive/`.
- `cancelled` — work abandoned (requirements changed, cost exceeds benefit, feature unnecessary, approach wrong). Accompanied by a decision record. Cancelled tasks may be archived if they contain useful findings; otherwise deleted.

## Body

Free-form markdown below the frontmatter. Used for:

- Scope description.
- Findings (investigation workflow).
- Notes accumulated during work.

Unapproved or planned items must be marked `TODO`. Do not present speculative scope as decided.

## Relationships

| Direction | Relationship    | Target   |
|-----------|-----------------|----------|
| Outbound  | `modifies`      | Spec     |
| Outbound  | `blocked_by`    | Task     |
| Inbound   | `blocked_by`    | Task     |

Inbound `blocked_by` is not stored on the blocking task. Reverse lookup via grep.

## Allowed Actions

| Action  | When |
|---------|------|
| Create  | New unit of work identified. |
| Update  | Re-scope, change status, set/clear `blocked_by`, add findings. |
| Archive | Status reaches `done`. File moves to `archive/`. |
| Cancel  | Work abandoned for any reason. Accompanied by a decision record. |

## Precedence

Task scope is subordinate to the governing spec. When findings or implementation reveal a conflict:

1. Spec is authoritative — task scope adjusts to match, not the reverse.
2. Spec suspected wrong — ask user, never silently override. Record the resolution via a decision if the spec changes.

## Forbidden Actions

- Archive a hotfix task without a linked decision record (post-mortem).
- Cancel without a decision record explaining why.
- Modify `modifies` to point at a nonexistent spec.
- Work on a task that changes spec-governed behavior without a covering spec in `modifies`.
- Present unapproved or speculative scope as decided. Discussion ≠ approval — items from brainstorming or unconfirmed requirements must carry a `TODO` marker.

## Anticipated Changes

- `type` field (greenfield, bugfix, refactor, investigation, chore, hotfix) for workflow classification.
- `triggered_by` field for external references (issue tracker, security advisory).
- Urgency marker to distinguish hotfix tasks from normal tasks.
- Originated-from link back to investigation tasks that spawned follow-up work.

## Dangers

- Tasks with empty `modifies` that actually change spec-governed behavior escape governance silently. Empty `modifies` is valid for chores — dangerous when misused for behavioral work.
- Archiving without verifying the spec is still consistent with the completed work.
- Hotfix tasks look identical to normal tasks — no urgency signal for tooling or agents.
