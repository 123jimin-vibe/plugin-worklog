+++
id = "t0013"
title = "validate.py: archive status, cancellation note, blocked_by cycles"
tags = ["tooling"]
status = "pending"
modifies = ["s0010", "s0018"]
+++

# validate.py: archive status, cancellation note, blocked_by cycles

Three s0012 rules are structurally checkable but unchecked.

## Scope

- Archived task whose status is not `done` or `cancelled` → error.
- `cancelled` task with an empty body → error (explanation is required).
- `blocked_by` cycle → error.
- Tests before implementation (s0017). Update the validate.py row in the SKILL.md scripts table.
