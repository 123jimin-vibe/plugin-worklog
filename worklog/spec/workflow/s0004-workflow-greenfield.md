+++
id = "s0004"
title = "Workflow: Greenfield"
tags = ["workflow", "methodology"]
+++

# Workflow: Greenfield

New feature development.

## Flow

1. **Survey** — check existing code, specs, and dependencies for overlap.
2. **Draft spec** — observable behavior, constraints, dangers. `TODO` markers on uncertain items.
3. **Review spec** — user reviews. Revise until approved.
4. **Create task(s)** — each with `modifies` pointing to the spec. Confirm scope with user.
5. **Write tests** from spec. If spec gaps surface → revise spec (step 3).
6. **Implement** until tests pass. If spec needs adjustment → update spec (user approval) → update affected tests.
7. **Record decision** if a non-trivial choice was made.
8. **Verify** spec still consistent with result. Update if needed.
9. **Archive task**.

Branches:
- Spec incomplete at write time → update spec, re-scope tasks.
- Design flaw discovered → update spec + create decision.
- Blocked by other work → set `blocked_by` on task.
- Requirement changed → cancel task(s) + create decision.

## Forbidden

- Spec's observable behavior modified without user approval.
- Test agent receiving implementation details from parent agent.

## Dangers

- Agent creates too-narrow specs (one per function) instead of extending existing spec.
- Discussion treated as approval; spec created without explicit confirmation.
- Subagent test prompts over-specified, leaking implementation knowledge.
- Survey step skipped, existing functionality reimplemented.
