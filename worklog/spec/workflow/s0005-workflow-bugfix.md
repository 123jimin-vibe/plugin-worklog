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

## Methodology Evaluation

Potential agent mistakes:
- Fixes the symptom without identifying root cause.
- Writes regression test after the fix, so it never proves it catches the bug.
- Doesn't file a separate task when a bug is found during unrelated work.

Gaps:
- No relationship from task to external bug report or issue tracker. Tasks have `modifies` (spec) and `blocked_by` (task) but no `triggered_by` or external reference field.
- Regression test has no traceability back to the spec it validates.
- No enforcement of test-before-fix ordering.

Tooling/hooks:
- validate.py: bugfix tasks reference a spec via `modifies`.
- Hook: warn if task is archived without a linked regression test.
