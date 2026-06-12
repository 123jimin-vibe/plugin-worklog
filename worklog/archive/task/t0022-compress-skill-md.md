+++
id = "t0022"
title = "Compress SKILL.md"
status = "done"
tags = ["methodology", "quality"]
modifies = ["s0018"]
+++

# Compress SKILL.md

SKILL.md grew 1765 → 2254 cl100k (2519 claude-opus-4-6) during the rule-revision
campaign. Verbose context degrades agent performance and raises per-session cost
(s0021). Compress wording and structure without dropping any measured rule.

## Plan

- Per-section token baseline (done: Task 825, Spec 465, Scripts 372, Workflows 171,
  Decision 147, Relationships 107, preamble+Entities 167 cl100k).
- Compress per s0021 and plugin-prompt-engineer `lab/compression` findings:
  sentence restructure and paragraph merge work (28-34%); synonym swaps, voice
  flips, and table↔list conversions don't. Known compressor blind spots to avoid
  by hand: qualifier drops, retrieval→inference wording drift, punctuation
  restructuring that creates parse ambiguity.
- Verify: fresh-reader comprehension probes (original vs. compressed, weak-model
  canary), then the exam suite against the r4 per-question baselines.
- Bookkeep attempts in `brainstorm/prompt-engineering/compress.jsonl` (s0021).

## Constraints

- No rule is dropped; only wording and scaffolding compress. Load-bearing
  qualifiers stay (compress.jsonl records the "not delegatable, not skippable"
  regression).
- An exam regression attributable to a compression lever reverts that lever.
- s0018 structure holds: section order, scripts/workflows as tables, single file.

## Outcome

- 2254 → 2097 cl100k (−7.0%); 2519 → 2344 claude-opus-4-6 (−175/session,
  confirmed in live exam input_tokens). Levers: task+decision TOML examples →
  field lists (spec example kept as sole syntax anchor); Stubs ¶ merged into
  Archiving; approval bullet and Forbidden impl-details line deduped to their
  remaining statements; Relationships diagram → inline line; minor merges.
- Verification: comprehension probes 10/10 parity (haiku, original vs.
  compressed; compressed read better twice). Exam suite behavior-neutral —
  every score delta reproduced under a same-exam r4-skill control run
  (r4-era behavior + missing in-turn forcing, not compression). Zero malformed
  frontmatter anywhere despite the removed examples.
- No lever reverted. Lever pairs + verdicts appended to
  brainstorm/prompt-engineering/compress.jsonl; full round in
  exams/entity/results/skill-revision-comparison.md ("Compression pass").
- s0018 write-back: subsection inventory wording matched to the artifact.
- Follow-up filed: t0023 (exam in-turn forcing; stalls cost attribution this
  round). Next size lever would be removing rules — a scope decision, not
  wording; left to the user.
