+++
id = "t0009"
title = "Spec authoring register rules and S6 rewording"
tags = ["methodology"]
status = "done"
modifies = ["s0011", "s0018"]
+++

# Spec authoring register rules and S6 rewording

Agents write specs in documentation register: narrative status sections, history recounting, restated rules, selling adjectives (new.r-g.kr t0015 condensed exactly this). Exam side: pitfall-spec-authoring (S6/S7) still fails, while happy-create regressed — the current "write only what the user stated or approved" wording over-corrects into question-asking on clear instructions.

## Scope

- s0011 + SKILL.md: spec prose register. Every sentence binds; one rule, one place; no history, narration, or status sections in the body (git and tasks hold history); a sentence adding no behavior, constraint, or danger is cut. Concise ≠ vague — qualifiers that change behavior stay.
- Rework the S6 wording so both directions pass: write what the user stated plus its direct entailments, invent nothing, ask only when a needed behavior is genuinely undecided.

## Constraints

- No metric proxies (token targets, banned-word lists) — agents optimize the metric instead of the writing.
- No overcorrection-prone examples in rule text.
- Verify: pitfall-spec-authoring and happy-create exams both pass.

## Outcome

s0011 gained the Register section (legislation register, one rule one place, no history/status/narration) and the redrafted creation rules; SKILL.md mirrors both. Measured across four revisions (results/skill-revision-comparison.md, 2026-06-12): the over-caution direction is fixed (happy greenfield canary passes at r4 — acts, marks everything, no re-asking) and S7 marker omission is fixed; no register narration appeared in any drafted spec. **S6 placement remains open**: invented items still land in behavioral sections despite four wording levers (incl. a reverted Proposals-definition attempt that regressed the canary). Conclusion recorded in the comparison doc: S6 needs structural enforcement, not more prose.
