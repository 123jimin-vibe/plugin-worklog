+++
id = "t0007"
title = "Reframe task completion as spec write-back"
tags = ["methodology"]
status = "done"
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

## Outcome

Three measured iterations (results/skill-revision-comparison.md, 2026-06-12): s0012 + SKILL.md now define completion as a write-back asserting only verified delivery, with the two-step archive.py protocol and the "even if the user claims to have reviewed or already updated the specs" qualifier. Measured: r2 stopped blind archiving but laundered task wording into spec text; the verified-delivery + two-step wording (r3/r4) ended false spec writes and cured the user-claim trap (happy Q6 F→P, completion-drift Q2 honest "partially delivered" downgrades). Residual: under a pre-baked self-endorsement (drift exam Q1) the stub re-check still doesn't fire — recorded as the prior-commitment limit, exam-side neutralization landed in t0018.
