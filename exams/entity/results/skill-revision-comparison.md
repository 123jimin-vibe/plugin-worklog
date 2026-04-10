# SKILL.md Revision Comparison

Model: claude-sonnet-4-6, temperature 0.0
Date: 2026-04-10

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
