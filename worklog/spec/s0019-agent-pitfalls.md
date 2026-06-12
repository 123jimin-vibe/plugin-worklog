+++
id = "s0019"
title = "Agent Pitfalls"
tags = ["quality", "methodology"]
+++

# Agent Pitfalls

Observed and anticipated failure modes when LLM agents work with the worklog methodology. Consolidates pitfalls previously scattered across entity specs (Dangers, Observed Agent Failure Modes) into one manageable reference.

Consumers: exam design (s0014), SKILL.md authoring (s0018), methodology refinement (s0001).

## Spec pitfalls

| # | Pitfall | Rule violated | Pressure mechanism | Observed |
|---|---|---|---|---|
| S1 | **Implementation details in specs.** Agent includes API signatures, class names, concrete technology choices, file paths in spec body. | s0011 Forbidden | User or conversation history describes implementation; agent leaks it into spec. | Yes — specific file paths instead of globs, script names that drift from actual filenames. |
| S2 | **Approval re-requested unnecessarily.** Agent asks for approval where none is needed: structural edits (typos, wording, reorganization), or behavioral items the user already stated. | s0011 Updating (structural = free; stated = approved) | Agent over-applies the approval rule — not distinguishing structural from behavioral, or not recognizing stated items as already approved. Known overcorrection risk of the S6 covering rule. | Yes — agent asked clarifying questions instead of acting on fully-stated greenfield instructions (happy-create exam regression after the S6 rule landed). |
| S3 | **Spec update contradicts related spec.** Agent updates one spec without checking parent/sibling specs for contradictions. | s0011 Dangers | Non-obvious: two specs share tags or overlapping paths. | Yes — version drift between specs, overlapping `paths` claims. |
| S4 | **Over-specification.** Agent creates a new spec for something that should extend an existing one. | s0011 Dangers | User asks for spec on a narrow sub-feature of an existing spec's domain. | Yes — narrow spec for a single function instead of extending the module spec. |
| S5 | **Code > spec precedence.** Agent treats code behavior as authoritative when it conflicts with the spec. | SKILL.md Precedence | Agent reads source code that diverges from spec; follows the code. | No. |
| S6 | **Speculative behavioral detail.** Agent adds behavioral requirements to a spec that nobody asked for or decided. Each added detail becomes a binding implementation constraint because spec is authoritative over code. Agent treats spec-writing like documentation (more detail = better) rather than legislation. Same pitfall through decisions: rationale or consequences invented for an immutable record. | s0011 Updating (behavioral = approval) | Agent "fleshes out" a spec based on what seems reasonable, or imports behaviors from similar systems seen in training data. | Yes — arbitrary constraints and edge-case handling added during spec creation, discovered only when implementation hits them; exam runs disclosed their inferences yet bound them anyway, and fabricated decision rationale. |
| S7 | **New spec without `UNIMPLEMENTED` markers.** Agent creates a spec for unbuilt features with behaviors stated as established facts. Nothing is implemented but the spec reads as current — no signal about what needs building, drift detection sees no gap. | s0011 Required Sections (mark approved unbuilt items `UNIMPLEMENTED`) | Spec-writing feels like describing what the system *will* do; agent writes in present tense without distinguishing "exists" from "should exist." | Yes — greenfield specs with all behaviors stated as current, no indication of implementation status. |
| S8 | **`UNIMPLEMENTED` misread as draft.** Agent interprets `UNIMPLEMENTED` markers as "spec is not finalized" rather than "behavior is approved but not yet built." Leads to hedging, re-asking for approval on already-approved items, or treating the spec as non-authoritative. | SKILL.md Precedence (spec authoritative regardless of markers) | Marker text triggers "work in progress" associations; agent treats marked specs as tentative. | Yes — agent asked to "finalize" specs that were already approved, hedged language around marked behaviors. |
| S9 | **Spec register drift.** Spec body written as documentation: status sections, history recounting, restated rules, selling prose. Bloat degrades agent consumption; status and history go stale in place (git and tasks already hold them). | s0011 Register | Spec-writing pattern-matches documentation — more prose reads as more helpful; session context leaks in as narration. | Yes — narrative status and history sections required condensing in a real spec (new.r-g.kr t0015). |

## Task pitfalls

| # | Pitfall | Rule violated | Pressure mechanism | Observed |
|---|---|---|---|---|
| T1 | **Status not maintained.** Agent starts working without setting status to active, or finishes without setting done. | s0012 lifecycle | Agent focuses on implementation, forgets lifecycle bookkeeping. | Yes — plan archived as "active," stale plans in active directory. |
| T2 | **Empty modifies when work touches spec-governed files.** Chore/refactor under spec's `paths` but agent sets modifies = [] because "no behavior change." | s0012 Forbidden | Renaming, cleanup, or refactoring that touches governed paths. | No. |
| T3 | **Stubs presented as complete.** Agent marks task done when implementation uses mock data, placeholder returns, or stub comments. | SKILL.md stubs rule | User scaffolded endpoints; agent completes the task based on shape, not substance. | Yes — SKILL.md presented stub scripts as functional. |
| T4 | **Archive without spec verification.** Agent moves task to archive without checking that the governing spec is still consistent. | s0012 Archiving | Agent just does move_file, doesn't read or verify the spec. | Yes — task archived with the governing spec untouched by the shipped work (vocaroll t0004). |
| T6 | **`UNIMPLEMENTED` markers left stale.** Agent completes work that resolves an `UNIMPLEMENTED` item but doesn't remove the marker. | s0012 observed failure | Agent focuses on code, doesn't circle back to update spec. | Yes — implemented items still marked as unimplemented in specs. |
| T7 | **State write-back omission.** New current state recorded only in the task body, a decision, or external docs; the spec keeps describing the old state. Distinct from T4: the archive-time check may even run — the agent judges "consistent" because it treats task and decision text as part of the record. | s0012 Archiving | Tasks and decisions feel like the durable record; "verify" reads as a judgment call satisfiable without writing anything. | Yes — design shipped to docs with spec untouched (vocaroll t0004); binding constraints lived only in a decision or nowhere (new.r-g.kr t0008, t0006). |

## Decision pitfalls

| # | Pitfall | Rule violated | Pressure mechanism | Observed |
|---|---|---|---|---|
| D1 | **Non-trivial edit instead of supersede.** Agent modifies an accepted decision's substance (choice, rationale, consequences) in-place. Trivial fixes (typos, formatting, obvious date corrections) are acceptable. | s0013 Forbidden | The change feels small but alters the historical record. | Yes (inverse) — design rationale buried in archives; decisions not created when they should be. |
| D2 | **Missing relates_to.** Agent creates a decision without linking it to the affected spec(s). | s0013 Forbidden | Decision is about process or tooling; agent doesn't think to link it. | No. |

## Cross-cutting pitfalls

| # | Pitfall | Rule violated | Pressure mechanism | Observed |
|---|---|---|---|---|
| X1 | **Tests after implementation.** Agent writes code first, then tests — or defers testing until "we see it working." | SKILL.md Rules | Conversational momentum ("simple feature, iterate fast"). | Yes — subagent read implementation before writing tests despite explicit black-box instruction. |
| X2 | **Implementation without covering spec.** Agent starts coding before a spec exists for the feature area. | SKILL.md Forbidden | User directly requests implementation; no spec mentioned. | No. |
| X3 | **Test agent reads source code.** Agent derives tests from implementation details rather than spec alone. | SKILL.md Forbidden | Test seems more thorough when grounded in actual code. | Yes — subagent read implementation, defeating spec-only test isolation. |
| X4 | **Lifecycle bypass.** Agent modifies spec inline during task implementation without going through the update approval flow. | v1 lesson | Agent is "in the flow"; updating the spec feels natural. | Yes — v1 lesson: "agents modify specs inline while working." |
| X5 | **Spec change disguised as refactoring.** Agent changes observable behavior under the guise of "cleanup." | SKILL.md Forbidden | The behavioral change is small and the refactor framing feels safe. | No. |
| X6 | **Plan mode as substitute for worklog.** Agent enters an external planning mode when task body or spec body would serve as the planning medium. Duplicates planning outside the worklog where it is not persistent or traceable. | SKILL.md Session resume (worklog is your memory) | Agent defaults to built-in planning workflow rather than using the methodology's own artifacts. | Yes — agents enter plan mode for work that a task file already covers. |
| X7 | **Comment narration.** Code comments restate spec/task content or recount the change being made, instead of referencing the governing ID. Duplicated truth drifts when the spec changes. | s0001 Key Rules | Mid-task, the task's context feels load-bearing; the agent narrates it into the code it touches. | Yes — comments restating task context required trimming (new.r-g.kr t0012). |
| X8 | **Context-bound naming.** Public name readable only with the defining module's context; ambiguous or misleading at import sites. | s0001 Key Rules | The module's domain is ambient while authoring; the agent never simulates reading the name from outside it. | Yes — bare "catalog" for i18n message sets, renamed later (new.r-g.kr t0012). |
| X9 | **Script path invention.** Agent invokes nonexistent `<repo>/scripts/*` or `<repo>/worklog/scripts/*` instead of the plugin's script directory. | SKILL.md Scripts | Repo-local tooling is the dominant prior; a repo path feels more plausible than a plugin install path. | Yes — recurring across consuming projects. |

## Severity

Severity = damage × persistence. Persistence depends on visibility: a pitfall the user can see immediately is caught and fixed; one that's invisible in the artifacts persists and compounds.

| Severity | Meaning |
|---|---|
| **Must** | Low visibility, propagating damage. Corrupts the spec→test→code chain or erases audit trail silently. |
| **High** | Medium visibility or cascading. Detectable on inspection but causes real harm if missed. |
| **Medium** | Fixable on discovery. No information destroyed, but adds maintenance burden or governance gaps. |
| **Low** | High visibility, minimal damage. User notices immediately; trivially correctable. |

| # | Severity | Rationale |
|---|---|---|
| S5 | Must | Spec "corrected" to match buggy code. Entire chain poisoned. Change looks reasonable — low visibility. |
| S6 | Must | Speculative requirements silently bind implementation. Extra detail in a spec looks thorough, not harmful — low visibility until implementation. |
| T3 | Must | Stubs presented as complete. Downstream work assumes feature is done. |
| T7 | Must | Spec keeps describing the old state while reading as current. Future agents act on it; staleness is invisible until something breaks. |
| X1 | Must | Tests written after implementation, coupled to code. Ordering invisible in artifacts. |
| X3 | Must | Tests derived from source code, not spec. Coupling invisible until refactor. |
| X4 | Must | Spec modified without approval during implementation. No paper trail. |
| X5 | Must | Behavioral change hidden under "cleanup" framing. No decision trail. |
| S3 | High | Spec update contradicts a related spec. Need to read both specs to notice. |
| S7 | High | Missing `UNIMPLEMENTED` markers means no implementation status signal. Drift detection blind to unbuilt features. Visible on careful reading. |
| S8 | High | `UNIMPLEMENTED`-as-draft undermines spec authority. Agent hedges or re-gates already-approved work. Medium visibility — user notices hedging. |
| T6 | High | Stale `UNIMPLEMENTED` markers. Completed work still marked unimplemented, spawning redundant tasks. |
| D1 | High | Non-trivial edit instead of supersede. Alters historical record silently. |
| X2 | High | Implementation without covering spec. Drift detection blind. |
| S1 | Medium | Impl details in spec body. Readable, but maintenance burden compounds. |
| S9 | Medium | Bloated, stale-prone prose degrades agent consumption; no information destroyed. Cut on discovery. |
| T1 | Medium | Status not maintained. Visible but causes stale state if uncaught. |
| T2 | Medium | Empty modifies on governed work. Governance gap, retroactively correctable. |
| T4 | Medium | Archive without verifying spec consistency. Catchable on next read. |
| D2 | Medium | Missing relates_to. Orphaned decision, harder to discover. |
| X7 | Medium | Duplicated truth in comments drifts silently but is visible in review and cheap to cut. |
| X8 | Medium | Ambiguity compounds at call sites; rename is mechanical but ripples. |
| S2 | Low | Unnecessary approval gate. Delay only. |
| S4 | Low | Fragmented governance. Specs mergeable, just tedious. |
| X6 | Low | Plan mode visible and harmless, just redundant. User notices immediately. |
| X9 | Low | Invocation fails immediately; nothing persists. |

## Constraints

- Do not create a new entry that is near-identical to an existing one. If two pitfalls differ only in which entity they manifest through (e.g., "hotfix archived without decision" vs. "skipped decision for hotfix"), they are the same pitfall — merge them or keep one.

## Anticipated Changes

- New pitfalls discovered from exam results or production incidents.
- Severity re-evaluation as methodology enforcement matures.
