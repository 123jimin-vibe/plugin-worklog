+++
id = "s0007"
title = "Workflow: Investigation"
tags = ["workflow", "methodology"]
+++

# Workflow: Investigation

Research producing knowledge, not code.

## Flow

1. **State question or hypothesis** — what are you trying to find out?
2. **Create task** — what's being investigated, what would count as an answer.
3. **Research** — read code, benchmark, prototype, survey dependencies.
4. **Document findings** in task body as they emerge — don't wait until the end.
5. **Determine outcome**:
   - New work needed → create task or spec.
   - Design choice clarified → create decision.
   - No action needed → document why.
6. **Archive task**.

Branches:
- Real problem is elsewhere → scope pivots, update task body.
- Findings inconclusive → document as-is, may be revisited.
- Prototype worth keeping → promote to greenfield workflow with new spec.
- Critical issue found → escalate to hotfix workflow.

## Forbidden

- Investigation code merged without a spec and proper task lifecycle.
- Findings not documented (knowledge lost at session end).

## Dangers

- Prototype code merged without spec/task lifecycle.
- Follow-up tasks not created for discovered work.
