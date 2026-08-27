+++
id = "s0012"
title = "Agent mode"
+++

# Agent mode

Agent mode governs how agents may create or change Worklog entities.

## Related entities

- s0002 defines common entity fields and approval rules.
- s0008 defines how `worklog/project.toml` configures project-level modes.
- s0011 defines references, to which agent mode does not apply.

## Entity policy

Agent mode applies to specs, tasks, and notes.

An entity's effective agent mode is selected in the following order:

1. The entity's `agent_mode` override.
2. The project-level mode for its type configured through s0008.
3. The default mode for its type.

| `agent_mode` | Agent behavior |
| --- | --- |
| `read_only` | Humans write. Agents MUST NOT create or change entities and SHOULD NOT prepare changes unless asked. |
| `propose` | Agents propose changes, but MUST obtain human approval before applying each change. |
| `draft` | Agents may apply changes, but MUST mark them as awaiting human approval. |
| `autonomous` | Agents may apply changes without routine human confirmation. |

The default modes are:

| Entity | Default mode |
| --- | --- |
| Spec | `propose` |
| Task | `draft` |
| Note | `draft` |

Humans may create or change entities in every mode.

## Entity overrides

A spec, task, or note MAY declare `agent_mode` in its TOML frontmatter.
The declared mode overrides both its project-level mode and its type's default mode.

An agent MUST NOT introduce or relax an override without prior human approval.
An agent MUST NOT represent a draft change as human-approved before receiving that approval.
