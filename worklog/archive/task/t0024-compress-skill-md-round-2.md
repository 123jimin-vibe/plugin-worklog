+++
id = "t0024"
title = "Compress SKILL.md round 2: emphasis + binding paragraph"
status = "done"
tags = ["methodology", "quality"]
modifies = ["s0018"]
+++

# Compress SKILL.md round 2: emphasis + binding paragraph

User-directed follow-up to t0022. Two lever groups, kept distinguishable for
bisection:

1. **Mechanical**: strip `**`/`*` emphasis markers file-wide (bold paragraph
   leads → plain or colon-label form; bullet titles → lead phrases; table-cell
   bold → plain). Emphasis pairs cost tokens without stated evidence of
   performance weight.
2. **Semantic**: restructure the Spec section's binding paragraph per user
   comments — merge the pre-write confirm-test into the write-only-stated rule
   (the test becomes the definition of "stated"); shorten the don't-re-ask
   sentence; split `UNIMPLEMENTED` semantics into its own paragraph; replace
   "marking an inferred item does not license it" with a concrete formulation.
   Smaller same-spirit merges in adjacent Spec paragraphs and Archiving.

## Constraints

- No rule dropped; "without reduction in performance" gates via comprehension
  probes (haiku, vs stored r4/c1 answers) + full exam suite vs c1 snapshots
  (`results/c1/`).
- Named regression to watch: ask-first stalls on the over-caution canary
  (happy Q1) — the r5 failure shape. "genuinely undecided" qualifier stays.
- Load-bearing verbatim phrases (archive protocol, claims qualifier, chore row,
  script template + negative) remain untouched by the semantic group.

## Outcome

- 2097 → 2000 cl100k; 2344 → 2239 claude-opus-4-6. Cumulative t0022+t0024:
  2254 → 2000 (−11.3%) / 2519 → 2239 (−280/session).
- Both lever groups landed; nothing reverted. Comprehension probes 10/10 (best
  Proposals routing of all revisions on the S6 probe). All five exams
  behavior-neutral-or-better vs the c1 snapshots: required passes held, no new
  ask-stalls on stated content (the named r5 risk), shape improvements on
  spec-auth Q1 (silent → disclosed binding), happy Q3/Q4, completion-drift Q1,
  precedence Q3.
- New confirmed gap (3 consecutive runs): markers stripped on the user's verbal
  "shipped" claim without verification → filed t0025.
- Lever pairs in brainstorm/prompt-engineering/compress.jsonl; round record in
  exams/entity/results/skill-revision-comparison.md ("Compression round 2").
- s0018 required no further write-back (structure, tables, and source mapping
  unchanged by this round).
