+++
id = "s0012"
title = "Agent mode"
+++

# Agent mode

Agent mode governs whether agents may change worklog entities and whether their content is authoritative.

## Related entities

- s0002 defines common entity fields and approval rules.
- s0003 defines spec authority.
- s0008 defines how `worklog/project.toml` configures project-level modes.
- s0009 defines task scope and lifecycle.
- s0011 defines references, to which agent mode does not apply.

## Policy

Agent mode applies to specs, tasks, and notes.

An entity's effective mode is selected in this order:

1. The entity's `agent_mode` override.
2. The project-level mode for its type configured through s0008.
3. The default mode for its type.

| `agent_mode` | Permission to edit | Authority of resulting content |
| --- | --- | --- |
| `read_only` | Agents MUST NOT create or change the entity and SHOULD NOT prepare changes unless asked. | A human must change the entity or its mode. |
| `propose` | Before applying a change, an agent MUST obtain approval of its content or permission scoped to the edit. | Human-approved content is authoritative. Other agent-authored content MUST be marked `NEEDS APPROVAL`. |
| `draft` | Agents MAY apply changes without prior permission. | Human-approved content is authoritative. Other agent-authored content MUST be marked `NEEDS APPROVAL`. |
| `autonomous` | Agents MAY apply changes without prior permission. | Agent-authored content is authoritative. |

Content approval and edit permission are independent; an instruction MAY grant either or both.
Approval covers the stated content and its direct entailments, not additional agent decisions.
Permission only allows changes within its stated scope and never makes their content authoritative.

The default is `propose` for specs and `draft` for tasks and notes.

Humans may create or change entities in every mode.
An agent MUST NOT introduce or relax an entity override without prior human approval,
or represent draft content as human-approved.

## Task work

The target spec's mode governs its modification; the task's mode does not.

A task's existence, fields, and status grant neither content approval nor edit permission.
An explicit human instruction to execute a task approves its then-stated requirements and direct entailments,
and permits necessary changes to its then-listed `modifies` specs except those in `read_only` mode.
It does not approve agent-inferred behavior, out-of-scope changes, or implementation state.

Agents MUST NOT implement behavior unless it is authoritative in a governing spec.
Permitted drafts MAY record other behavior as `NEEDS APPROVAL`, but agents MUST NOT implement it.

Verified implementation-state marker updates do not require content approval,
but the target mode still controls editing and implementation does not authorize behavior.

A task MUST NOT be completed or archived while required spec content remains `NEEDS APPROVAL`.
A required change to a `read_only` spec blocks the task until a human changes the spec or its mode.

## In-band descriptions

A comment next to a visible declaration SHOULD state only behavior not evident from its field, value, and scope:

| Mode | Recommended comment |
| --- | --- |
| `read_only` | Agents SHOULD NOT prepare changes unless asked. |
| `propose` | Before applying a change, agents MUST obtain human approval of its content or permission scoped to the edit. |
| `draft` | Unapproved agent-authored content MUST be marked `NEEDS APPROVAL`. |
| `autonomous` | Agents MAY change content without routine human approval. |

Otherwise, describe both permission and authority from the policy table.
Descriptions MAY be adapted grammatically but MUST preserve meaning, grant no additional rights,
and establish no authority independently of `agent_mode`.
