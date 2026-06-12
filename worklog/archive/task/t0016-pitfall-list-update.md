+++
id = "t0016"
title = "s0019: add observed pitfalls from real-world usage"
tags = ["quality"]
status = "done"
modifies = ["s0019"]
+++

# s0019: add observed pitfalls from real-world usage

Real-world worklogs surfaced failure modes s0019 doesn't list and contradict some "Observed: No" entries.

## Scope

New entries, each with severity and pressure mechanism:

- **State write-back omission** — current state recorded only in task body, decision, or docs; specs keep describing the old state. Observed: vocaroll t0004; new.r-g.kr t0008, t0006. Check against T4 first — same pitfall through a different entity must merge (s0019 constraint).
- **Comment narration** — task/spec context restated in code comments instead of referenced. Observed: new.r-g.kr t0012.
- **Context-bound naming** — public names that need the defining module's context to read. Observed: new.r-g.kr t0012 (bare "catalog" for i18n message sets).
- **Spec register drift** — documentation/marketing voice, status sections, history recounting in spec bodies. Observed: new.r-g.kr t0015.
- **Script path invention** — invoking `<repo>/worklog/scripts/*` or `<repo>/scripts/*` instead of the plugin's script directory. Observed: user report across projects.

Also: re-evaluate T4's "Observed: No" against vocaroll t0004, and record the S6 wording's happy-create over-caution (exam regression) in the relevant entry.

## Outcome

- Added S9 (spec register drift), T7 (state write-back omission — checked against T4: distinct mechanism, recording locus vs skipped check; T7 cell documents the boundary), X7 (comment narration), X8 (context-bound naming), X9 (script path invention). Severities: T7 Must; S9/X7/X8 Medium; X9 Low.
- T4 Observed flipped to Yes (vocaroll t0004); S2 generalized to cover re-asking on already-stated items and flipped to Yes (happy exam over-caution regression).
- Severity rows normalized to the legend vocabulary (Better → Medium) and tier-grouped.
- S6 widened during this session's exam iteration: same pitfall through decisions (fabricated rationale/consequences), with exam evidence in Observed.
