+++
id = "s0008"
title = "Worklog project configuration"
+++

# Worklog project configuration

A Worklog project MAY use `worklog/project.toml` to configure Worklog for that project.

## File

`worklog/project.toml` is a TOML file.
When the file is absent, Worklog uses the defaults defined by s0012.

The file's own agent mode is always `read_only`.

## Entity policy tables

The tables `spec`, `task`, and `note` configure project-level policy for their corresponding entity types.

Each table MAY contain `agent_mode`.
Its value MUST be an agent mode defined by s0012.
