+++
id = "s0007"
title = "Workflow: Investigation"
tags = ["workflow"]
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

## Methodology Evaluation

Potential agent mistakes:
- Merges prototype code without going through spec/task lifecycle.
- Doesn't document findings, losing knowledge at session boundary.
- Doesn't create follow-up tasks for discovered work.

Gaps:
- No relationship from follow-up task back to the investigation that spawned it. The follow-up has `modifies` (spec) but no "originated from investigation" link.
- No convention for investigation output format beyond "findings in task body."

Tooling/hooks:
- None critical. Investigations are lightweight by design.
