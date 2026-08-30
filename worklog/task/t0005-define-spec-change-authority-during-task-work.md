+++
id = "t0005"
title = "Define spec-change authority during task work"
tags = ["agent-mode", "methodology"]
status = "pending"
modifies = ["s0012"]
+++

# Define spec-change authority during task work

Revise s0012 to define how a spec's effective `agent_mode` governs agent-authored changes,
including changes made while executing or closing a task.
The existing `autonomous` semantics need no further clarification.

Retain the two approval paths for `propose`:

1. The human approves the specific proposed content before the agent applies it.
2. The human permits the agent to edit a specified entity without approving the resulting content in advance.
   The agent marks content applied through this path `NEEDS APPROVAL`.

Keep the two human actions distinct:
approval of specific content makes that content authoritative when applied;
permission to edit authorizes the edit but does not approve its content.

Define task-driven spec changes precisely for `read_only`, `propose`, and `draft`.
The rules must distinguish:

- authority conveyed by the task's content from permission to edit its `modifies` specs;
- human-approved task requirements from agent-inferred behavioral changes;
- behavioral specification from verified implementation-state write-back;
- an explicit human instruction to execute the task from the task's mere existence, metadata, or status; and
- changes that may be applied immediately from changes that prevent implementation or task closure until human action.

Complete when:

- s0012 defines the prerequisites, authority consequences, and marker requirements for task-driven spec changes under each non-`autonomous` mode;
- s0012 states when human authorization of a task constitutes content approval, edit permission, both, or neither;
- s0012 states how unresolved `NEEDS APPROVAL` content affects implementation, task completion, and archival;
- its recommended adjacent and standalone descriptions remain consistent with those paths;
- permission to edit never causes unapproved agent-authored content to appear authoritative; and
- s0012 remains consistent with the approval and `NEEDS APPROVAL` rules in s0002 and s0003.
