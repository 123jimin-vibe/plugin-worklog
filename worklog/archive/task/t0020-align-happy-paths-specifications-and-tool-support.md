+++
id = "t0020"
title = "Align happy paths, specifications, and tool support"
status = "done"
modifies = ["s0002", "s0003", "s0004", "s0005", "s0006", "s0008", "s0009", "s0010", "s0011", "s0012", "s0013", "s0015", "s0016", "s0017", "s0018", "s0019", "s0020"]
+++

# Align happy paths, specifications, and tool support

1. Amend n0002.
2. Check whether n0003 needs revision, and revise it where needed.
3. Review every in-scope spec to determine whether the current specification is sufficient for the amended happy paths.
   Identify and address ambiguous parts.
4. Review whether the current tools sufficiently support the amended happy paths.

Agent-development work, particularly t0007 and t0011, is outside this task because it is still pre-development.

## Proposed approach and completion conditions

Amend n0002 around how understanding develops during actual work, not merely how a predetermined plan is executed.
In particular, account for tasks that begin without precise requirements or a complete understanding of affected specs and develop through implementation.
Evaluate the following related changes rather than treating them as already-approved methodology:

- Delivery against existing specs as well as introducing new intended behavior.
- Evolving task detail, boundaries, decomposition, dependencies, and work order.
- Refining spec coverage and boundaries as the enduring concepts become clear.
- Updating established decisions and delivered state during work, not only at closure.
- Continuing an existing task with enough current context to resume it.
- Developing acceptance criteria through evidence and human feedback without silently weakening established requirements.
- Ordinary investigation/delivery handoffs, appropriate evidence destinations, and valid outcomes that require no implementation or follow-up task.
- Approval and verification modes, and whether chore exemptions distinguish accurate wording from sufficient coverage.

Review n0003 for pitfalls exposed by these workflows, distinguishing legitimate uncertainty and refinement from stale records, unapproved scope growth, and premature completion.
Do not turn every observed execution mistake into another mandatory happy-path step.

Review each non-agent spec individually, recording whether it is sufficient, needs clarification, or conflicts with the amended workflows.
The initial `modifies` set covers the non-agent editable specs under review; it does not assert that every one needs an edit.
Review s0001 without editing it and report any issue requiring human action.
Exclude agent-specific s0007 and s0014 along with t0007 and t0011; shared entity, task, and authority rules remain in scope.
Maintain the affected-spec relationships as the work becomes better understood, and respect each entity's effective agent mode.

Exercise representative amended workflows with the current tools.
Distinguish supported manual work from genuine tool gaps, and identify the required response to each gap rather than assuming every workflow needs a new command.
Tool implementation is not an automatic deliverable of this review.
During creation of this task, `status` reported reference-file parsing errors and `create task` refused creation because of those unrelated errors; include that failure isolation issue in the tool assessment.

Complete when n0002 is amended, n0003 has a justified revision or no-change decision, every in-scope spec has a review disposition with required ambiguity resolutions addressed, and the tool review records exercised scenarios, sufficiency findings, and recommended actions for gaps.
Report unresolved authority decisions explicitly; required unapproved spec content is not completed work.

## Specification review

The user-reviewed n0002 and n0003 are the basis for this review.
All 18 non-agent specs were reviewed.

| Spec | Disposition |
| --- | --- |
| s0001 | Sufficient unchanged. Durable shared intent, units of work, and varying human involvement permit the revised workflows. No human-only edit is required. |
| s0002 | Sufficient unchanged. Identity, hierarchy, current-state writing, and marker rules support developing entities without a new schema. |
| s0003 | Sufficient unchanged. Incremental coverage follows creation and related-spec rules; same-session maintenance already applies during ongoing tasks. |
| s0004 | Sufficient unchanged. The skill contract requires reliable entity choice, task execution, verification, and write-back without enumerating every scenario. |
| s0005 | Sufficient unchanged. Action-scoped validation, independent batches, and preservation cover the required tool operations. |
| s0006 | Unchanged. No auxiliary skills are currently specified. |
| s0008 | Sufficient unchanged. Project policy remains independent of task shape or progress. |
| s0009 | Approved clarification. Allows incomplete initial requirements and coverage, with finalizing affected specs before activation recommended for coordination. Keeps scope, dependencies, evidence requirements, and continuation state current; covers findings/specification outcomes and the chore exemption. |
| s0010 | Approved clarification. Reusable non-authoritative findings can belong in notes, not only guidance described as unverifiable project behavior. |
| s0011 | Approved clarification. Reference interpretation may belong in a citing task as well as a note or spec. |
| s0012 | Sufficient unchanged. Execution permission covers then-listed specs; adding another spec to `modifies` leaves its own effective mode in force. Required content approval and edit permission remain separate. |
| s0013 | Sufficient unchanged. Initialization establishes structure, not semantic coverage, and supports gradual adoption. |
| s0015 | Sufficient unchanged. Classification and tag maintenance are independent of task refinement. |
| s0016 | Sufficient unchanged. Registry operations complement entity classification without imposing a workflow type. |
| s0017 | Sufficient unchanged. Status provides declared relationships and actionability; task findings still require reading the task. |
| s0018 | Sufficient unchanged. Minimal creation permits initially empty coverage and creates no invented scope. |
| s0019 | Sufficient unchanged. Existing field operations support revised coverage, dependencies, hierarchy, and classification while preserving task prose. |
| s0020 | Current behavior is explicit, with a limitation: approval checks cover whole governing specs rather than only the task's required content. See the tool review. |

The user approved the changes to s0009, s0010, and s0011, with finalizing affected specs before activation recommended to avoid confusion between agents working on different tasks.
The one-session task preference remains a preference, not a prohibition on continuing an existing task.
Agent-specific s0007 and s0014 remain excluded.

## Tool review

Exercised the current CLI in a disposable project with unrelated malformed reference files.
After correcting a sandbox-directory setup error recorded in n0004, 29 CLI calls produced 24 successful exits and five expected nonzero results.

| Scenario | Observed result |
| --- | --- |
| Initialize and begin before precise coverage is known | Initialization and minimal pending-task creation succeeded; activation accepted an empty `modifies` list. |
| Discover coverage and decompose active work | Added a governing spec, a child task, and a dependency; metadata changes preserved task prose. |
| Block and continue | Premature resume was rejected without mutation. After the child finished and archived, resume succeeded while retaining the resolved dependency. |
| Refine paths and orient work | Added governed paths; source-path status found the spec. Status preserved file contents and reported the active task with its archived prerequisite. |
| Close a negative or specification-only outcome | Both tasks finished and archived without an implementation artifact. Semantic acceptance remained the caller's responsibility. |
| Deliver a bounded part of a larger spec | Closure succeeded while unrelated `UNIMPLEMENTED` behavior remained marked. |
| Isolate relevant failures | A valid field target changed despite an invalid sibling target; a missing required spec prevented creation without changes. |
| Ignore unrelated malformed references | Task/spec creation and targeted status succeeded without reference diagnostics. The earlier creation failure did not recur. |
| Maintain classification | Tag creation and applying the tag to a task succeeded without unrelated-reference diagnostics. |
| Enforce approval | Required draft spec content prevented closure and left the task active. |
| Close beside an unrelated draft in the same spec | Closure was also rejected when only an out-of-scope proposal remained unapproved. |

Ordinary editing remains sufficient for task findings, specification prose, and marker maintenance.
No new command is needed merely to grow or split a task.
The chore exemption requires a judgment about whether to use worklog, not another tool operation.

The outstanding tool limitation is s0020's spec-wide approval gate.
s0012 prevents completion while required spec content needs approval, but the tool cannot distinguish that content from an unrelated proposal within the same `modifies` spec.
The implementation follows its current contract; this is a capability limitation, not an unexplained implementation failure.
Recommended follow-up: determine how task-relevant approval scope can be established before changing close-out behavior.
Keep the current guard until that distinction has an approved design; removing an affected spec from `modifies` is not a valid workaround.
No tool implementation changes were made.

## Completion evidence (NEEDS APPROVAL)

- Reconciled the skill with the approved task-growth, knowledge-outcome, note, and reference rules.
- Carried the pre-activation `modifies` recommendation into the skill and n0002; later discoveries can still update the list.
- Exercised 11 additional CLI calls in a disposable project: declared two tasks' scopes before activation, inspected their pending plans, added a newly discovered shared subject after activation, and confirmed status exposed both governing tasks.
- Confirmed that an investigation with unresolved coverage can still activate; no mandatory activation gate or scope lock was introduced.
- The skill is 5,650 UTF-8 bytes without BOM, uses LF line endings, and remains below the 7,646-byte limit.
- Removed the disposable project.
- The spec-wide close-out gate remains a documented limitation with a recommended design follow-up; changing it is outside this review's implementation scope.
- The existing unimplemented source-freshness mechanism in s0004 remains unchanged.
