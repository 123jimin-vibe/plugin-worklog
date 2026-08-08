+++
id = "t0031"
title = "Audit brainstorm coverage before removing the corpus"
status = "active"
tags = ["research", "methodology"]
modifies = ["s0003"]
priority = 0
+++

# Audit brainstorm coverage before removing the corpus

Investigation preceding removal of `brainstorm/`. Output is knowledge: which
issues raised in the corpus no specification addresses. Nothing is deleted under
this task.

An issue is any problem, requirement, constraint, design question, or failure
mode the corpus raises. Per issue the question is whether a spec's contents
address it — not whether a spec mentions the same topic.

## Scope

- Inventory the corpus and classify every issue: covered, partially covered
  (a spec addresses it but drops a condition), uncovered, or obsolete.
- Identify what would dangle on removal: specs, tasks, or artifacts that point
  into `brainstorm/` and would break.
- Findings in this body. Promotion of uncovered issues into specs is behavioral
  and out of scope.

## Known dangling references

Established before the audit ran:

- s0021 mandates recording compression attempts in the ledger under
  `brainstorm/prompt-engineering/`. Removing the corpus deletes the register a
  spec requires be written to.
- t0029 plans to return D1's misfiled observation to `brainstorm/case-study-bfc.md`,
  where s0003 governs it. Removal invalidates that plan.
- s0003 governs `brainstorm/**` and describes nothing else. Removing the corpus
  retires the spec, which s0011 gates behind a decision record.

## Findings

Roughly 90 issues are uncovered across 17 files. They are not scattered: five
structural classes account for nearly all of them, and each class is uncovered
for a stated reason rather than by oversight.

### Class 1 — Rejected and deferred alternatives

No spec section is the home for "X was evaluated and rejected because Y".
s0013 defines rationale as "why this option over alternatives", so decision
records are that home, but only two exist and neither concerns any of these.

- Drift by commit SHA in spec frontmatter. Rejected as self-referential:
  writing the SHA creates a new commit, so the value is always stale. The only
  record of why drift detection stores nothing. s0010's watermark-reset danger
  reads as an unfixed flaw without it.
- Two evaluated file-mapping alternatives (derived from task/commit history; AI
  inference at check time) with their costs, the accuracy verdict on globs
  ("poor for cross-cutting"), and the hybrid recommendation that was never built.
- Five designed drift mechanisms, none shipped: post-commit changeset flag, CI
  gate, `git notes` retro-annotation, pickaxe behavior-level detection, blame
  churn scoring. The last two are the designed mitigations for s0010's own two
  recorded dangers.
- Ten spec-representation approaches evaluated against a real codebase. The
  chosen one survives in s0011; every rejection and the decisive criterion
  ("cross-cutting specs must stay intact", which eliminated four) do not.
- Task sub-progress checklists: tried in v1, dropped on measured grounds.
- The Plan entity in full — IDs, four statuses, `targets`/`implements`, its
  lifecycle, and the "do not maintain a task list" constraint. v2 has three
  entity types and no record of removing the fourth.
- Directory-format entities with scratchpad and checklist files, and the
  promotion migration into them.
- `created`/`updated` date fields, dropped in favour of git.

### Class 2 — Purpose, goals, and cross-cutting constraints

s0011's Register makes spec prose legislation and cuts any sentence adding no
behavior, constraint, or danger. A purpose statement binds no implementation, so
the register that keeps specs sharp is what excludes these.

- The meta-goal: make agents reliable for large projects under minimal human
  supervision. Both scale conditions justify the methodology's process cost and
  appear in no spec.
- The counterfactual that the whole methodology compensates for a model
  limitation rather than being intrinsically good — with it goes the sunset
  condition.
- Domain and language agnosticism; nothing forbids a future spec adding
  language-specific rules.
- Portability: the current delivery is the first implementation, not the
  definition. s0001 states the platform with no such qualifier.
- The empirical stance: tests-first is the assumed baseline, any other practice
  needs empirical justification before adoption.
- git as a hard prerequisite, and the no-duplication rule covering authorship
  and diffs, not only history.
- Multi-agent concurrency via worktrees and branches — the only answer to how
  two agents share one worklog.
- Conventions must be inferable from structure, frontmatter, and naming.
- In-repo context files carry only triggers pointing at the skill, never
  methodology content.
- The five-stage development model the methodology is a specialization of, and
  the fact that two stages were elided rather than never considered.
- Ten domain-general architecture principles, including the only stated metric
  for spec boundary-drawing (minimize components touched per requirement change)
  and declared inter-component dependency rules.

### Class 3 — The empirical basis for claims the specs assert

s0018 and s0021 state five principles as measured results. The measurements are
inside the deletion set. The specs stay authoritative and become unfalsifiable.

- The context-file study behind "verbose context degrades agent performance":
  its figures, its mechanism, and the citation. Two spec-side principles rest on
  it and neither carries it.
- Every verbatim before/after text pair in the compression ledger, for all 24
  entries. No second home anywhere. Entries 1-7 exist nowhere else at all.
- The rejected variants of cut clauses, which is what makes a cut re-measurable.
- The attribution law learned the hard way: before crediting a clause, test by
  removal and by restoration; correlation across revisions that all contain it
  proves nothing. s0018 Verification specifies the removal direction only, so the
  error that stood wrong for five revisions can recur.
- The negative result that a clause asserting its own authority confers none.
- The highest-yield structural rewrite measured (diagram to inline notation,
  −46% on one section), absent from s0021's lever list.
- The enforcement gradient prose -> types -> tests -> lint -> CI, which tells a
  future agent which rung to climb next.
- The discoverability test for what belongs in a spec at all: only
  non-discoverable knowledge that cannot be encoded as tooling.
- The entire design surface behind s0001's five-word "enforcement mechanism"
  anticipated change, including completion-gating on subagent stop — the
  mechanical analogue of the write-back that s0012 calls not skippable.
- Trigger-phrased rules as an untested competitor to the whole compression
  approach.

### Class 4 — Failure modes that surface in code or in strategy

s0019 is organized by worklog entity; the corpus catalogue is organized by agent
faculty. Every corpus item whose failure lands in an artifact has a row. Every
item landing in code or in the agent's own strategy has none — 18 of 29.

Addressable, and absent from every spec:

- Tech-debt blindness: no model of change frequency, cannot recognize debt it is
  creating. Only hotfix-scoped debt is specced.
- Change locality: code satisfies the task without organizing for future edits.
- No refactoring initiative, and the ROI triage distinguishing messy-but-cold
  from messy-and-hot code. s0006 presumes the refactor already decided.
- Implicit generality unread: specs imply generality across a dimension and the
  agent builds the degenerate case. This is the read-side mirror of the
  speculative-detail pitfall, and the catalogue has nine rows on over-writing a
  spec and none on under-reading one.
- Good-path test bias: agents treat tests as something to pass, not a tool to
  find failures. Nothing governs tests an agent writes for a consuming project —
  s0017 governs this repo's own suite, s0014 governs exam questions.
- No test decomposition; oversized undifferentiated test files.
- Interface design as simultaneously a behavioral contract and an implementation
  decision. This is the actual pressure behind the most-observed spec pitfall,
  which the catalogue attributes to a shallower cause.

Inherent model and harness limits, recorded as context only: no cross-session
learning, subagent context loss, no inter-agent channel, no orchestration
self-awareness. Notably the methodology's own answer to the first — a durable
failure register propagated into the prompt — is the reason s0019 exists, and no
spec says so.

### Class 5 — Rules that live only in the artifact

Not corpus content, but surfaced by the audit and load-bearing for it. Five
rules ship in SKILL.md with no source spec, inverting the flow s0018 prescribes:
the deliver clause, the abort-and-escalate qualifiers, the small-project
decision allowance, the single-session task-sizing yardstick, and the
spec-count ceremony threshold. The corpus is the only place three of them are
argued for.

## Partial coverage worth naming

- The antipatterns rule. The spec keeps the five-item list and drops the
  non-override clause ("satisfying the immediate task does not override
  defensive concerns"), the three-way security/performance/reliability taxonomy
  that makes the list exemplary rather than closed, and two members outright
  (XSS, no backoff on retries). It then never reaches the artifact at all.
- Cold reader. The spec instructs it; the corpus records that agents cannot do
  it even when explicitly instructed. The finding is the instruction's own
  refutation, and only the instruction survives.
- Precedence ranks spec over code over tests. The corpus ranks documentation
  too; a spec-versus-README conflict is unresolvable from s0001 alone.
- Ceremony scaling keeps "small projects need less process" and drops the
  invariant that separates artifacts from rules — that the rules still apply.
- ASCII connectives forbid the unicode glyphs the artifact actually ships; the
  measured exemption for two cheap ones is ledger-only.

## Additional dangling references

Beyond the three known before the audit:

- Two in-spec "v1 lesson" citations — one on a Must-severity pitfall whose
  evidence is quoted verbatim from the corpus — refer to a deleted file. Neither
  is a path, so no link check or grep sweep surfaces the break.
- s0003 describes the corpus in five places (contents categories, the ledger's
  append-only rule, two Proposals, one Danger). Deleting the corpus makes
  authoritative sentences false, not merely stale.
- The exam comparison ledger cites the compression ledger three times. That
  record is append-only by s0014, so those citations cannot be repaired without
  violating the spec that governs it.
- t0029 has a second planned write-back into the corpus: re-citing T1's evidence
  or marking its vintage requires the case study to stay citable.
- s0003's own Proposal that the index list every corpus file is live: one
  resource file is unlisted, and two of seven are internal imports rather than
  the external references the index claims.

## Corrections to the record

- s0019 has 26 rows, not 24. T5 is a numbering gap with no row and no severity
  entry.
- The antipatterns rule is s0001 Key Rules line 49, not 45.
- The naive claim that the compression ledger's findings vanish entirely is
  false. Round-level narrative for entries 8-24 survives in the exam comparison
  ledger, outside the corpus. Entries 1-7 and every verbatim text pair do not.
