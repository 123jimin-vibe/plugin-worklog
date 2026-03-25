+++
id = "s0006"
title = "Workflow: Refactor"
tags = ["workflow", "methodology"]
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

## Anticipated Changes

- Mechanism to verify "no behavioral change" beyond existing test coverage.
- Formal distinction between structural and behavioral spec changes.
- TODO: Hook — flag spec edits during a refactor task for user review.

## Dangers

- Behavioral change disguised as structural — the boundary is ambiguous during refactoring.
- Scope creep: adjacent changes that should be separate tasks.
- Refactoring areas with insufficient test coverage risks silent breakage.
