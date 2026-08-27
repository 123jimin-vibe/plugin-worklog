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

## Recommended in-band descriptions

When `agent_mode` is declared in entity frontmatter or project configuration, a nearby comment SHOULD describe its effect.

The following descriptions use `{scope}` for either the individual entity or the configured entity type:

| Mode | Recommended description |
| --- | --- |
| `read_only` | Agents MUST treat {scope} as read-only and SHOULD NOT prepare changes unless asked. |
| `propose` | Agents MAY propose changes to {scope}, but MUST obtain human approval before applying them. |
| `draft` | Agents MAY change {scope}, but MUST mark agent-authored changes as `NEEDS APPROVAL`. |
| `autonomous` | Agents MAY change {scope} without routine human approval. |

The description MAY be adapted grammatically to its scope but MUST preserve the mode's meaning and MUST NOT grant additional rights to agents.

Such comments MUST NOT be regarded as establishing authority independently of the `agent_mode` field.

Example entity override:

```toml
# Agents MUST treat this entity as read-only and SHOULD NOT prepare changes unless asked.
agent_mode = "read_only"
```
