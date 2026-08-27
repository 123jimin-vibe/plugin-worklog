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

- **Durable behavior has no spec** — High; anticipated; s0003.
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

- **Overlapping spec created unnecessarily** — Low; observed; s0002, s0003.
  - Failure: A new spec duplicates or fragments behavior already governed elsewhere.
  - Pressure: A narrow request appears easier to isolate than integrate.
  - Check: Search existing entities and extend the governing spec unless the subject is genuinely distinct.

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

- **Governed specs omitted from `modifies`** — Medium; anticipated; s0009.
  - Failure: A task touches behavior governed by a spec but omits that spec from `modifies`.
  - Pressure: Refactoring or chores appear unrelated to behavior even when they touch governed files.
  - Check: Compare the work boundary with spec subjects and `paths`, not only with the task's label.