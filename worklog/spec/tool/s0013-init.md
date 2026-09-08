+++
id = "s0013"
title = "The init tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/initialization.py"]
agent_mode = "draft"
+++

# The `init` tool

```text
worklog init [PROJECT]
```

`PROJECT` defaults to the current directory.
Invocation means the project has chosen worklog; the command does not decide adoption and MUST NOT imply adequate spec coverage.
Common tool rules follow s0005.

## Initialization

Create only missing standard directories and files:

- Entity and archive directories from s0002.
- `worklog/project.toml` from s0008, with explicit default policies from s0012.
- `worklog/tags.csv` from s0015.

Preserve existing files.
Create no semantic entities, inferred behavior, or placeholder coverage; do not modify version control or files outside `worklog/`, except bytecode permitted by s0005.

When the database is missing, scan tag metadata from all current entities and archived tasks.
Seed distinct normalized tags in alphabetical order with empty descriptions, or only the header if there are none.
Invalid tags, per-entity normalized duplicates, or unparseable metadata preventing tag discovery fail initialization; unrelated metadata defects do not.

An existing database must be valid and remains unchanged.
Unknown tags and unused rows do not prevent initialization or require discovery when the database exists.
Preserve existing configuration without loading its policy for unrelated mode diagnostics.
A complete compatible worklog MUST NOT trigger entity scans or writes.

Required-path conflicts fail without partial changes or a destructive `--force` mode.
Failure identifies each structural conflict and leaves the project unchanged.

Success reports “Worklog initialized”, “Worklog structure completed”, or “Worklog already initialized”, with the project and created/existing paths.
