+++
id = "s0007"
title = "Workflow: Investigation"
tags = ["workflow", "methodology"]
+++

# Workflow: Investigation

Research producing knowledge, not code.

## Flow

1. Question or hypothesis stated.
2. Task (create) — defines what's being investigated.
3. Research: benchmarks, prototypes, reading.
4. Findings documented in task body.
5. Outcome determines next step:
   - New work needed → task (create) or spec (create/update).
   - Design choice clarified → decision (create).
   - No action needed → nothing.
6. Task (archive).

Branches:
- Real problem is elsewhere → scope pivots, task body updated.
- Findings inconclusive → documented as-is, may be revisited.
- Prototype worth keeping → promoted to greenfield workflow with spec (create).
- Critical issue found → escalates to hotfix workflow.

## Forbidden

- Investigation code merged without a spec and proper task lifecycle.
- Findings not documented (knowledge lost at session end).

## Anticipated Changes

- Relationship from follow-up task back to the investigation that spawned it (originated-from link).
- Convention for investigation output format beyond free-form task body.

## Dangers

- Prototype code merged without spec/task lifecycle.
- Findings not documented, losing knowledge at session boundary.
- Follow-up tasks not created for discovered work.
