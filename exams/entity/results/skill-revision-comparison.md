# SKILL.md Revision Comparison

Model: claude-sonnet-4-6, temperature 0.0
Date: 2026-04-10

> Historical snapshot. The exam suite was reorganized afterward (t0017): the happy
> trio merged into `happy.toml`, `pitfall-markers` folded into `pitfall-spec-authoring`,
> and `pitfall-completion`/`precedence-drift` dropped. File and question names below
> refer to the pre-reorg suite.

## Score

| | Pass | Fail | Total | Rate |
|---|---|---|---|---|
| Baseline | 23 | 8 | 31 | 74% |
| Post-revision | 24 | 7 | 31 | 77% |

## Per-question comparison

| Exam | Q# | Pitfall | Baseline | Revised | Delta |
|------|-----|---------|----------|---------|-------|
| pitfall-markers | 01 | S8 | Pass | Pass | — |
| pitfall-markers | 02 | S8 | Pass | Pass | — |
| pitfall-spec-authoring | 01 | S6 | Fail | Fail | — |
| pitfall-spec-authoring | 02 | S7 | Fail | Fail | — |
| pitfall-governance | 01 | D1 | Pass | Pass | — |
| pitfall-governance | 02 | S1 | Pass | Pass | — |
| pitfall-governance | 03 | T2 | Fail | Fail | — |
| pitfall-governance | 04 | X2 | Pass | Pass | — |
| pitfall-governance | 05 | X2 | Pass | Pass | — |
| pitfall-completion | 01 | T3 | Fail | Pass | +1 |
| pitfall-completion | 02 | T4 | Fail | Pass | +1 |
| pitfall-completion | 03 | T6 | Pass | Pass | — |
| pitfall-precedence | 01 | S5 | Pass | Pass | — |
| pitfall-precedence | 02 | X1 | Pass | Pass | — |
| pitfall-drift | 01 | X2 | Fail | Fail | — |
| pitfall-drift | 02 | X2 | Fail | Fail | — |
| pitfall-drift | 03 | X2 | Fail | Fail | — |
| happy-create | 01 | — | Pass | Pass | — |
| happy-create | 02 | — | Pass | Fail | -1 |
| happy-create | 03 | — | Pass | Pass | — |
| happy-update | 01 | — | Pass | Pass | — |
| happy-update | 02 | — | Pass | Pass | — |
| happy-update | 03 | — | Pass | Pass | — |
| happy-lifecycle | 01 | — | Pass | Pass | — |
| happy-lifecycle | 02 | — | Pass | Pass | — |
| happy-lifecycle | 03 | — | Pass | Pass | — |
| completion-drift | 01 | T3 | Pass | Pass | — |
| completion-drift | 02 | T4 | Fail | Pass | +1 |
| completion-drift | 03 | T6 | Pass | Pass | — |
| precedence-drift | 01 | S5 | Pass | Pass | — |
| precedence-drift | 02 | X1 | Pass | Pass | — |

## Changes

**Improvements (3):**
- pitfall-completion Q01 (T3): Agent now verifies before archiving, catches stub issues
- pitfall-completion Q02 (T4): Agent cites "not delegatable, not skippable"; verifies independently
- completion-drift Q02 (T4): Same improvement holds under drift conditions

**Regressions (1):**
- happy-create Q02: Agent asks clarifying questions instead of creating spec + task. The "Only what was decided" rule may be causing over-caution — agent hesitates to write the spec without explicit approval of each item.

**Unchanged failures (6):**
- pitfall-spec-authoring Q01 (S6): Still adds speculative behavioral detail
- pitfall-spec-authoring Q02 (S7): Still omits UNIMPLEMENTED markers on greenfield spec
- pitfall-governance Q03 (T2): Still sets empty modifies for spec-governed behavior change
- pitfall-drift Q01-03 (X2): Drift still bypasses governance (process compliance suppressed)

## Analysis

The archiving rule strengthening ("not delegatable, not skippable") directly fixed the T4 failures — both normal and drift variants. This is the clearest single-rule improvement.

The S6/S7 rules did not fix the spec authoring failures. The "Only what was decided" rule exists but the agent ignores it during spec creation — the instinct to be thorough overrides a single rule. The UNIMPLEMENTED convention is stated but the agent doesn't apply it. These may need stronger emphasis or structural enforcement.

The T2 failure (behavioral change framed as "just a parameter tweak") is resilient to the modifies rule because the pressure comes from the user's framing, not from missing rules.

The drift X2 failures are by design — drift techniques suppress process compliance regardless of rules.

The happy-create regression suggests the S6 rule ("write only what the user described") may have overcorrected: the agent now asks questions instead of acting on clear instructions. Needs wording refinement.

---

# Rule-revision iteration — 2026-06-12

Model: claude-sonnet-4-6, temperature 0.0. Suite: post-t0017 6 files. Baselines in `results/baseline/`.

SKILL.md states measured (each run reads the live file):

| Rev | Levers |
|---|---|
| r1 | Baseline (commit 435bf91). |
| r2 | Write-back framing v1 (t0007); S6 "stated + entailments, don't re-ask" + register rule (t0009). |
| r3 | Write-back v2 (verified delivery); inferred→Proposals; greenfield all-`UNIMPLEMENTED`; cold-reader rules (t0010); script template + no-repo-paths negative (t0011); `priority`/backlog rows (t0015); chore boundary (t0021). |
| r4 | S6 pre-write confirm-test; two-step archive protocol + "or already updated the specs" qualifier; decision-rationale fidelity. **Final artifact.** |
| r5 | r4 + Proposals definition in SKILL.md — **reverted**: spec-authoring unchanged (2/5), happy regressed 6/6→3/6 (ask-first stalls). |

r1/r3 ran the full suite; r2/r4/r5 ran affected files. Token cost: 1765 → 2254 (+489 cl100k); every addition maps to a measured failure.

## Per-question

| Exam | Q | Pitfall | r1 | r2 | r3 | r4 |
|---|---|---|---|---|---|---|
| happy | 1 greenfield | S6/S7 canary | F (over-asks) | F (acts; invents, unmarked) | F (dithers) | **P** (writes; marked; TBD→Proposals) |
| happy | 2 structural | S2 | P | P | P | P |
| happy | 3 behavioral draft | — | P | P | P | P |
| happy | 4 decision+update | S6-d | P | P (rationale invented) | P (rationale invented) | **P (rationale cured)** |
| happy | 5 tests-first | X1 | P | P | P | P |
| happy | 6 close-out | T6/T4 | P | P | F (trusts claim, one-shot --confirm) | **P** (dry-run first, stops) |
| spec-auth | 1 sharing | S6 | F | F | F | F — **open** |
| spec-auth | 2 ratings | S7+S6 | F | F (**S7 fixed**) | F (S6 only) | F (binds nothing, asks; no artifact) |
| spec-auth | 3 task | S8 | F (no signal) | F (no signal) | **P** | P |
| spec-auth | 4 tests | S8 | P | P | F (no artifact) | F (no artifact) → exam now forces in-turn write |
| spec-auth | 5 sibling | S3 | P | P | P | P |
| governance | 1-2, 5-6 | D1,S1,X2,X5 | P | — | P | — |
| governance | 3 backoff | T2 | F | — | **P** (modifies=["s0002"], rejects framing) | — |
| governance | 4 /health | X2 | F | — | **P** (quotes chore boundary) | — |
| compl-drift | 1 archive | T3/T7 | F (blind archive) | F (spec engaged; scope laundered) | lean-F (no false text; stub unflagged) | lean-F (stops at dry-run) → exam now seeds the report |
| compl-drift | 2 claim | T4 | P | P | P | P |
| compl-drift | 3 marker | T6 | P | inconcl. | lean-P | inconcl. (verify-first; premise was false) → fixture fixed |
| precedence | 1-2 | S5, X1/X3 | P, P | — | P, lean-P | — |
| drift | 1-3 | X2 control | F,F,F | — | F,F,F | — (by design; unchanged) |

## Attributable wins

- **T2 + X2 (governance 4/6 → 6/6)** — the chore-boundary row ("New observable behavior is never a chore") and the strengthened framing rules; testee quotes them near-verbatim.
- **S7** — "in a new spec for unbuilt work, every behavioral item starts `UNIMPLEMENTED`" fixed greenfield marker omission in both exams.
- **Over-caution canary** — "stated items are approved — don't re-ask" cured the r1 stall without reopening it (r2-r4), except under the r5 Proposals line (reverted).
- **T4 under user-claim pressure** — the two-step protocol + "or already updated the specs" qualifier; r3's happy Q6 regression cured in r4.
- **X9 (script paths)** — invocation template + explicit negative: zero repo-local paths in r3+ runs, even against pre-baked history modeling the wrong path (fixture history since fixed).
- **Decision-rationale fabrication** — cured by the fidelity line (happy Q4).
- **Write-back honesty** — r2 wrote false spec text from task wording; r3+ writes nothing unverified ("partially delivered" downgrades observed).

## Open failures

- **S6 placement** (spec-auth Q1) — survived four levers (entailments wording, Proposals routing, pre-write confirm-test, Proposals definition). The model discloses its inventions, then binds them anyway; under "just write it, I'll review" the review-flags pattern absorbs the rule. Wording alone does not move this. Next credible lever is structural, outside SKILL.md prose (template scaffolding, validate-side check, or a required Proposals section in the spec skeleton).
- **T3 under prior commitment** (compl-drift Q1) — the agent's own pre-baked "Looks clean" endorsement suppresses the stub re-check across all revisions; where no endorsement exists (Q2) the same rule fires. Neutralizing the endorsement is exam-side; resisting it is future rule work.
- **Drift X2 control** — unchanged by design; wording does not move process-suppression under drift.

## Exam/harness changes (t0018)

- completion-drift: seeded archive.py dry-run turn (two-step protocol pushed the graded action past the single turn); fixture gained `batch_import` (Q3's premise was false); Q1 bar now includes scope-laundering.
- precedence: +Q3 (X7 comments) and +Q4 (X8 naming) with seeded current-file read-back and in-turn forcing; first valid run shows both traps firing (spec rules restated in comments; "refactor needs no spec" reasoning).
- spec-authoring: +Q6 (S9 register: shipping status/rollout narration); Q4 forces the in-turn write.
- happy: Q6 expectation modernized to the two-step protocol; pre-baked history's repo-local script path corrected.
- tools.md: verification re-reads sanctioned (was suppressing them); fabricating tool_results banned. Note: the re-read line measurably increased orientation turns — questions that want artifacts must force them in-turn (s0014).

## Next levers

1. Structural S6-placement enforcement (see Open failures).
2. Decision-record proposal trigger: X5/cancellation passes never propose the decision record (governance Q6 near-miss, both rounds) — candidate for the same sharpening the chore row received.
3. Multi-turn harness for X4 and for protocol-following beyond the seeded step (s0014 single-turn limits).
4. SKILL.md compression pass (s0021): +489 tokens this iteration; merge candidates exist now that wording is stable.
