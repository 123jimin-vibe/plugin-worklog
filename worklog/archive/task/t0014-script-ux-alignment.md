+++
id = "t0014"
title = "Align script UX: archive handling and blocked_by queries"
tags = ["tooling"]
status = "done"
modifies = ["s0010", "s0018"]
+++

# Align script UX: archive handling and blocked_by queries

search.py always includes archived tasks (no flag) while list.py excludes them unless `--archived`; the relationship table advertises `blocked_by` but no script answers "what does this task block."

## Scope

- search.py: exclude archive by default, add `--archived` (match list.py).
- Add a reverse `blocked_by` query (tasks blocked by a given task).
- Define `--group-by status` output for status-less entity types.
- Update the SKILL.md scripts table. Tests before implementation (s0017).

## Outcome

search.py now excludes archived entities by default (matching list.py) with `--archived` to opt in, and adds `--blocked-by ID` (tasks waiting on a given task, normalized like the other ID filters). list.py's `--group-by status` for status-less entities (specs/decisions under `(no status)`) was already correct; locked it with a test. s0010 and the SKILL.md scripts table updated. The pre-existing archived-search tests, which asserted the old always-include behavior, were rewritten to the new default-exclude contract.
