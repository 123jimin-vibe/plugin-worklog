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
4. SKILL.md compression pass (s0021): +489 tokens this iteration; merge candidates exist now that wording is stable. **Done — see below.**

---

# Compression pass (t0022) — 2026-06-12

Model: claude-sonnet-4-6, temperature 0.0 (exams); claude-haiku-4-5 (comprehension canary).

Tokens: 2254 → 2097 cl100k (−7.0%); 2519 → 2344 claude-opus-4-6 (−175/session, confirmed in exam input_tokens). Per-section cl100k: Task 825→748, Relationships 107→58, Decision 147→133, Entities 58→51, Spec 465→457 (binding paragraph minimal-touch — S6 battleground), Scripts 372→370, preamble/Workflows unchanged.

Levers (pairs + verdicts in `brainstorm/prompt-engineering/compress.jsonl`): task+decision TOML examples → field lists (spec example kept as sole syntax anchor); Stubs ¶ merged into Archiving; "Approval = explicit confirmation" bullet deduped (rule stays in Spec ¶ + Forbidden); "Implementation details in specs." deduped from Forbidden (stays in Spec ¶); Relationships diagram → inline `·` line; status lifecycle merged into the field list; minor merges (decision edit rules, next_id gloss). Every measured load-bearing phrase kept verbatim.

## Verification

- Comprehension probes (10 questions × {r4, compressed}, haiku): 10/10 parity; compressed read better twice (frontmatter probe included `tags`; Proposals routing cleaner, no invented constraints in the illustration).
- Exams: happy 5/6, governance 4/6, spec-auth 3/6, completion-drift and precedence unchanged. **Every delta reproduces under a same-exam r4-skill control run** — governance r4-control Q3 writes t0004 with no `modifies`, rationalizing "the parameter isn't a behavioral item"; r4-control Q2 ask-stalls with no artifact; happy r4-control Q1 stalls identically. The dips are r4-era behavior + exam observability surfaced by re-running files last measured at r3, not compression. Zero malformed frontmatter in any run despite the removed examples.

## Watch items (pre-existing, surfaced by this round)

- T2 (governance Q3): the r3 pass did not survive into r4 — fails under both r4-control and compressed runs. Confirms the doc's earlier read: framing pressure, flaky boundary.
- S6 (spec-auth Q1): fresh run binds the same invented spec with zero disclosure prose (r4 at least disclosed). Single sample; strengthens the structural-lever recommendation.
- Spec-auth Q6: both runs strip all six markers purely on the user's shipped-claim, no verification surfaced — latent T6-adjacent gap distinct from the register property (which both hold).
- Orientation stalls on artifact questions without in-turn forcing now affect happy Q1, governance Q2, spec-auth Q3, precedence Q4 (post-t0018 tools.md re-read line). Exam-side forcing pass queued as t0023.

Verdict: compression is behavior-neutral on every attributable comparison; −175 claude tokens/session banked. Next size lever would be removing rules, which is a scope decision, not a wording one.

---

# Compression round 2 (t0024) — 2026-06-12

User-directed deeper pass. Tokens: 2097 → 2000 cl100k; 2344 → 2239 claude-opus-4-6. Cumulative across both rounds: 2254 → 2000 cl100k (−11.3%), 2519 → 2239 claude (−280/session, visible in exam input_tokens: governance ~−145, precedence ~−105, drift-condition exams ~−100 vs r4).

Levers (pairs in compress.jsonl): (1) file-wide bold/italic strip — paragraph leads → plain or colon-labels, Rules bullet titles → lead phrases, workflow names plain (~60 cl100k); (2) binding paragraph rebuilt — confirm-test merged into the write-rule as the definition of unstated, "invent nothing" subsumed by "only", don't-re-ask sentence shortened ("genuinely" kept); (3) `UNIMPLEMENTED` semantics split to own paragraph, "does not license it" → concrete "marking an item does not approve it"; (4) archiving lost-state sentence merged. Verbatim-kept: two-step protocol + "Never `--confirm` first." + claims qualifier, "Never present stubs as complete.", "Discussion is not approval.", chore row, script location/template/negative, greenfield marker rule.

## Verification

- Comprehension probes (haiku, 10 Q): 10/10; the S6 probe produced the cleanest Proposals routing of the three revisions.
- Exams vs c1 (snapshot `results/c1/`): happy 5/6 =, governance 4/6 =, spec-auth 3/6 =, completion-drift =, precedence = . All required passes held; **no new ask-stalls on stated content** (the named r5 risk — happy Q4's re-ask canary clean; the residual ask-stalls target only genuinely-undecided points, per graders).
- Shape improvements, not graded as wins: spec-auth Q1 back to disclosed binding (c1 bound silently; c2 appends "things I inferred that you should confirm or correct" — the merged confirm-test fires post-write; binding-section discipline still open); happy Q4's malformed double-brace tool JSON gone and invented rationale hedged; happy Q3 delivers the draft in-turn; completion-drift Q1 proposes instead of writing immediately; precedence Q3 comments flag divergence instead of asserting spec rules as code truth.

## New finding

- Spec-auth Q6: third consecutive run (r4, c1, c2) strips all six markers on the user's verbal "shipped" claim — no verification, none surfaced. Confirmed gap, not noise: "remove the marker when implemented" reads as *claimed*. Filed t0025 (rule: marker removal outside the archive write-back requires verified implementation).

Verdict: behavior-neutral-or-better; emphasis markers carried no measured behavioral weight; the binding-paragraph rewrite changed disclosure, not binding — consistent with the standing conclusion that S6 placement needs a structural lever.

---

# Compression round 3 + marker rule (t0026, t0025) — 2026-06-12

Two levers this round, sequenced for attribution: (1) t0025 marker-verification rule added and single-lever verified on spec-auth Q6 before any compression ("I need to verify the implementation directly — a user claim alone isn't sufficient"); (2) t0026 telegraphic rewrite — prompt as natural-language program: articles/copulas dropped, ASCII connectives (`=>` implication, `!=` non-equivalence, `Stated = approved`), archive protocol as an explicit numbered 3-step pipeline.

Tokens: 2000 → 1935 cl100k; 2239 → 2180 claude-opus-4-6 (net, including the rule's +~16). Cumulative campaign: 2254 → 1935 cl100k (−14.2%); 2519 → 2180 claude (−339/session, −13.5%).

**Tokenizer-divergence trap (recorded in compress.jsonl and s0021 Dangers):** the first telegraphic draft used `⇒ ≠ ≥` — cl100k prices them like ASCII (parity), the Claude tokenizer prices them 3-5× (`⇒` ≈ 4-5 tokens vs `=>` ≈ 1). Draft measured −79 cl100k but only −23 claude; the ASCII swap recovered 52 claude tokens. `→` and `·` are cheap in both. Measure the deployment tokenizer, not a proxy.

## Verification

- Probes (haiku, 11 Q incl. new marker-claim probe): 11/11. Telegraphic register parses clean on the weak model; archive answer came back *more* procedural (mirrors the pipeline numbering); marker probe declines removal when code is uninspectable.
- Exams vs c2 (`results/c2/`): governance =, happy = (Q6 pipeline textbook: report first, claim != verification), **spec-auth 3/6 → 4/6** (Q6 cured: verifies src/collections instead of stripping markers; Q2's ask-stall gone per "Stated = approved" though still no artifact — forcing gap), **completion-drift Q3 → conduct-PASS** (handles the dangling seeded thread, then "verify batch import is actually implemented before removing the marker" → reads store.py; removal unobservable past the turn boundary — seed the re-read if full observability wanted), **precedence Q2 lean-P → P** (quotes the isolation bullet, self-identifies as contaminated) and Q4 now produces artifacts (forced-write compliance fixed; X8 property itself still fails: bare-generic module name, invented dead-code helper).
- Zero `=>`/`!=`/`=` misparses across all five exams and 11 probes.

## Watch items

- **X7 comment-honesty trade (precedence Q3, within expected-FAIL):** c3 cites spec IDs more and narrates less, but twice asserts a spec rule as code truth above divergent code without flagging the divergence (c2 flagged it). Plausibly the telegraphic "cite the ID, don't restate" executed as "compress the restatement". Next X7 wording pass must address divergence-flagging explicitly. Deliberately NOT patched this round — unmeasured tail-end edits are how regressions sneak in.
- Pipeline step-2 escape hatch "(or confirm wording already covers it)" taken exactly once across runs — under attention redirection (compl-drift Q3) — while identical drift got folded elsewhere. Exploitable; candidate for tightening when next touched.
- One `next_id.py s` arg slip (prefix/type conflation, isolated single occurrence).
- T3 under prior commitment (compl-drift Q1) and S6 binding discipline (spec-auth Q1) remain the standing open failures; the litmus self-incriminates post-write but does not route. Structural lever still the recommendation.

Verdict: strict improvement — two cures (S9-marker, T6-conduct), one strengthened pass, zero regressions on attributable comparisons; −339 claude tokens/session cumulative. Remaining mass: tables 523, TOML example + fences ~75, frontmatter 109, telegraphic rules ~750 — further reduction means removing rules or interface docs (scope decision).

---

# Trim experiment (t0027) — 2026-06-12

User-directed: clauses judged non-preventing (counterfactually present during failures, duplicated, or mechanism-unmapped) cut as c4 and evaluated. Sequence: c4 (eight cuts) → c5 (bisect: litmus restored) → c6 (final: litmus re-cut + deliver clause).

Tokens: 1935 → 1766 (c4) → 1782 cl100k (c6 final); claude 2180 → 1995 → 2014. **Campaign cumulative: 2254 → 1782 cl100k (−20.9%); 2519 → 2014 claude (−505/session, −20.0%).**

## Cut verdicts

| Cut | Watcher | Verdict |
|---|---|---|
| Scripts preamble (path prose + "This section is authoritative") | happy Q6 direct X9 stress + all-run sweeps | **Clean** — template-only path statement suffices; zero invented paths anywhere |
| No-antipatterns bullet | (exam-blind, mechanism-unmapped) | **Clean** — no effect anywhere |
| Forbidden regression-test line (dup of Bug fix row) | (exam-blind) | **Clean** |
| Session-resume + Plan-in-worklog → merged bullet | (exam-blind, X6 Low) | **Clean** |
| Decision "Create when:" list | governance Q1, happy Q4 | **Clean** — supersede mechanism alone drives correct decision handling |
| X7 comments bullet | precedence Q3 | **Keep cut** — WITH the rule: trap fired every run + false spec-as-truth comments with cargo-cult ID cites; WITHOUT: c4 zero false/zero narration (one false comment returned at c6 under the deliver clause — still better than any rule-present run) |
| X8 names bullet | precedence Q4 | **Keep cut on c3-era evidence** — counterfactual still unmeasurable (no artifact in any condition; Q4 defied forcing via questions→chore-deflection→survey across c4/c5/c6 — t0023 evidence) |
| Binding-paragraph litmus | spec-auth Q1, happy | **Keep cut — attribution corrected**: happy Q3 regressed at c4, but restoring the litmus (c5) did NOT cure it, and its credited disclosure effect survived removal (Q1 disclosed in c4/c6). The five-revision attribution was wrong. |

## The Q3 mechanism and the deliver clause

The c4 regression (happy Q3: "Draft the spec update" → 3 questions, no draft) was ask-salience redistribution: thinning the rules list amplified "Scope unclear => ask". Fix (c6): the ask bullet gains "A requested deliverable is delivered with open points flagged — not withheld pending answers." Results: happy Q3 cured (draft delivered, write correctly withheld); **spec-auth Q2 flips to its first-ever PASS** (ratings spec written, all five behavioral items `UNIMPLEMENTED`, opens flagged in prose); approval gates verified intact (governance Q5/Q6 — Q6 stronger); the binding rule dominates where delivery would encode a contradiction (spec-auth Q5 still flags, doesn't write); completion-drift Q2's in-turn write-back restored, Q3 marker verification sharper (greps the function).

Known costs of the clause (recorded, accepted): happy Q4 self-initiated an unrequested third write retiring s0001's Dangers note (out-of-scope edit, non-behavioral); precedence Q3's one false comment (above); precedence Q4 now tool-stalls (survey) instead of question-stalls — the clause needs "in this response"-grade teeth only the exam-side forcing (t0023) can measure.

## Suite state at c6 vs campaign start (r4)

happy 5/6 (Q1 environmental), governance 4/6 (Q2/Q3 r4-era, control-proven), **spec-auth 4/6 (Q2 and Q6 both new passes vs r4's 2/5)**, completion-drift Q2 + Q3-conduct, precedence Q1/Q2. The file is 20% smaller than r4 and the suite is strictly stronger.

Standing items: T3-under-prior-commitment and S6 binding (open as ever, structural lever); X7 future work = divergence-flagging wording; t0023 (on hold) now owns three documented Q4 defiance routes + happy Q1/governance Q2/spec-auth Q3 stalls; deliver-clause act-bias watch (Q4-happy shape).
