+++
id = "t0019"
title = "archive.py: archive multiple tasks at once"
tags = ["tooling"]
status = "done"
modifies = ["s0010", "s0018"]
+++

# archive.py: archive multiple tasks at once

archive.py takes a single task ID. Archiving a batch of completed tasks (e.g. a
finished sprint) means invoking it repeatedly. Accept multiple IDs in one call.

## Scope

- Accept one or more task IDs positionally; a single ID behaves exactly as today.
- Gate every task first; if any cannot be archived (unknown, not a task,
  non-terminal, cancelled without explanation), report all problems and archive
  nothing — the batch is atomic. An already-archived ID is skipped with a notice,
  not treated as a failure.
- Surface governing specs deduplicated across the batch: each unique spec printed
  once, in full, with its drift and the tasks that touch it.
- With `--confirm`, move each task (git mv when tracked, plain mv otherwise).
- Duplicate IDs in the argument list collapse to one.

## Constraints

- Tests before implementation (s0017); preserve the single-ID tests.
- Update the archive.py description in s0010 and the SKILL.md scripts table.

## Outcome

archive.py takes `nargs="+"` task IDs. Gating runs over the whole batch before any
move: fatal problems (unknown, not a task, non-terminal, cancelled without a body)
abort the batch with all problems reported; an already-archived ID is skipped with a
notice rather than failing. Governing specs are deduplicated across the batch — each
unique spec printed once with its drift and the tasks that touch it — and duplicate
IDs collapse. Single-ID invocation is unchanged. s0010 and the SKILL.md scripts table
updated. Five tests added (batch move, report-only, dedup, atomic abort, duplicate IDs);
the seven single-ID tests still pass.
