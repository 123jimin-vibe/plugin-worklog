+++
id = "t0030"
title = "Gate worklog creation on the project using the methodology"
status = "done"
tags = ["methodology"]
modifies = ["s0001", "s0018"]
priority = 0
+++

# Gate worklog creation on the project using the methodology

User-directed. The artifact's init instruction read "Root: `worklog/`. If absent,
create ..." — unconditional. The skill's own trigger phrases are generic (plan
work, track progress, create task), so it activates in projects that have never
adopted the methodology, and the instruction then tells the agent to scaffold a
worklog nobody asked for. Absence of the root is a signal about the project, not
a task to perform.

## Scope

- s0001 gains the rule. Edits flow specs to artifact (s0018 Dangers), and
  adoption is a methodology-level rule, not a composition one.
- The artifact's init line gates on it, in the register s0018 prescribes.
- s0018 itself: confirm, do not edit. Its Structure entry already covers "root
  directory, init instruction" generically, and its Source Mapping already
  routes the Worklog section to s0001.

## Constraints

- The gate must not fire when the user asked for the setup. Without that
  qualifier the clause trades one pitfall for another — s0019 S2, approval
  re-requested unnecessarily, is an observed overcorrection with an exam
  regression behind it. s0021 names dropping a necessary condition as a bug, not
  a saving.

## Outcome

- s0001 gained an Adoption section: the methodology is opt-in, `worklog/` is the
  only signal a project opted in, a missing root means the project may not use
  the methodology rather than that a worklog is owed, and creating one is an
  adoption decision gated on the user unless they requested the setup.
- Artifact clause: "Root: `worklog/`. Absent => project may not use this
  methodology; unless setup was requested, ask before creating ...". Telegraphic,
  no emphasis, ASCII implication — conforms to s0018 Composition Principles.
- s0018 confirmed unchanged, as scoped.
- Measured (s0021): clause 39 -> 53 claude, 30 -> 44 o200k. Whole artifact
  2014 -> 2028 claude, 1782 -> 1796 o200k. Cost +14 either tokenizer.

## Verification not performed

s0018 Verification is unfulfilled and this task does not claim otherwise. No
comprehension probe ran and no exam ran; the change ships on user direction, not
on measurement.

Two consequences to carry forward:

- The clause has no watching question. Every exam seeds a populated fictional
  worklog, so none of them exercises an absent root. A future compression round
  applying the measured-preventing-power criterion would read this clause as
  mechanism-unmapped and cut it. Its protection is its s0001 home and this
  record, not evidence.
- Authoring an exam question for an absent root — does the agent ask, or
  scaffold? — would close both gaps at once, and would also supply the watcher
  the criterion wants.
