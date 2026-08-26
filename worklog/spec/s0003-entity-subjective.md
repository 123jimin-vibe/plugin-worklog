+++
id = "s0003"
title = "Worklog entities: subjective specification"
+++

# Worklog entity judgment

s0002 defines entity structure; n0001 guides writing. n0002 describes the expected happy path; n0003 records pitfalls.

## Common rules

- Write for a reader with no session context.
- Extend an existing entity rather than create an overlapping one.
- Keep each entity to one subject; split entities that cover distinct subjects.
- Record current state and intent, not how they arose.
- Cite another entity by ID instead of restating it.
- Express requirement strength with MUST, SHOULD, or MAY.
- An agent MUST NOT present unapproved content as decided. Discussion is not approval.

## Spec

- Create a spec for behavior expected to outlast the current task.
- State observable behavior, constraints, known failure modes, and expected future changes.
- A spec SHOULD NOT contain behavior-independent implementation details or individual file paths.
  - Name governed files with `paths` globs.
- Include only user-stated behavior and its direct entailments as authoritative content.
  - Clearly mark other content as unapproved.
- A spec outranks source code and tests.
  - Treat divergence as a code defect.
  - If the spec seems wrong, raise it with the user; never override it silently.
- Specs MUST NOT contradict each other.
  - Before changing a spec, check specs governing related behavior.
- Behavioral changes require the user's approval, including changes made while implementing a task.
- Update a spec in the same session as any change that invalidates it.
- Remove behavior the spec no longer governs; do not retain it as history.

## Task

- Create a task for work that produces a reviewable change.
- Work spanning more than one session SHOULD be split into multiple tasks.
- State the intended outcome and completion criteria.
- List in `modifies` every spec whose governed behavior the work touches.
  - Leave it empty only when no spec governs the work.
- Task scope is subordinate to the specs it modifies.
  - If findings conflict with a spec, notify the user.
- `status` MUST track the task's current state in real time.
  - Set `active` before work begins. Agents MUST NOT skip `active` or defer status updates until after completion.
- A task is done only when the delivered work meets its completion criteria.
  - Stubs, mocks, and placeholders MUST NOT count as done.
- Before archiving, fold the delivered state into every spec in `modifies`, or confirm that its existing wording covers the delivery.
- Archive a task as soon as it is resolved.
- A resolved task SHOULD NOT be reopened.
  - Instead, create a new task referencing the resolved task.
- Archived tasks are history and MUST NOT be treated as current-state references.
  - Consult specs instead.

## Note

- Create a note for guidance that is not verifiable as project behavior, such as conventions, recurring mistakes, or working advice.
- When its guidance becomes authoritative, move its content to a spec.
  - Remove the note when one or more specs completely replace it.

## Reference

- Create a reference only when the external material is consulted repeatedly or its source may change or disappear.
- Contents SHOULD preserve the source's contents.
  - Format conversion and partial extraction MAY be performed.
  - Copied contents SHOULD NOT be rephrased or supplemented with clarification.
- Put judgment or comments about a reference in the spec or note that cites it, never in the reference itself.

## Review

- A human approves worklog entities. An agent MUST NOT treat an entity it wrote as reviewed.
- Keep each entity short enough to read in full during review.
- At the end of a session, report entities written or changed without approval.