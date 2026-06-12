+++
id = "t0027"
title = "Trim non-preventing prompts from SKILL.md, exam-evaluated"
status = "done"
tags = ["methodology", "quality"]
modifies = ["s0018"]
+++

# Trim non-preventing prompts from SKILL.md, exam-evaluated

User-directed: clauses identified as counterfactually non-preventing (present
while their pitfall fired), duplicated, or mechanism-unmapped are cut as
candidate c4 and evaluated against the c3 exam baselines. Groups C (escape
hatches — rule-tightening) and D (uncatalogued mechanisms — s0019 work first)
are out of scope.

## Cuts (Group A) and merges (Group B), with their watching exams

- Litmus test clause from the binding paragraph (routing to Proposals KEPT) —
  watch: spec-auth Q1 shape (disclosed vs silent binding), happy canary.
- `No antipatterns` bullet — no catalogued mechanism; exam-blind.
- X7 comments bullet + X8 names bullet — precedence Q3/Q4: already-failing
  WITH the rules; headline experiment is failure-shape without them.
- Forbidden regression-test line — verbatim twin of the Bug fix table row
  (rule survives in-file); exam-blind.
- Decision `Create when:` list — watch: governance Q1 (D1), happy Q4.
- Session-resume + Plan-in-worklog → single merged bullet — exam-blind (X6).
- Scripts preamble: location prose deduped to the template, `This section is
  authoritative.` cut (present since r1 while X9 fired; cure was
  template + negatives) — watch: X9 across all runs, probe Q7, happy Q6.

## Verdict rule

Per lever: verdict regression or worse failure shape on its watching
question(s), attributable => restore that lever; otherwise the cut stands.
Probes (11) gate before exams. Baselines: results/c3/.

## Outcome

- Final state c6: 1935 → 1782 cl100k / 2180 → 2014 claude. Campaign cumulative
  2254 → 1782 (−20.9%) / 2519 → 2014 (−505/session).
- Seven of eight cuts clean on their watchers (scripts preamble survived the
  direct X9 stress; X7's removal improved comment honesty vs every
  rule-present run; X8 counterfactual still unmeasurable — t0023 evidence
  appended there). One regression (happy Q3 ask-stall) bisected: restoring the
  litmus did NOT cure it (c5), so the litmus stays cut and its five-revision
  disclosure attribution is corrected in the comparison doc; the true
  mechanism (ask-salience after list-thinning) is fixed by a new measured
  deliver clause on the ask bullet.
- Deliver clause net: happy Q3 cured + spec-auth Q2 first-ever PASS (S7
  markers complete) + completion-drift write-back observability restored;
  approval gates verified intact; known costs recorded (one out-of-scope
  Dangers retirement in happy Q4, one false comment in precedence Q3,
  Q4 tool-stalling) — see comparison doc "Trim experiment (t0027)".
- Suite at c6 is strictly stronger than campaign start while 20% smaller.
- Bookkeeping: four entries appended to compress.jsonl (litmus saga, X7/X8
  counterfactual, scripts preamble, deliver clause).
