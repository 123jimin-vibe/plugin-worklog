+++
id = "s0020"
title = "The task tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/task_command.py"]
+++

# The `task` tool

```text
worklog task COMMAND TASK... [--project PROJECT]
```

Shared rules follow s0005; lifecycle and approval obligations follow s0009 and s0012.

| Command | Starting status | Result |
| --- | --- | --- |
| `start` | pending | active |
| `block --reason TEXT` | pending, active | blocked; append reason |
| `resume --checked TEXT` | blocked | active; append check |
| `finish` | active, done | done and archived |
| `cancel [--reason TEXT]` | pending, active, blocked, cancelled | cancelled and archived |

- `start`, `resume`, and `finish` require resolved dependencies, including archived tasks.
- Block reasons, resume checks, and reasons for new cancellations must be non-empty.
  Resume checks describe checking that the blocker no longer prevents work.
  Already-cancelled tasks need no new reason.
- `finish` and `cancel` apply terminal status and archival atomically after close-out checks.
  Repeating the matching operation on an archived task is a no-op; other terminal-state transitions are rejected.

## Close-out and results

Before closing a current task, the tool MUST resolve `modifies` specs and reject invalid, missing, or wrong-type references.
Their `NEEDS APPROVAL` or `NEEDS REVIEW` content prevents closure; code examples do not.
The caller remains responsible for semantic verification, approval review, and spec write-back.
Tool success MUST NOT be presented as proof of completion.

Report each target's state, mode, and archival result.
Close-out output also identifies governing specs and modes and reminds the caller of verification and write-back obligations.

Actions read selected tasks and needed mode policy; only `start`/`resume`/`finish` require dependency resolution, and only current-task closure requires governing-spec checks.
Archived no-ops require neither dependency nor governing-spec scans.
Task actions MUST NOT scan unrelated entities, hierarchy graphs, or tag usage, or read the tag database.
