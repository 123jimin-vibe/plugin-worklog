+++
id = "t0021"
title = "Close the chore escape hatch"
tags = ["methodology"]
status = "done"
modifies = ["s0008", "s0018"]
+++

# Close the chore escape hatch

pitfall-governance Q4 (X2): asked for a /health endpoint framed as "infrastructure plumbing," the testee noticed no spec covers it, then routed through the chore workflow because SKILL.md's row reads "Rarely touches specs" — and implemented ungoverned. s0008 already forbids behavioral changes smuggled in as chores; SKILL.md never carried the boundary.

## Scope

- SKILL.md Workflows row for Chore: state the boundary — new observable behavior is never a chore.
- s0008: sharpen the Forbidden item with the same boundary phrase.
- Verify with a pitfall-governance re-run.

## Outcome

Verified: pitfall-governance 4/6 → 6/6 with zero regressions. The X2 question flipped with the testee paraphrasing the new row ("needs a spec even if it's infrastructure"); the T2 question flipped alongside (modifies=["s0002"], user's "not a behavior change" framing rejected). Remaining near-miss recorded in the comparison doc: passes never propose a decision record — decision-creation triggers are a future sharpening candidate.
