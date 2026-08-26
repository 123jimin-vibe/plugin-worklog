+++
id = "s0003"
title = "Worklog entities: subjective specification"
+++

# Worklog entity judgment

## Relevant entries

- s0002 defines entity structure.
- s0008 defines project-level agent policy.
- n0001 guides writing.
- n0002 describes the expected happy path.
- n0003 records pitfalls.

## Common rules

- Write for a reader with no session context.
- Extend an existing entity rather than create an overlapping one.
- Keep each entity to one subject; split entities that cover distinct subjects.
- Record current state and intent, not how they arose.
- Cite another entity by ID instead of restating it.
- Express requirement strength with MUST, SHOULD, or MAY.
- An agent MUST NOT present content awaiting human approval as approved. Discussion is not approval.

## Recommended markers

Use markers to expose state that is not evident from the content itself.

- `NEEDS APPROVAL`: content awaits required human approval and is not yet authoritative.
- `UNIMPLEMENTED`: authorized spec behavior is not implemented; it remains authoritative.
- A marker in a Markdown heading applies to the entire section rooted at that heading.
  - Example: `## UX (UNIMPLEMENTED)` marks the entire `UX` section as unimplemented.
  - A marker-only child section, such as `### UNIMPLEMENTED` under `## UX`, MAY be used to mark only part of the parent section.
- A heading marker MUST be removed when it no longer applies to every part of its section.
  - In the same change, apply the marker to every child section or statement that remains affected.
- A marker MUST be removed when its condition no longer applies.

## Spec

- Create a spec for behavior expected to outlast the current task.
- State observable behavior, constraints, known failure modes, and expected future changes.
- A spec SHOULD NOT contain behavior-independent implementation details or individual file paths.
  - Name governed files with `paths` globs.
- Include only behavior authorized by the applicable `agent_mode` and its direct entailments as authoritative content.
  - Agent-authored spec content is authoritative only after required human approval, or when the applicable mode is `autonomous`.
  - Clearly mark content awaiting human approval.
- A spec outranks source code and tests.
  - Treat divergence as a code defect.
  - If the spec seems wrong, resolve it under the applicable `agent_mode`; never override it silently.
- Specs MUST NOT contradict each other.
  - Before changing a spec, check specs governing related behavior.
- Agent-authored behavioral changes MUST follow the applicable `agent_mode`, including changes made while implementing a task.
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

## Human approval

- Apply the `agent_mode` selected by s0008 before creating or changing an entity.
- An agent MUST NOT claim human approval that it did not receive.
- It's encouraged to make small changes that can be reviewed in full.
- At the end of a session, report draft changes still awaiting human approval.