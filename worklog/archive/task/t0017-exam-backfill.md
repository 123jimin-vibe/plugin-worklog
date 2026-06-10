+++
id = "t0017"
title = "Exams for deferred Must/High pitfalls (X3, X4, X5, S3)"
tags = ["quality"]
status = "done"
modifies = ["s0014"]
+++

# Exams for deferred Must/High pitfalls (X3, X4, X5, S3)

t0006 deferred X3/X4/X5/S3 as hard to test in single-turn exams. Three are Must severity and S3 is High; they remain the only uncovered non-Low pitfalls.

## Scope

- Design exams within s0014's emulated-tool format — pre-baked histories can stage the multi-step setups these need (mid-task spec edit for X4, refactor framing for X5, sibling-spec contradiction for S3, test-writing with source in reach for X3).
- If a pitfall genuinely cannot be tested single-turn, record why in s0014 and propose the format extension instead of forcing a weak exam.

## Outcome

Coverage added for the deferred pitfalls, and the suite consolidated per the
reorganization directive (11 → 6 exam files, no coverage loss).

Pitfalls:
- **X5** (behavioral change disguised as refactoring) — new question in pitfall-governance:
  dropping s0001's 30-day soft-delete framed as dead-code cleanup. The spec documents the
  behavior, so the correct answer is irrefutable; the refactor framing is the pressure.
- **S3** (spec update contradicts a related spec) — new question in pitfall-spec-authoring,
  exploiting the collections(s0003)↔recipes(s0001) deletion overlap (hard cascade vs. soft-delete).
- **X3** (test agent reads source) — attributed to pitfall-precedence Q2, which already tests
  "tests from spec, not the visible diverging code"; comment sharpened to claim X3.
- **X4** (inline spec edit without approval) — not cleanly single-turn-testable: a direct
  instruction to edit reads as authorization (irrefutability problem); the real violation is a
  spontaneous mid-task edit, which needs multi-turn observation. Recorded in s0014
  "Single-turn coverage limits" with the extension it needs.

Reorg (per the NOTE):
- Merged happy-create/update/lifecycle → happy.toml (curated to the over-correction guards).
- Folded pitfall-markers (S8) into pitfall-spec-authoring (now S6/S7/S8/S3).
- Dropped pitfall-completion (completion-drift covers T3/T4/T6 under a harder, realistic
  condition) and precedence-drift (drift provably can't move reasoning-rule S5/X1 — s0014
  "What drift affects" + identical Pass/Pass in the results snapshot).
- Kept pitfall-governance, pitfall-precedence, completion-drift, pitfall-drift.

All 6 TOMLs parse. Covered now includes S3/X3/X5; X4 documented; S4/T1/D2/X6 remain (Low).
skill-revision-comparison.md marked a pre-reorg snapshot.
