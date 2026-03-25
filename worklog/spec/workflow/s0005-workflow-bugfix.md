+++
id = "s0005"
title = "Workflow: Bug Fix"
tags = ["workflow"]
+++

# Workflow: Bug Fix

Correcting defective behavior.

## Flow

1. Bug reported (user, CI, monitoring).
2. Triage: severity, affected spec, spec violation vs. spec gap.
3. Task (create) — reproduce and identify root cause.
4. Regression test (write) — must fail before fix.
5. Fix until test passes.
6. Spec (update) if bug reveals a gap.
7. Task (archive).

Branches:
- Root cause in different component → task scope expands, additional spec(s) (update).
- Bug found during unrelated task → new task (create), don't derail current work.
- Bug is instance of general problem → fix the general case, not just observed failure.
- Not worth fixing now → document, defer, track as task (blocked or pending).
- Fix requires design change → spec (update or create) + decision (create).

## Forbidden

- Distorting code to route around a bug instead of fixing it.
- Fixing only the observed failure without evaluating whether it's a general problem.
- Regression test written after the fix (must fail before fix to prove it catches the bug).
- Closing without documenting the underlying issue.

## Anticipated Changes

- Task field for external bug report or issue tracker reference (`triggered_by`).
- Regression test traceability back to the spec it validates.
- Enforcement of test-before-fix ordering.
- TODO: validate.py — bugfix tasks reference a spec via `modifies`.
- TODO: Hook — warn if task is archived without a linked regression test.

## Dangers

- Symptom fixed without identifying root cause.
- Regression test written after the fix — never proves it catches the bug.
- Bug found during unrelated work not filed as separate task.
