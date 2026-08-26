+++
id = "s0008"
title = "Worklog project configuration"
+++

# Worklog project configuration

A Worklog project MAY use `worklog/project.toml` to define how agents interact with its entity types.

## Entity policy

Tables are named `spec`, `task`, or `note`. Each present table MAY set `agent_mode`.

| `agent_mode` | Agent behavior |
| --- | --- |
| `read_only` | Humans write. Agents MUST NOT create or change entities and SHOULD NOT prepare changes unless asked. |
| `propose` | Agents propose changes, but MUST obtain human approval before applying each change. |
| `draft` | Agents may apply changes, but MUST mark them as awaiting human approval. |
| `autonomous` | Agents may apply changes without routine human confirmation. |

If not specified, following values are used as default `agent_mode`:

| Entity | Default value |
| --- | --- |
| `spec` | `propose` |
| `task` | `draft` |
| `note` | `draft` |
| `ref` | `read_only` for convenience, but s0011 takes precedence |

Humans may create or change entities in every mode.
`agent_mode` of `project.toml` itself is always `read_only`.

## Entity overrides

A spec, task, or note MAY set its own `agent_mode` in TOML frontmatter, which overrides the default per-type value.
An agent MUST NOT introduce or relax an override without prior human approval.

An agent MUST NOT represent a draft change as human-approved before receiving that approval.
