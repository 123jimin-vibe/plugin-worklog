+++
id = "t0013"
title = "validate.py: archive status, cancellation note, blocked_by cycles"
tags = ["tooling"]
status = "done"
modifies = ["s0010", "s0018"]
+++

# validate.py: archive status, cancellation note, blocked_by cycles

Three s0012 rules are structurally checkable but unchecked.

## Scope

- Archived task whose status is not `done` or `cancelled` → error.
- `cancelled` task with an empty body → error (explanation is required).
- `blocked_by` cycle → error.
- Tests before implementation (s0017). Update the validate.py row in the SKILL.md scripts table.

## Outcome

validate.py gained three checks: archived tasks must be terminal (`done`/`cancelled`); cancelled tasks must carry a non-empty body; `blocked_by` chains must be acyclic (DFS with self-loop detection, restricted to existing task nodes so dangling refs don't crash it). `Entity` now carries `body` (parse.py extension) to back the cancellation check. s0010 and the SKILL.md scripts table updated. Tests cover each check and its negative (terminal archived task, cancelled-with-note, acyclic chain) so the checks can't over-fire.
