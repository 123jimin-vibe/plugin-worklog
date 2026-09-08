+++
id = "s0009"
title = "Task entities"
paths = ["plugin/skills/worklog/scripts/worklog_lib/entity_commands.py", "plugin/skills/worklog/scripts/worklog_lib/task_command.py", "plugin/skills/worklog/scripts/worklog_lib/status_command.py"]
+++

# Task entities

## Related entities

- s0002 defines common entity rules.
- s0003 defines the specs that tasks modify.
- s0012 defines agent modes and entity policy.
- n0001 guides writing.
- n0002 describes the expected happy path.

## Principles

- A task is one unit of work expected to be completable in one session.
- Task scope is subordinate to the specs it modifies.
- `status` MUST track the task's current state in real time.
- Archived tasks are history and MUST NOT be treated as current-state references.
  - Consult specs instead.

## Inherent properties

### Identity

- ID prefix: `t`.

### Fields

- A task declares `status` and the spec IDs it `modifies`.
- A task MAY declare `blocked_by`: IDs of tasks that need to be resolved first.
  - `blocked_by` records task dependencies only; it does not explain a blocking condition or represent an external blocker.

### State

- `pending`: work has not started.
- `active`: work is in progress.
- `blocked`: a dependency or external cause explicitly prevents work.
- `done`: work is complete.
- `cancelled`: work will not be completed.
- A task is resolved when its status is `done` or `cancelled`.
- Set `active` before work begins. Agents SHOULD NOT skip `active` or defer status updates until after completion.
- A blocked task SHOULD state what prevents progress, its effect on the task, and what would allow work to resume.
  - This explanation SHOULD NOT merely repeat `blocked_by` IDs.
  - A task is unblocked only after checking that the stated condition no longer prevents work.
- A task is done only when the delivered work meets its stated completion conditions.
  - Stubs, mocks, and placeholders MUST NOT count as done.

### Archival

- Tasks may be archived per s0002.

## Desirable properties

### Scope

- Reviewable work SHOULD have a task.
  - A chore or urgent fix MAY omit a task when it finishes in the current session and leaves no follow-up or resumable state.
- Work spanning more than one session SHOULD be split into multiple tasks.
- A task MAY begin with incomplete requirements or unidentified affected specs.
  - It is RECOMMENDED to finalize list of affected specs before a task is put in `active` state.
  - State the known outcome, initial completion conditions, and unresolved questions.
- Refine the scope, completion conditions, and task breakdown as understanding develops.
- Completion conditions SHOULD identify the evidence and any required human acceptance.
  - Findings or a reviewed specification MAY complete a task when that is its stated outcome.
- Record known affected specs in `modifies` and update it as governing coverage becomes clear.
  - State unresolved coverage in the task.
- Update `blocked_by` when actual prerequisites change.
- If evidence or conclusions conflict with a spec, notify the user.

### Body organization

- A task body MAY be free-form and need no sections.
- Add a heading only when it makes necessary content easier to find, and name it for that content.
- `Done when` MAY state planned completion conditions, while `Completion evidence` MAY record performed checks and material limitations.

### Lifecycle

- Keep findings, unresolved questions, remaining work, and next actions clear enough to continue the task.
- Before continuing work, check recorded progress and prerequisites against the current project state.
- Before archiving, fold the delivered state into every spec in `modifies`, or confirm that its existing wording covers the delivery.
- Archive a task as soon as it is resolved.
- Done, cancelled, and archived tasks SHOULD remain terminal.
  - Record further work as a separate task referencing the resolved task.
