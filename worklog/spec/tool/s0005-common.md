+++
id = "s0005"
title = "Common tool rules"
+++

# Common tool rules

Tools shipped with the plugin for managing worklogs.

Individual tool specs define each tool's usage and behavior.

## Related tools

- s0013 defines the `init` tool.

## Tool inventory

### `init` — UNIMPLEMENTED (t0006)

Initializes the minimum compatible worklog structure after the project has chosen to use worklog.
It is idempotent, preserves existing worklog data, and neither creates semantic entities nor implies adequate spec coverage.

```text
worklog init [PROJECT]
```

### Proposed additions (NEEDS APPROVAL)

#### `status`

Summarizes the current worklog or a working set selected by entity IDs and project paths so an agent can orient or resume without reading every entity.
It resolves canonical entities, effective agent modes, governing specs, hierarchy, task dependencies and actionability, relevant markers, and the next mechanically available worklog actions.

```text
worklog status [ENTITY...] [--path PATH...] [--project PROJECT]
```

#### `create`

Creates one or more specs, tasks, or notes with allocated standard IDs, minimal valid content, and only fields available to that entity type.
It validates relationships before writing, avoids fixed body templates, and reports the effective agent mode and any content that still needs human approval.

```text
worklog create (spec|task|note) (--title TITLE [--body FILE] | --from MANIFEST) [--parent ID] [--tag TAG...] [--agent-mode MODE] [--paths GLOB...] [--modifies SPEC...] [--blocked-by TASK...] [--project PROJECT]
```

#### `set-parent`

Sets or clears the organizational parent of one or more specs, tasks, or notes without implying dependency or lifecycle changes.
It validates existence and cycles before writing, includes archived tasks when resolving task hierarchy, and supports independent targets in one invocation.

```text
worklog set-parent ENTITY... (--parent PARENT | --none) [--project PROJECT]
```

#### `set-spec-paths`

Sets the complete collection of project path globs governed by a spec after the caller identifies the behavioral boundary.
It validates the supplied globs, shows the resulting coverage change, and does not infer behavioral ownership from filenames or implementation alone.

```text
worklog set-spec-paths SPEC --paths GLOB... [--project PROJECT]
```

#### `task`

Manages task governance and lifecycle, including its governing specs, dependencies, activation, blocking, resumption, completion, cancellation, and prompt archival when resolved.
It validates `modifies` and `blocked_by`, records blocker checks, applies mechanically checkable close-out gates, and leaves semantic judgment of completion evidence to the caller.

```text
worklog task set-specs TASK (--spec SPEC... | --none) [--project PROJECT]
worklog task set-dependencies TASK (--task TASK... | --none) [--project PROJECT]
worklog task start TASK... [--project PROJECT]
worklog task block TASK... --reason TEXT [--blocked-by TASK...] [--project PROJECT]
worklog task resume TASK... --checked TEXT [--project PROJECT]
worklog task finish TASK... --evidence FILE --specs-reconciled [--project PROJECT]
worklog task cancel TASK... --reason TEXT [--follow-up TASK] [--project PROJECT]
worklog task archive TASK... [--project PROJECT]
```

#### `marker`

Manages structurally scoped `NEEDS APPROVAL` and `UNIMPLEMENTED` markers without losing affected child scopes, and records verified implementation by clearing `UNIMPLEMENTED`.
It may associate an implementation marker with its owning task and requires evidence for implementation updates, but it does not judge that evidence, clear `NEEDS APPROVAL`, or treat invocation as approval.

```text
worklog marker (add|move) ENTITY --marker (needs-approval|unimplemented) --scope SCOPE [--to SCOPE] [--task TASK] [--project PROJECT]
worklog marker implemented SPEC --scope SCOPE --evidence FILE [--project PROJECT]
```

#### `validate`

Performs a read-only integrity check over current entities, archived tasks, and project configuration.
It reports malformed frontmatter, identity collisions, invalid fields and references, hierarchy or dependency cycles, lifecycle inconsistencies, and unresolved review separately from structural errors, without rewriting files.

```text
worklog validate [ENTITY...] [--project PROJECT]
```

### Implementation

- Tools MUST be written in Python.
  - Each tool SHOULD NOT introduce an additional dependency.
- Tools SHOULD expose workflow operations instead of requiring callers to manipulate entity file frontmatter directly.

### Entity IDs

- Every entity ID parameter MUST follow the identity and interoperability rules in s0002.
- Tools SHOULD emit entity IDs in standard form.

### Entity hierarchy

#### UNIMPLEMENTED (t0006)

- Tools MUST validate `parent` availability, references, and cycles according to s0002.
- Parent lookup and validation MUST include archived tasks.
- Hierarchy cycles MUST be validated independently from type-specific relationship cycles such as `blocked_by`.
- Reverse lookup and hierarchy grouping MUST derive children from `parent` rather than duplicated parent metadata.
- A summary view MAY group entities beneath their parent.
- Tools MUST determine task actionability from ordinary task status and `blocked_by`, not from `parent`.

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
