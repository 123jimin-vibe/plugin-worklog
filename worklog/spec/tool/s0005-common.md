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

#### `context`

Builds a compact, read-only working set from entity IDs and project paths so an agent can orient or resume without reading the whole worklog.
It resolves canonical entities, effective agent modes, governing specs, hierarchy, task dependencies and actionability, relevant markers, and the next mechanically available worklog actions.

```text
worklog context [ENTITY...] [--path PATH...] [--project PROJECT]
```

#### `create`

Creates one or more specs, tasks, or notes with allocated standard IDs, minimal valid content, and only fields available to that entity type.
It validates relationships before writing, applies the effective agent mode, avoids fixed body templates, and reports any content that still needs human approval.

```text
worklog create (spec|task|note) (--title TITLE [--body FILE] | --from MANIFEST) [--parent ID] [--tag TAG...] [--agent-mode MODE] [--paths GLOB...] [--modifies SPEC...] [--blocked-by TASK...] [--project PROJECT]
```

#### `capture`

Creates one or more references by faithfully copying material from a URL, file, or standard input into `worklog/ref/` with source and selection metadata.
It keeps interpretation out of the copied contents, validates the destination, and does not overwrite an existing reference.

```text
worklog capture (SOURCE --to REF_PATH --title TITLE [--selection TEXT] | --from MANIFEST) [--project PROJECT]
```

#### `group`

Places specs, tasks, or notes beneath a same-type parent, or returns them to the top level, without implying dependency or lifecycle changes.
It validates existence and cycles before writing, includes archived tasks when resolving task hierarchy, and supports independent targets in one invocation.

```text
worklog group ENTITY... (--under PARENT | --top-level) [--project PROJECT]
```

#### `scope`

Reconciles governance scope after the caller identifies it by updating a spec's governed path globs or a task's complete `modifies` set.
It validates every supplied relationship, shows the resulting coverage change, and does not infer behavioral ownership from filenames or implementation alone.

```text
worklog scope (spec SPEC --paths GLOB... | task TASK --modifies SPEC...) [--project PROJECT]
```

#### `task`

Manages non-terminal task workflow: starting pending work, recording a concrete blocking condition and task dependencies, and recording the caller's blocker check before resuming.
It enforces valid statuses and `blocked_by` relationships while keeping hierarchy independent from actionability.

```text
worklog task start TASK... [--project PROJECT]
worklog task block TASK... --reason TEXT [--blocked-by TASK...] [--project PROJECT]
worklog task resume TASK... --checked TEXT [--project PROJECT]
```

#### `mark`

Adds or moves structurally scoped `NEEDS APPROVAL` and `UNIMPLEMENTED` markers without losing affected child scopes, and records verified implementation by clearing `UNIMPLEMENTED`.
It may associate an implementation marker with its owning task and requires evidence for implementation updates, but it does not judge that evidence, clear `NEEDS APPROVAL`, or treat invocation as approval.

```text
worklog mark (add|move) ENTITY --marker (needs-approval|unimplemented) --scope SCOPE [--to SCOPE] [--task TASK] [--project PROJECT]
worklog mark implemented SPEC --scope SCOPE --evidence FILE [--project PROJECT]
```

#### `close`

Preflights mechanically checkable close-out conditions, closes tasks as done or cancelled, and archives each task that passes.
Completion requires supplied evidence and the caller's spec-reconciliation declaration, rejects detectable unresolved approval or implementation state, and leaves judgment of the evidence to the caller; cancellation preserves the reason and reports unfinished state requiring disposition.

```text
worklog close done TASK... --evidence FILE --specs-reconciled [--project PROJECT]
worklog close cancel TASK... --reason TEXT [--follow-up TASK] [--project PROJECT]
```

#### `check`

Performs a read-only integrity check over current entities, archived tasks, and project configuration.
It reports malformed frontmatter, identity collisions, invalid fields and references, hierarchy or dependency cycles, lifecycle inconsistencies, and unresolved review separately from structural errors, without rewriting files.

```text
worklog check [ENTITY...] [--project PROJECT]
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
