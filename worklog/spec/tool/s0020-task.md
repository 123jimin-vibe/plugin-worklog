+++
id = "s0020"
title = "The task tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/task_command.py"]
+++

# The `task` tool

Manages activation, blocking, resumption, completion, cancellation, and archival.
s0005 governs shared diagnostics, necessary I/O, independent batches, and mutation guarantees.
s0009 defines task lifecycle and spec write-back obligations; s0002 and s0012 define markers and approval rules.

## Usage

```text
worklog task start TASK... [--project PROJECT]
worklog task block TASK... --reason TEXT [--project PROJECT]
worklog task resume TASK... --checked TEXT [--project PROJECT]
worklog task finish TASK... [--project PROJECT]
worklog task cancel TASK... [--reason TEXT] [--project PROJECT]
```

## Transitions

| Command | Starting status | Result |
| --- | --- | --- |
| `start` | pending | active |
| `block` | pending, active | blocked; append the supplied reason |
| `resume` | blocked | active; append the supplied check |
| `finish` | active, done | done and archived |
| `cancel` | pending, active, blocked, cancelled | cancelled and archived |

- `start`, `resume`, and `finish` require resolved declared dependencies.
  A dependency is resolved when it is `done` or `cancelled`, including archived tasks.
- `block` requires a non-empty `--reason`.
  `resume` requires a non-empty `--checked` description of checking that the blocker no longer prevents work.
- A new cancellation requires a non-empty `--reason`.
  Closing an already-cancelled task requires no additional reason.
- `finish` and `cancel` each apply terminal status and archive as one operation.
  The matching command also archives an already-resolved current task after the same close-out preflight.
  Archival is not a separate lifecycle path.
- Repeating the matching closing command on an already archived task succeeds without a change.
  Other transitions out of terminal states are rejected; further work belongs to a new task.

## Close-out and results

Before closing a current task, the tool MUST resolve each spec in `modifies` and reject missing, invalid, or wrong-type references.
Mechanically detected `NEEDS APPROVAL` or `NEEDS REVIEW` content in those governing specs prevents closure.
Marker examples in code are not approval gates.

The tool enforces these mechanically detectable gates, not semantic completion, verification, or approval judgments.
Before invoking closure, the caller remains responsible for verification, required approval review, and spec write-back under s0009 and s0012.
Command success MUST NOT be presented as proof of completion.

Results identify each target's state, effective mode, and archival result where applicable.
Close-out output identifies the governing specs and their modes and reminds the caller of verification and write-back obligations.

## Required inputs

Each action reads its selected task and the configuration needed for mode reporting.
`start`, `resume`, and `finish` additionally resolve the dependencies needed to determine actionability.
Closing a current task additionally reads its declared governing specs for close-out gates and mode reporting.
`block` and `cancel` do not require dependencies to be resolved.
The matching no-op on an already archived task requires no new dependency or governing-spec scan.

Task lifecycle actions MUST NOT scan unrelated entities, hierarchy graphs, or tag usage, or read the tag database.
A selected task's invalid state, required dependency, or close-out gate fails that target without blocking independent targets.
