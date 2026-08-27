+++
id = "s0005"
title = "Plugin tooling"
+++

Tools shipped with the plugin for managing worklogs: inventory, purpose,
usage requirements.

## Common tool behavior

### Implementation

- Tools MUST be written in Python.
  - Each tool SHOULD NOT introduce an additional dependency.
- Tools SHOULD expose workflow operations instead of requiring callers to manipulate entity file frontmatter directly.

### Entity IDs

- Every entity ID parameter MUST follow the identity and interoperability rules in s0002.
- Tools SHOULD emit entity IDs in standard form.

### Batch operations

- An operation that can target multiple independent entities SHOULD accept multiple targets in one invocation.
  - Examples include creating multiple entities and archiving multiple tasks.
  - A batch operation SHOULD report the result for each target.
  - Whether a failed target prevents changes to the remaining targets MUST be specified.

### Tool communication

Tool messages are produced through an installed worklog plugin and need not independently explain the complete methodology.

Help text, error messages, and normal output SHOULD provide enough local context to understand:

- what operation or result the message concerns;
- whether the operation changed worklog state;
- whether the caller may proceed;
- what action, if any, the caller should take next.

Messages MAY assume familiarity with basic worklog vocabulary, including specs, tasks, and entity ID syntax.

When relevant to the immediate operation, messages SHOULD restate constraints that agents are likely to forget, including:

- lifecycle preconditions and consequences;
- the effective or default `agent_mode`;
- required human review or approval;
- conditions that prevent completion or archival;
- safe remediation after a failure.

Messages SHOULD NOT repeat general methodology, obvious argument meanings, or unrelated constraints solely to be fully standalone.
Messages MAY refer to the worklog skill for background information.

### Generated files

Unlike tool messages, generated files SHOULD remain understandable and usable without the worklog plugin.
Generated files SHOULD contain concise comments identifying their purpose and any non-obvious fields, authority, or handling, following the governing specs.

## `init` (UNIMPLEMENTED)

Initializes worklog for a project.

### Usage

```text
worklog init [PROJECT]
```

`PROJECT` is the project directory.
It defaults to the current directory.

Running `init` means that the project has chosen to use worklog.
The command does not decide whether worklog is appropriate for the project.

### Behavior

`init` creates the minimum valid worklog structure defined by s0002.

It:

- creates the standard entity and archive directories;
- creates `worklog/project.toml` as defined by s0008 when it does not exist;
- writes explicit policies for specs, tasks, and notes using the default modes from s0012;
- preserves every existing worklog file;
- reports which paths it created and which already existed.

It does not:

- create specs, tasks, notes, references, or decisions;
- infer behavior from source code or project documentation;
- generate placeholder project coverage;
- initialize or modify version control;
- modify files outside `worklog/`;
- rewrite an existing `project.toml`.

Creating semantic entities belongs to later workflow steps.
Initialization alone MUST NOT imply that the project has adequate spec coverage.

### Existing worklogs

`init` is idempotent.

When the project already has a complete worklog, it makes no changes and exits successfully.

When the project has a partial but compatible worklog, it creates only the missing standard structure.
Existing v0.1 entities and directories are preserved for backward compatibility.

If a required path is occupied by an incompatible file or directory, `init` fails without making partial changes.
It never requires a destructive `--force` mode.

### Result

Success reports one of:

- Worklog initialized.
- Worklog structure completed.
- Worklog already initialized.

The result also identifies the project directory and the paths created.

Failure identifies each structural conflict and leaves the project unchanged.
