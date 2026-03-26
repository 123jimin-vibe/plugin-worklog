+++
id = "s0006"
title = "Workflow: Refactor"
tags = ["workflow", "methodology"]
+++

# Workflow: Refactor

Restructuring without behavioral change.

## Flow

1. **Identify motivation** — coupling, duplication, maintainability.
2. **Create task** — scope: what moves, what stays, what invariants hold.
3. **Baseline** — verify existing tests pass before changes.
4. **Restructure incrementally**. After each step: tests pass, no behavioral change.
5. If implementation-coupled tests break despite no behavioral change → **update tests**.
6. **Update spec** if component boundaries changed.
7. **Archive task**.

Branches:
- Refactoring reveals latent bug → create separate task for the bug.
- Scope creeps ("while I'm here") → split into separate task(s) or resist.
- Cost exceeds benefit → abandon + create decision.

## Forbidden

- Behavioral changes smuggled in as "refactoring."
- Refactoring without test coverage to verify behavioral preservation.

## Dangers

- Behavioral change disguised as structural — the boundary is ambiguous during refactoring.
- Scope creep: adjacent changes that should be separate tasks.
- Refactoring areas with insufficient test coverage risks silent breakage.
