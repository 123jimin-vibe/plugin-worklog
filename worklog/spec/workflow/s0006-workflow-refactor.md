+++
id = "s0006"
title = "Workflow: Refactor"
tags = ["workflow"]
+++

# Workflow: Refactor

Restructuring without behavioral change.

## Flow

1. Motivation identified (coupling, duplication, maintainability).
2. Task (create) — scope: what moves, what invariants hold.
3. Verify existing tests pass before changes.
4. Incremental restructuring.
5. All tests pass — no behavioral change.
6. Spec (update) if component boundaries changed.
7. Task (archive).

Branches:
- Tests coupled to implementation details break despite no behavioral change → tests (update).
- Refactoring reveals latent bug → task (create) for the bug separately.
- Scope creeps ("while I'm here") → split into separate task(s) or resist.
- Cost exceeds benefit → abandon + decision (create).

## Forbidden

- Behavioral changes smuggled in as "refactoring."
- Refactoring without test coverage to verify behavioral preservation.

## Methodology Evaluation

Potential agent mistakes:
- Introduces behavioral changes under the label "refactoring."
- Scope creep: adjacent changes that should be separate tasks.
- Refactors areas with insufficient test coverage, risking silent breakage.

Gaps:
- No way to verify "no behavioral change" beyond existing tests, which may be incomplete.
- No distinction between structural spec changes (allowed) and behavioral spec changes (forbidden in this workflow).

Tooling/hooks:
- Hook: flag spec edits during a refactor task for user review (structural vs. smuggled behavioral change).
