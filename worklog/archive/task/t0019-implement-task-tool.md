+++
id = "t0019"
title = "Implement the task tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0012"]
blocked_by = ["t0013"]
+++

# Implement the task tool

After its proposed behavior in s0005 is approved, implement `worklog task` for task lifecycle transitions and atomic closure.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when `start`, `block`, `resume`, `finish`, and `cancel` are shipped and their transition, dependency, close-out, atomic archival, already-resolved, batch, failure, and result workflows are verified.

## Completion evidence (NEEDS APPROVAL)

Delivered `worklog task (start|block|resume|finish|cancel) TASK... [options]` through `worklog.py` and `worklog_lib/task_command.py`.
The command enforces the complete task lifecycle: transition validation, dependency checks against unresolved `blocked_by` tasks, recorded reasons for block and cancel actions, and required check descriptions on resume.

Atomic task closure (`finish` and `cancel`) verifies that governing specs in `modifies` have no unapproved markers, updates the task status, and atomically archives the entity file to `archive/task/`.
Already-resolved archived tasks are handled idempotently.
Supports independent batch processing where errors on one task do not affect other targets.

Behavioral unit tests in `tests/test_tools.py` cover lifecycle transitions, dependency gating, reason appending, atomic archival on finish/cancel, spec review enforcement before closure, and independent batch handling.
Reconciled with governing specs s0002, s0003, s0005, s0008, s0009, and s0012; updated implementation paths and cleared tool implementation markers.
