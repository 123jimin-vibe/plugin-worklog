+++
id = "t0029"
title = "Reconcile spec rules the artifact does not ship"
status = "pending"
tags = ["methodology", "quality"]
modifies = ["s0001", "s0013", "s0015", "s0018", "s0019"]
priority = 1
+++

# Reconcile spec rules the artifact does not ship

s0018 promises SKILL.md is self-contained — an agent follows the methodology
from it alone. Its only stated coverage floor is weaker: every Must/High
severity pitfall carries a covering rule. The cut criterion (s0018 Composition
Principles) retires clauses that map to no catalogued mechanism, so any rule
without a catalogued pitfall is structurally cuttable while its spec keeps
binding it. Recorded as an s0018 Proposal by t0028; this task resolves it.

Rules that bind on paper and are absent from the artifact agents read:

- s0001 Key Rules: no antipatterns; cold reader; comment narration; public
  naming. The cold-reader rule was never propagated to any revision of the
  artifact; the other three were cut deliberately.
- s0013: the decision-creation obligations. The artifact says what a decision is
  and how to write one. Of the two cases Required Creation would bind, the
  hotfix post-mortem already ships via the Hotfix workflow row; an abandoned
  refactor does not ship at all. The discretionary Create-when list is absent,
  which s0013's own "not every small choice needs a record" arguably licenses.
- s0015: the tag index. The artifact's init instruction never mentions it, so a
  worklog created per the artifact has no index — and `validate.py` then skips
  tag validation silently rather than failing (s0010).

Converse direction: the artifact carries one rule with no spec home — a
requested deliverable ships with open points flagged rather than withheld
pending answers. It was added as the measured fix for an ask-stall.

## The pitfall route for the decision-creation half

Catalogue "decisions not created when they should be" as its own pitfall: that
gives the obligation a mechanism, clears the s0018 cut criterion, and fires the
s0018 update trigger at Must or High.

The route does not need an admissible incident. s0019 carries five rows with
`Observed: No.` — S5 and X5 rated Must, X2 rated High — because severity is
damage times persistence keyed to visibility, not to whether anyone has caught
it happening. So the entry is well-formed with `Observed: No.` and `Rule
violated` pointing at s0013 Required Creation, severity argued from visibility:
an uncreated decision leaves nothing to inspect, strictly less visible than a
stale spec (T7, Must).

Required Creation already binds one case, which is enough for a well-formed
column, so nothing blocks the entry. One correction goes with it, and one piece
of work runs alongside it.

- Strip the inverse observation from D1's `Observed` cell (see below). Structural,
  and correct on its own merits.
- Reconcile s0009 into s0013 Required Creation. Independent of the route, not a
  prerequisite for it. Behavioral, needs approval. Carries a snag: s0013's "The
  hotfix itself is not a decision" is unscoped, so adding a post-mortem entry
  while leaving that clause makes the spec deny the record it just required.
  Scope it to the fix action versus the preventive measure.

Direction of that reconciliation is pre-settled on lopsided evidence: s0009
asserts the post-mortem obligation three times — mandatory in its flow, forbidden
to omit, and a Danger about skipping it once deployed — and the artifact already
ships it as mandatory in the Hotfix row, against one s0013 bullet describing a
different record. So s0013 gives, and `modifies` is scoped accordingly.

If the ruling inverts and hotfix post-mortems are not required, the fix inverts
with it: s0009's flow step, Forbidden line, and Danger all need softening, the
artifact's Hotfix row goes with them, and s0009 joins `modifies` under s0012
Re-scoping before any of it is touched.

Drafting constraint. s0019 forbids an entry near-identical to an existing one,
and its worked example is this exact shape — "hotfix archived without decision"
versus "skipped decision for hotfix", one failure seen through two entities. So
frame the entry once at the Required Creation level, with `Rule violated` citing
the section rather than an individual bullet; framed per-trigger it splits into
precisely those duplicates. Nothing collides today: the decision table holds only
D1 and D2, and T7 covers state recorded in the wrong place rather than rationale
never recorded at all.

What actually returns to the artifact is narrow: a required-creation rule
covering the mandatory triggers, not the full Create-when list. Of those, the
hotfix post-mortem already ships in the Hotfix workflow row, and the recommended
tier is partly represented by the cancelled-task clause. Net artifact change is
one clause — an abandoned refactor requires a decision. The general case, an
ordinary feature's rationale lost, stays guidance-only and unenforceable under
every exit; promoting it would make "non-trivial choice made" binding in every
workflow, a far larger behavioral change than this task carries.

The antipatterns rule has no route at all. Catalogueing it would clear the cut
criterion but fail s0018 Verification, which requires every lever to name the
questions watching it — that rule was exam-blind in both directions. It needs an
exam question authored first.

## s0019 cataloguing defects

All four descriptive. Two of them — X4 and T6 — put a provenance where a rule
belongs, which is the shape that matters: s0018's coverage floor asserts every
Must and High pitfall carries a covering rule, and these two rows give the reader
nothing to check that assertion against. The obligation itself is satisfied; both
have a real covering rule that was never written into the column. So this is a
checkability defect, not a coverage breach — worth fixing precisely because that
floor is the clause the whole coverage argument rests on.

Same symptom, different root causes, so different fixes.

- **X4 (Must)** — supply a link. `Rule violated` reads "v1 lesson", which points
  at the research corpus's own Limitations-of-Worklog-v1 section. Research cannot
  be violated, so this cell never named a rule at all. The covering rule is s0011
  Updating's behavioral-requires-approval gate, surfaced in the artifact's
  approval clause and its Forbidden line on modifying spec behavior during task
  work. Cite both.
- **T6 (High)** — repair a link. `Rule violated` reads "s0012 observed failure",
  and s0019 broke it itself: s0019 consolidated pitfalls previously scattered
  across entity specs under Dangers and Observed Agent Failure Modes, so s0012's
  Dangers now says only "See s0019" and the section this cell cites no longer
  exists. Correct when written, stale on landing. The covering rule is s0012
  Archiving's remove-resolved-markers sentence plus s0011 Updating's
  marker-removal rule, surfaced in the artifact's write-back clause.

Every other row names a spec and section: S3 cites s0011 Dangers, T1 cites s0012
lifecycle, T7 cites s0012 Archiving, D1 cites s0013 Forbidden, X3 and X5 cite the
artifact's Forbidden list. Conform these two to that convention.

One borderline cell passes and must be left alone: T3 cites "SKILL.md stubs
rule", which names a rule rather than a section but resolves to the artifact's
never-present-stubs-as-complete clause. Checkable, so not a third defect.

The other two are evidence defects, not column defects.

- **D1 (High)** — the only row whose evidence is not an instance of its own
  pitfall, as its own "(inverse)" qualifier concedes. The pitfall is
  non-trivial-edit-instead-of-supersede; the cell records decisions never created,
  sourced from a v1-era case study of an ordinary feature whose rationale was lost
  on archiving, in a project with its own entity numbering. A v1 project cannot
  supply an observed instance of a v2 pitfall. Return the observation to the case
  study that produced it, where s0003 governs it.
- **T1 (Medium)** — a real instance of its own pitfall, observed on a retired
  artifact type: its evidence is a plan archived as active, and plans are the v1
  entity that three entity types replaced. Re-cite from v2 or mark the vintage.

The remaining rows hold: of nineteen `Yes` rows, sixteen carry sound v2 evidence
and the three v1-era ones are the entries above.

## Constraints

- Any artifact change passes s0018 Verification: comprehension probes, then
  exams against same-file baselines, then per-lever attribution. Tail-end edits
  after the last measured run are forbidden.
- Retiring a rule from a spec, or adding one to a spec, is a behavioral change
  and needs explicit user approval. Only the s0019 cataloguing corrections and
  the s0018 floor statement are structural.
