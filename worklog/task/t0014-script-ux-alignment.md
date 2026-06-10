+++
id = "t0014"
title = "Align script UX: archive handling and blocked_by queries"
tags = ["tooling"]
status = "pending"
modifies = ["s0010", "s0018"]
+++

# Align script UX: archive handling and blocked_by queries

search.py always includes archived tasks (no flag) while list.py excludes them unless `--archived`; the relationship table advertises `blocked_by` but no script answers "what does this task block."

## Scope

- search.py: exclude archive by default, add `--archived` (match list.py).
- Add a reverse `blocked_by` query (tasks blocked by a given task).
- Define `--group-by status` output for status-less entity types.
- Update the SKILL.md scripts table. Tests before implementation (s0017).
