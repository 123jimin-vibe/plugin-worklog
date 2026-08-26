+++
id = "s0009"
title = "Task entities"
+++

# Task entities

A task is one unit of work expected to be completable in one session.

## Relevant entries

- s0002 defines common entity rules.
- s0003 defines the specs that tasks modify.
- s0008 defines project-level agent policy.
- n0001 guides writing.
- n0002 describes the expected happy path.

## Structure

- ID prefix: `t`.
- A task declares `status` and the spec IDs it `modifies`.
  - `pending`: work has not started.
  - `active`: work is in progress.
  - `blocked`: a dependency or external cause explicitly prevents work.
  - `done`: work is complete.
  - `cancelled`: work will not be completed.
- A task MAY declare `blocked_by`: IDs of tasks that need to be resolved first.
- A task is resolved when its status is `done` or `cancelled`.

## Judgment and lifecycle

- Create a task for work that produces a reviewable change.
- Work spanning more than one session SHOULD be split into multiple tasks.
- State the intended outcome and completion criteria.
- List in `modifies` every spec whose governed behavior the work touches.
  - Leave it empty only when no spec governs the work.
- Task scope is subordinate to the specs it modifies.
  - If findings conflict with a spec, notify the user.
- `status` MUST track the task's current state in real time.
  - Set `active` before work begins. Agents MUST NOT skip `active` or defer status updates until after completion.
- Only tasks MAY be archived.
- A blocked task MUST state what prevents work. It is unblocked only after checking that the stated cause no longer prevents work.
- A task is done only when the delivered work meets its completion criteria.
  - Stubs, mocks, and placeholders MUST NOT count as done.
- Before archiving, fold the delivered state into every spec in `modifies`, or confirm that its existing wording covers the delivery.
- Open tasks live in `worklog/task/`.
- Archive a task as soon as it is resolved.
- Archived tasks are stored as `worklog/archive/task/{filename}.md`; subdirectories are not allowed.
- Done, cancelled, and archived tasks SHOULD remain terminal.
  - Record further work as a separate task referencing the resolved task.
- Archived tasks are history and MUST NOT be treated as current-state references.
  - Consult specs instead.
