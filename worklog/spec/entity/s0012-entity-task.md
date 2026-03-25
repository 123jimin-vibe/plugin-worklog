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
| `status`     | string     | One of: `pending`, `active`, `done`, `blocked`.          |
| `modifies`   | string[]   | Spec IDs this task changes behavior under.               |

Optional fields:

| Field        | Type       | Description                                              |
|--------------|------------|----------------------------------------------------------|
| `blocked_by` | string[]   | Task IDs that must complete before this task can proceed. |

## Status Lifecycle

```
pending → active → done
              ↘ blocked → active → done
```

- `pending` — created, not yet started.
- `active` — work in progress.
- `blocked` — waiting on another task (`blocked_by`). Returns to `active` when unblocked.
- `done` — complete. Task is moved to `archive/`.

A task may also be **cancelled** — removed from active work when requirements change. Cancellation is recorded via a decision.

## Body

Free-form markdown below the frontmatter. Used for:

- Scope description.
- Findings (investigation workflow).
- Notes accumulated during work.

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
| Cancel  | Requirements changed. Accompanied by a decision record. |

## Forbidden Actions

- Archive without reaching `done` status.
- Archive a hotfix task without a linked decision record (post-mortem).
- Modify `modifies` to point at a nonexistent spec.
- Work on a task without a covering spec in `modifies`.

## Anticipated Changes

- `type` field (greenfield, bugfix, refactor, investigation, chore, hotfix) for workflow classification.
- `triggered_by` field for external references (issue tracker, security advisory).
- Urgency marker to distinguish hotfix tasks from normal tasks.
- Originated-from link back to investigation tasks that spawned follow-up work.

## Dangers

- Tasks created without `modifies` escape spec governance entirely.
- Archiving without verifying the spec is still consistent with the completed work.
- Hotfix tasks look identical to normal tasks — no urgency signal for tooling or agents.
