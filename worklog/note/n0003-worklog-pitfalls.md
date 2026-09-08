+++
id = "n0003"
title = "Worklog pitfalls"
+++

Generalized failure modes when agents use worklog.
Authoritative rules remain in specs.
Repository-specific incidents belong in n0004.

## Classification

### Severity

- Critical: silently corrupts authority, verification, or completion state.
- High: creates persistent but discoverable drift.
- Medium: repairable governance or maintenance failure.
- Low: visible friction with little persistent damage.

### Observed

- Observed: failures already encountered.
- Anticipated: failures inferred from current rules but not yet encountered.

## Pitfalls

### Authority and approval

- **Unauthorized spec modification** — Critical; observed; s0003, s0012.
  - Failure: An agent adds or changes authoritative behavior without the authorization required by the effective `agent_mode`.
  - Pressure: New behavior looks like clarification or incidental bookkeeping, especially during task work.
  - Check: Trace every behavioral change to human input, prior authoritative content, or autonomy granted by the effective `agent_mode`.

- **Implementation treated as authority** — Critical; anticipated; s0003.
  - Failure: An agent changes or disregards a spec because source code or tests behave differently.
  - Pressure: Existing implementation looks like stronger evidence than written intent.
  - Check: Treat divergence as an implementation defect unless the spec is changed under the effective `agent_mode`.

- **Behavioral change framed as non-behavioral work** — Critical; anticipated; s0003, s0009.
  - Failure: Refactoring, cleanup, or maintenance changes observable behavior without treating it as a spec change.
  - Pressure: A non-behavioral task label makes small behavior changes appear harmless.
  - Check: Compare observable behavior before and after the work, then resolve any difference under the effective `agent_mode`.

- **`UNIMPLEMENTED` treated as unapproved** — High; observed; s0002, s0003.
  - Failure: An agent treats authorized but unimplemented behavior as tentative or non-authoritative.
  - Pressure: The marker resembles a draft-status warning.
  - Check: Distinguish implementation state from approval state; only `NEEDS APPROVAL` removes authority.

### Spec integrity

- **Related specs left contradictory** — High; observed; s0003.
  - Failure: A spec change conflicts with another spec governing related behavior.
  - Pressure: The edited spec appears self-contained.
  - Check: Inspect related behavior and overlapping `paths` before changing a spec.

- **Unbuilt behavior presented as implemented** — High; observed; s0002, s0003.
  - Failure: A spec states authorized behavior as current even though it is not implemented and is not marked `UNIMPLEMENTED`.
  - Pressure: Spec writing naturally describes the intended end state.
  - Check: Verify implementation state separately from authority and mark every authorized gap.

- **Durable behavior has no spec (NEEDS APPROVAL)** — High; observed; s0003.
  - Failure: Behavior expected to outlast the current task is implemented without governing coverage, including maintenance that adds behavior without making any existing spec statement false.
  - Pressure: A small change or incomplete initial understanding makes specification feel unnecessary.
  - Check: Establish authoritative governing behavior for the part being implemented; extend coverage as new enduring subjects become known without requiring the whole task to be specified first.

- **Behavior-independent implementation detail in a spec** — Medium; observed; s0003.
  - Failure: A spec body records API shapes, internal names, individual file paths, or other details that do not affect governed behavior.
  - Pressure: Concrete implementation context makes the spec appear more precise.
  - Check: Remove details that can change without changing behavior; express governed files through `paths` globs.

- **History or narration retained in a spec** — Medium; observed; s0002, s0003.
  - Failure: A spec recounts prior states, conversations, or implementation progress instead of describing current behavior.
  - Pressure: Historical context feels necessary to explain the current wording.
  - Check: Delete statements that add neither current behavior, a constraint, nor a known failure mode.

- **Behavior duplicated or fragmented across specs** — Medium; observed; s0002, s0003.
  - Failure: A new or existing spec duplicates a behavioral rule or fragments one subject across multiple authoritative records.
  - Pressure: A narrow request appears easier to isolate than integrate, and duplicated wording appears convenient to readers.
  - Check: Search existing entities and keep each behavioral rule in one governing spec unless the subjects are genuinely distinct.

### Task lifecycle

- **Placeholder work marked done** — Critical; observed; s0009.
  - Failure: A task becomes `done` while its delivery still depends on stubs, mocks, placeholders, or incomplete behavior.
  - Pressure: Complete structure is mistaken for complete behavior.
  - Check: Evaluate the delivery against the task's completion criteria rather than its shape.

- **Current state stranded in a task (NEEDS APPROVAL)** — Critical; observed; s0002, s0003, s0009.
  - Failure: Settled decisions or verified delivered behavior remain only in an active or archived task while governing specs and markers still describe an earlier state.
  - Pressure: Spec write-back is treated as an end-of-task action, even when the task has several stages.
  - Check: Synchronize authoritative decisions and verified implementation state during work, then reconcile affected specs before archival; leave genuinely unbuilt parts marked.

- **Task status not kept current** — Medium; observed; s0009.
  - Failure: Work begins without `active`, finishes without `done`, or remains blocked after its blocker is gone.
  - Pressure: Status maintenance is deferred until after the substantive work.
  - Check: Update status at each lifecycle transition rather than during later cleanup.

- **Governance links do not match the implementation surface (NEEDS APPROVAL)** — High; observed; s0003, s0009.
  - Failure: Known affected specs or files remain absent from `modifies` or `paths`, or overly broad coverage obscures which spec governs the behavior.
  - Pressure: Initial relationships are treated as final even after implementation reveals a wider change surface.
  - Check: Record known relationships, keep unresolved coverage explicit, and revise links and spec boundaries as the affected subjects become clear.


### Developing tasks (NEEDS APPROVAL)

- **Premature task precision** — Medium; anticipated; s0009.
  - Failure: An agent delays useful work until requirements, affected specs, and the complete task breakdown are known, or invents those details to make the task look ready.
  - Pressure: Task creation is treated as transcription of a finished plan rather than the beginning of a developing work record.
  - Check: Start with the known outcome, constraints, and uncertainties; let investigation and implementation refine the task without presenting guesses as established requirements.

- **Task breakdown frozen or endlessly expanded** — Medium; anticipated; s0009.
  - Failure: Newly understood work is forced into an obsolete task breakdown, or unrelated outcomes accumulate in one growing task that cannot be reviewed or resumed clearly.
  - Pressure: The initial task boundary is mistaken for an obligation to keep every discovery together or to preserve every planned subtask.
  - Check: Revisit the breakdown when meaningful boundaries emerge, keep related discovery and delivery together, and give independently actionable remaining outcomes an explicit home.

- **Acceptance criteria adjusted to fit the result** — Critical; anticipated; s0009, s0012.
  - Failure: An agent weakens an established requirement or changes a delivery objective into an investigation verdict so that unfinished work can be marked done.
  - Pressure: Legitimate refinement of an initially imprecise task is mistaken for permission to redefine success.
  - Check: Distinguish clarification from a changed outcome, resolve intent under the applicable authority, and test completion against the resulting authorized criteria.

- **Investigation forced to produce a change** — Medium; anticipated; s0003, s0009, s0010.
  - Failure: A sufficient negative or no-change conclusion is treated as unfinished, or every finding is promoted into a spec edit or follow-up task.
  - Pressure: Product delivery is treated as the only useful outcome and write-back as a requirement to change an authoritative document.
  - Check: Close against the investigation's evidence and review conditions; retain task evidence, reusable guidance, authoritative conclusions, and actionable follow-up work only where each belongs.

## Additional observed pitfalls

#### Project adoption

- **Parallel authority introduced through partial worklog adoption (NEEDS APPROVAL)** — High; observed; s0002.
  - Failure: Worklog is introduced beside an established authoritative process, or covers only one contributor or subsystem while presenting itself as complete project state.
  - Pressure: Adding another ledger appears safer than deciding which record is authoritative.
  - Check: Confirm adoption and the authoritative record before initializing worklog; identify coverage gaps while establishing governed work rather than hiding them or demanding complete coverage before initialization.

#### Spec integrity

- **Requirement strength left implicit** — Medium; observed; s0002.
  - Failure: Binding requirements use ordinary declarative prose, leaving required, recommended, and optional behavior indistinguishable.
  - Pressure: Natural-language statements already sound authoritative.
  - Check: Classify each behavioral statement explicitly with `MUST`, `SHOULD`, or `MAY`.

#### Task lifecycle

- **Worklog state reconstructed after delivery (NEEDS APPROVAL)** — High; observed; s0002, s0009.
  - Failure: Reviewable work proceeds only from an external plan, or a task is written retrospectively without preserving actionable state during execution.
  - Pressure: Temporary planning tools seem sufficient, or task creation is delayed until its requirements and affected specs can be described precisely.
  - Check: Create or select and activate the task before substantive work; keep its current findings, uncertainties, remaining work, and next action usable for continuation, with temporary plans subordinate to that record.

- **Task dependency metadata does not match reality (NEEDS APPROVAL)** — Medium; observed; s0009.
  - Failure: A current prerequisite is missing from `blocked_by`, or the recorded relationship no longer represents the task's actual dependency.
  - Pressure: The initial plan is treated as complete, or dependencies are left implicit in task prose and session context.
  - Check: Reassess prerequisites and work order as evidence develops; update relationships when the dependency changes, without deleting a still-valid relationship merely because its prerequisite is resolved.

#### Verification and completion

- **Claimed result stronger than evidence (NEEDS APPROVAL)** — Critical; observed; s0009.
  - Failure: A task claims completion, correctness, or exhaustion from evidence that does not exercise the claimed boundary or decisive counterexamples.
  - Pressure: Builds, unit tests, synthetic fixtures, forced state, aggregate metrics, authentication failures, or producer-side success provide convenient green signals.
  - Check: Develop verification alongside the requirement, use representative evidence for the actual outcome, and obtain required human or expert judgment; disclose unavailable verification without generalizing a proxy result.

#### Cross-cutting

- **Worklog history duplicated in source comments** — Medium; observed; s0002, s0003.
  - Failure: Code comments restate specs, cite task-era changes, preserve rejected alternatives, or narrate debugging history.
  - Pressure: Session context feels useful and nearby comments appear durable.
  - Check: Retain only non-obvious local invariants and their present rationale; remove change narration and duplicated authority.

#### Backward compatibility

- **Legacy decision history rewritten or erased** — High; observed; s0002.
  - Failure: A pre-v0.2 decision is substantively edited or deleted, corrupting the historical rationale that backward compatibility requires preserving.
  - Pressure: Because new decisions are deprecated, cleanup or current intent appears to justify changing old records.
  - Check: Create no new decisions, preserve existing ones unchanged, and express current authority through specs without erasing legacy history.
