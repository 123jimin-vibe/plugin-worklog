+++
id = "t0007"
title = "Reframe task completion as spec write-back"
tags = ["methodology"]
status = "pending"
modifies = ["s0012", "s0018"]
+++

# Reframe task completion as spec write-back

Agents treat tasks/decisions as the durable record and leave specs describing the old state (vocaroll t0004: design shipped to docs/, spec untouched; new.r-g.kr t0008/t0006: binding constraints lived only in a decision / nowhere). Root cause: the archiving rule reads as a *check* ("verify specs are consistent") satisfiable by judgment without writing anything, and nothing states that archived tasks are write-only history.

## Scope

- s0012 Archiving: completion = fold the new current state into every spec in `modifies` (or confirm existing wording covers it) and remove resolved `UNIMPLEMENTED` markers; only then archive.
- State the asymmetry: future agents read specs; archived tasks and decisions are history, not reference. A constraint established by a decision also goes into the spec (the decision keeps the why).
- Propagate to the SKILL.md Task section.

## Constraints

- Wording per s0021: measure tokens, no restatement across sections.
- Run pitfall-completion and completion-drift exams for regressions.
