+++
id = "t0031"
title = "Audit brainstorm coverage before removing the corpus"
status = "active"
tags = ["research", "methodology"]
modifies = ["s0003"]
priority = 0
+++

# Audit brainstorm coverage before removing the corpus

Investigation preceding removal of `brainstorm/`. Output is knowledge: which
issues raised in the corpus no specification addresses. Nothing is deleted under
this task.

An issue is any problem, requirement, constraint, design question, or failure
mode the corpus raises. Per issue the question is whether a spec's contents
address it — not whether a spec mentions the same topic.

## Scope

- Inventory the corpus and classify every issue: covered, partially covered
  (a spec addresses it but drops a condition), uncovered, or obsolete.
- Identify what would dangle on removal: specs, tasks, or artifacts that point
  into `brainstorm/` and would break.
- Findings in this body. Promotion of uncovered issues into specs is behavioral
  and out of scope.

## Known dangling references

Established before the audit ran:

- s0021 mandates recording compression attempts in the ledger under
  `brainstorm/prompt-engineering/`. Removing the corpus deletes the register a
  spec requires be written to.
- t0029 plans to return D1's misfiled observation to `brainstorm/case-study-bfc.md`,
  where s0003 governs it. Removal invalidates that plan.
- s0003 governs `brainstorm/**` and describes nothing else. Removing the corpus
  retires the spec, which s0011 gates behind a decision record.

## Findings
