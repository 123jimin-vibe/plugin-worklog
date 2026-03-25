+++
id = "s0004"
title = "Workflow: Greenfield"
tags = ["workflow", "methodology"]
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

## Anticipated Changes

- Spec-to-test traceability to verify coverage without manual audit.
- `paths` distinction between governance and behavioral extension for drift detection.
- Enforcement that spec exists before implementation starts.
- TODO: validate.py — tasks have valid `modifies` refs; specs have required sections.
- TODO: Hook — warn on implementation without a covering spec.

## Dangers

- Agent creates too-narrow specs (one per function) instead of extending existing spec.
- Discussion treated as approval; spec created without explicit confirmation.
- Subagent test prompts over-specified, leaking implementation knowledge.
- Survey step skipped, existing functionality reimplemented.
