+++
id = "t0026"
title = "Compress SKILL.md round 3: telegraphic register + pseudo-code"
status = "done"
tags = ["methodology", "quality"]
modifies = ["s0018"]
+++

# Compress SKILL.md round 3: telegraphic register + pseudo-code

User-directed paradigm shift: treat SKILL.md as program code in natural
language, not prose. Telegraphic register (drop articles/copulas/grammatical
scaffolding), logical connectives (`⇒`, `≠`, `=`), numbered pipeline for the
archive protocol. Every condition and qualifier survives; only grammar is
removed.

## Constraints

- Zero ambiguity introduced — telegraphic text is exactly where a cold reader
  may misparse, so the weak-model probe set gates before exams (false-belief
  discipline: parse behavior is measured, never assumed).
- All conditions/qualifiers survive: claims qualifier, "Never `--confirm`
  first", genuinely-undecided, stub honesty, chore row, script negative,
  marker-verification rule (t0025, landed immediately before this round).
- Symbol conventions: `→` = state transition / forward link (existing usage),
  `⇒` = implication, `≠`/`=` = (non-)equivalence. Probe for misparse.
- Exam gate vs c2 snapshots (`results/c2/`); regression attributable to a
  telegraphic transform reverts that transform.

## Outcome

- 2000 → 1935 cl100k; 2239 → 2180 claude (net incl. t0025's +~16). Cumulative
  campaign: 2254 → 1935 cl100k (−14.2%); 2519 → 2180 claude (−13.5%,
  −339/session).
- Tokenizer-divergence trap found and fixed: unicode `⇒ ≠ ≥` cost 3-5× in the
  Claude tokenizer vs ASCII `=> != >=` while cl100k shows parity — first draft
  saved −79 cl100k but only −23 claude; ASCII swap recovered 52. Recorded in
  compress.jsonl and s0021 Dangers ("measure the tokenizer you deploy on").
- Gates: probes 11/11 (telegraphic register parses clean on haiku); five exams
  behavior-neutral-or-better vs c2 — zero notation misparses, no new
  ask-stalls, numbered archive pipeline executes correctly under both clean
  and drift conditions; precedence Q2 strengthened to full pass.
- Watch items recorded (not patched — unmeasured tail-end edits forbidden):
  X7 comment-honesty trade, pipeline step-2 escape hatch under attention
  redirection, one isolated `next_id.py` arg slip.
- Nothing reverted. Remaining mass is tables + one TOML example + frontmatter
  + ~750 telegraphic rules; further reduction = removing rules (scope
  decision, user's call).
