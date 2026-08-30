+++
id = "s0008"
title = "Worklog project configuration"
+++

# Worklog project configuration

A worklog project MAY use `worklog/project.toml` to configure worklog for that project.

## File

`worklog/project.toml` is a TOML file; an absent `project.toml` is equivalent to an empty one.
The file's own agent mode is always `read_only` as defined by s0012.

## Entity policy tables

The tables `spec`, `task`, and `note` configure project-level policy for their corresponding entity types.

Each table MAY contain `agent_mode`.
Its value MUST be an agent mode defined by s0012.

## In-band guidance

`worklog/project.toml` SHOULD contain comments sufficient to interpret it without access to the worklog plugin.

The comments SHOULD:

- identify the file as worklog project configuration;
- state that agents MUST treat the file itself as read-only;
- explain that omitted entity policies use the defaults from s0012;
  - For clarity, `project.toml` SHOULD state the policy for every applicable entity type instead of relying on implicit defaults.
- describe each configured `agent_mode` using the corresponding wording recommended by s0012.

Suggested generated header:

```toml
# worklog project configuration.
# Agents MUST treat this file as read-only and SHOULD NOT prepare changes unless asked.
```

Example configured policy:

```toml
[spec]
# Before applying a change, agents MUST obtain human approval of its content or permission scoped to the edit.
agent_mode = "propose"
```
