+++
id = "s0019"
title = "Agent Pitfalls"
tags = ["quality", "methodology"]
+++

# Agent Pitfalls

Observed and anticipated failure modes when LLM agents work with the worklog methodology. Consolidates pitfalls previously scattered across entity specs (Dangers, Observed Agent Failure Modes) into one manageable reference.

Consumers: exam design (s0014), SKILL.md authoring (s0018), methodology refinement (s0001).

## Spec pitfalls

| # | Pitfall | Rule violated | Pressure mechanism |
|---|---|---|---|
| S1 | **Implementation details in specs.** Agent includes API signatures, class names, concrete technology choices, file paths in spec body. | s0011 Forbidden | User or conversation history describes implementation; agent leaks it into spec. |
| S2 | **Discussion treated as approval.** Agent updates spec behavioral content based on casual chat, brainstorming, or "I was thinking..." statements. | s0011 Forbidden ("discussion ≠ approval") | Prior conversation turns contain design discussion that sounds like agreement. |
| S3 | **Structural update gated unnecessarily.** Agent asks for approval to fix a typo, reword a section, or add a constraint — even though behavior doesn't change. | s0011 Updating (structural = free) | Agent over-applies the approval rule, not distinguishing structural from behavioral. |
| S4 | **Spec update contradicts related spec.** Agent updates one spec without checking parent/sibling specs for contradictions. | s0011 Dangers | Non-obvious: two specs share tags or overlapping paths. |
| S5 | **Over-specification.** Agent creates a new spec for something that should extend an existing one. | s0011 Dangers | User asks for spec on a narrow sub-feature of an existing spec's domain. |
| S6 | **Code > spec precedence.** Agent treats code behavior as authoritative when it conflicts with the spec. | SKILL.md Precedence | Agent reads source code that diverges from spec; follows the code. |

## Task pitfalls

| # | Pitfall | Rule violated | Pressure mechanism |
|---|---|---|---|
| T1 | **Status not maintained.** Agent starts working without setting status to active, or finishes without setting done. | s0012 lifecycle | Agent focuses on implementation, forgets lifecycle bookkeeping. |
| T2 | **Empty modifies when work touches spec-governed files.** Chore/refactor under spec's `paths` but agent sets modifies = [] because "no behavior change." | s0012 Forbidden | Renaming, cleanup, or refactoring that touches governed paths. |
| T3 | **Stubs presented as complete.** Agent marks task done when implementation uses mock data, placeholder returns, or TODO comments. | SKILL.md stubs rule | User scaffolded endpoints; agent completes the task based on shape, not substance. |
| T4 | **Archive without spec verification.** Agent moves task to archive without checking that the governing spec is still consistent. | s0012 Archiving | Agent just does move_file, doesn't read or verify the spec. |
| T6 | **TODO markers left stale.** Agent completes work that resolves a spec TODO but doesn't remove the marker. | s0012 observed failure | Agent focuses on code, doesn't circle back to update spec. |
| T7 | **Cancel without decision record.** Agent cancels a task (or agrees to cancel) without creating a decision explaining why. | s0012 Forbidden | User says "let's drop this" casually. |

## Decision pitfalls

| # | Pitfall | Rule violated | Pressure mechanism |
|---|---|---|---|
| D1 | **Non-trivial edit instead of supersede.** Agent modifies an accepted decision's substance (choice, rationale, consequences) in-place. Trivial fixes (typos, formatting, obvious date corrections) are acceptable. | s0013 Forbidden | The change feels small but alters the historical record. |
| D2 | **Missing relates_to.** Agent creates a decision without linking it to the affected spec(s). | s0013 Forbidden | Decision is about process or tooling; agent doesn't think to link it. |
| D3 | **Hotfix without post-mortem.** Agent deploys/archives a hotfix without recording a post-mortem decision. Manifests in both decision creation (skipped) and task lifecycle (archived without linked decision). | s0012 Forbidden, s0013 Required Creation | Urgency overrides process; "we'll document it later." |
| D4 | **Casual statement treated as decision.** Agent records a formal decision based on an offhand remark in chat history. | s0011 Forbidden, s0014 adversarial design | Conversational momentum; the remark sounds decisive. |

## Cross-cutting pitfalls

| # | Pitfall | Rule violated | Pressure mechanism |
|---|---|---|---|
| X1 | **Tests after implementation.** Agent writes code first, then tests — or defers testing until "we see it working." | SKILL.md Rules | Conversational momentum ("simple feature, iterate fast"). |
| X2 | **Implementation without covering spec.** Agent starts coding before a spec exists for the feature area. | SKILL.md Forbidden | User directly requests implementation; no spec mentioned. |
| X3 | **Test agent reads source code.** Agent derives tests from implementation details rather than spec alone. | SKILL.md Forbidden | Test seems more thorough when grounded in actual code. |
| X4 | **Lifecycle bypass.** Agent modifies spec inline during task implementation without going through the update approval flow. | v1 lesson | Agent is "in the flow"; updating the spec feels natural. |
| X5 | **Spec change disguised as refactoring.** Agent changes observable behavior under the guise of "cleanup." | SKILL.md Forbidden | The behavioral change is small and the refactor framing feels safe. |

## Severity

How lasting and hard to reverse the damage is.

### Critical — false authority that propagates

| # | Why |
|---|---|
| S2 | Behavioral spec change without real approval. Downstream tasks, tests, and implementation build on it. Cascading. |
| S6 | Spec "corrected" to match buggy code. The bug becomes authoritative. Entire spec→test→code chain poisoned. |
| T3 | Downstream work assumes feature is done. Spec TODOs removed. Discovered much later in production. |
| X4 | Spec modified without approval. No record. Other agents build on the changed spec. |
| X5 | Behavioral change undetected. No decision trail. Tests validate the wrong behavior. |

### High — loses irrecoverable context

| # | Why |
|---|---|
| D3 | Post-mortem knowledge never captured. Can't be reconstructed months later. |
| D4 | Offhand remark becomes authoritative. Future work references it as a real commitment. |
| T7 | Cancellation rationale lost. Irrecoverable context about why work was abandoned. |
| X1 | Root cause of implementation-coupled tests (X3). Nobody rewrites passing tests. Load-bearing ordering. |
| X2 | Code without governing spec. Drift detection blind. Behavior defined only by implementation. |

### Medium — governance gaps, fixable on discovery

| # | Why |
|---|---|
| S1 | Specs drift with every impl change. Cleanable but maintenance compounds. |
| T2 | Work escapes governance. Retroactively correctable. |
| T4 | Spec may be inconsistent. Catchable on next read. |
| T6 | Redundant task created for done work. Wastes effort, doesn't corrupt state. |
| D1 | Alters historical record of one decision. Contained scope. |
| S4 | Conflicting authority. Reconcilable once surfaced. |

### Low — friction or delay only

| # | Why |
|---|---|
| S3 | Unnecessary approval request. User says "go ahead." |
| T1 | Wrong status. Trivially correctable. |
| S5 | Governance fragmentation. Specs mergeable. |
| D2 | Orphaned decision. Linkable via search later. |
| X3 | Implementation-coupled tests. Detectable on refactor. |

## Constraints

- Do not create a new entry that is near-identical to an existing one. If two pitfalls differ only in which entity they manifest through (e.g., "hotfix archived without decision" vs. "skipped decision for hotfix"), they are the same pitfall — merge them or keep one.

## Anticipated Changes

- New pitfalls discovered from exam results or production incidents.
- Severity re-evaluation as methodology enforcement matures.
