+++
id = "t0008"
title = "archive.py: archiving with forced spec read"
tags = ["tooling"]
status = "pending"
modifies = ["s0010", "s0012", "s0018"]
blocked_by = ["t0007"]
+++

# archive.py: archiving with forced spec read

The archive-time spec check is skippable because nothing routes the spec text through the agent's context. A script makes the read unskippable.

## Scope

- `archive.py <task-id>`: verify status is `done` (or `cancelled` with an explanation in the body); print each spec in `modifies` in full; run drift for those specs' `paths`. Default run only reports — `--confirm` performs the move, so the spec text is in context before the move happens.
- Move uses `git mv` for tracked files, plain `mv` otherwise.
- Tests before implementation (s0017). Add to the SKILL.md scripts table and the archiving flow from t0007.
