+++
id = "s0005"
title = "Workflow: Bug Fix"
tags = ["workflow", "methodology"]
+++

# Workflow: Bug Fix

Correcting defective behavior.

## Flow

1. **Reproduce** the bug.
2. **Triage** — spec violation vs. spec gap. Identify affected spec and severity.
3. **Create task** — root cause and fix approach.
4. **Write regression test** — must fail before fix.
5. **Fix** until regression test passes. If spec gap found → update spec (user approval).
6. **Generalize** — is this one instance of a broader problem? Fix the general case if so.
7. **Verify** existing tests still pass.
8. **Archive task**.

Branches:
- Root cause in different component → expand scope, update additional spec(s).
- Bug found during unrelated task → create new task, don't derail current work.
- Not worth fixing now → document, defer, track as pending task.
- Fix requires design change → update or create spec + create decision.

## Forbidden

- Distorting code to route around a bug instead of fixing it.
- Regression test written after the fix (must fail before fix to prove it catches the bug).

## Dangers

- Symptom fixed without identifying root cause.
- Regression test written after the fix — never proves it catches the bug.
- Bug found during unrelated work not filed as separate task.
