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

- **Durable behavior has no spec** — High; observed; s0003.
  - Failure: Behavior expected to outlast the current task is implemented without a governing spec.
  - Pressure: A direct implementation request makes specification feel optional.
  - Check: Identify the governing spec before implementing durable behavior; extend one or create one when none applies.

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

- **Current state stranded in task history** — Critical; observed; s0002, s0003, s0009.
  - Failure: A task is completed or archived while affected specs or markers still describe the pre-task state.
  - Pressure: The task body or archive feels like a durable substitute for spec write-back.
  - Check: Reconcile every spec in `modifies`, including stale markers, before archiving the task.

- **Task status not kept current** — Medium; observed; s0009.
  - Failure: Work begins without `active`, finishes without `done`, or remains blocked after its blocker is gone.
  - Pressure: Status maintenance is deferred until after the substantive work.
  - Check: Update status at each lifecycle transition rather than during later cleanup.

- **Governance links do not match the implementation surface** — High; observed; s0003, s0009.
  - Failure: A spec's `paths` omit files implementing its behavior or are so broad that drift ownership is unclear, or a task omits affected specs from `modifies`.
  - Pressure: Manual knowledge of file relationships makes metadata seem optional or redundant.
  - Check: Map each changed behavioral surface to its governing spec and keep `paths` precise; list every touched governing spec in `modifies`.

### Additional observed pitfalls

#### Project adoption

- **Parallel authority introduced through partial Worklog adoption** — High; observed; s0002.
  - Failure: Worklog is introduced beside an established authoritative process, or covers only one contributor or subsystem while presenting itself as project state.
  - Pressure: Adding another ledger appears safer than deciding which record is authoritative.
  - Check: Confirm adoption with the human, identify the authoritative record and workflow, and establish project-wide coverage before initializing Worklog.

#### Spec integrity

- **Requirement strength left implicit** — Medium; observed; s0002.
  - Failure: Binding requirements use ordinary declarative prose, leaving required, recommended, and optional behavior indistinguishable.
  - Pressure: Natural-language statements already sound authoritative.
  - Check: Classify each behavioral statement explicitly with `MUST`, `SHOULD`, or `MAY`.

#### Task lifecycle

- **Worklog state reconstructed after delivery** — High; observed; s0002, s0009.
  - Failure: Work proceeds from an external plan or without a task, then the task is created already done or archived, if it is created at all.
  - Pressure: Interactive planning tools feel sufficient during execution, and an after-the-fact record appears equivalent.
  - Check: Create and activate the task before reviewable work begins; keep temporary plans subordinate to its current state.

- **Task dependency metadata does not match reality** — Medium; observed; s0009.
  - Failure: A task depends on another task in practice or in its body, but `blocked_by` omits that dependency or retains a resolved one.
  - Pressure: The dependency seems obvious from prose or current session context.
  - Check: Reconcile `blocked_by` whenever prerequisites or task status change.

#### Verification and completion

- **Claimed result stronger than evidence** — Critical; observed; s0009.
  - Failure: A task claims completion, correctness, or exhaustion from evidence that does not exercise the claimed boundary or decisive counterexamples.
  - Pressure: Builds, unit tests, synthetic fixtures, forced state, aggregate metrics, authentication failures, or producer-side success provide convenient green signals.
  - Check: Define the actual delivery boundary before implementation and verify it with representative evidence; disclose unavailable verification without generalizing the proxy result.

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
