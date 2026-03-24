+++
id = "s0004"
title = "Workflow: Greenfield"
tags = ["workflow"]
+++

# Workflow: Greenfield

New feature development.

## Flow

1. Spec (create) — observable behavior, constraints, dangers.
2. Task(s) (create) — each with `modifies` pointing to the spec.
3. Tests (write) from spec, before implementation.
4. Implement until tests pass.
5. Spec (update) if implementation reveals adjustments.
6. Decision (create) if non-trivial choice was made.
7. Task (archive).

Branches:
- Spec incomplete at write time → spec (update) mid-flight, task(s) (re-scope).
- Design flaw discovered → spec (update) + decision (create).
- Blocked by other work → task (set `blocked_by`).
- Requirement changed → task(s) (cancel) + decision (create). Spec rewritten or marked obsolete.
- Existing code partially solves problem → reuse, don't reimplement.

## Forbidden

- Implementation without a covering spec.
- Implementation before tests.
- Spec's observable behavior modified without user approval.
- Tests written from implementation rather than spec.
- Test agent receiving implementation details from parent agent.

## Methodology Evaluation

Potential agent mistakes:
- Creates too-narrow specs (one per function) instead of extending existing spec.
- Treats discussion as approval; creates spec without explicit confirmation.
- Over-specifies subagent test prompts, leaking implementation knowledge.
- Skips survey step, reimplements existing functionality.

Gaps:
- No spec-to-test traceability. Can't verify test coverage against spec without manual audit.
- `paths` doesn't distinguish governance from behavioral extension. Drift detection misses reference docs that introduce untested behavior.
- No enforcement that spec exists before implementation starts.

Tooling/hooks:
- validate.py: tasks have valid `modifies` refs; specs have required sections.
- Hook: warn on implementation without a covering spec.
