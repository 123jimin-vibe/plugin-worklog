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
It reports canonical entities, effective agent modes, governing specs, hierarchy, task dependencies and actionability, unresolved markers and review needs, and the next mechanically available worklog actions.
Its output reflects declared worklog state for orientation; it is not a project-wide integrity check and does not certify that authority, spec coverage, implementation, verification, or completion is correct.

```text
worklog status [ENTITY...] [--path PATH...] [--project PROJECT]
```

#### `create`

Creates one or more same-type specs, tasks, or notes with allocated standard IDs, minimal valid content, and only fields available to that entity type.
All entities in one invocation receive the same optional fields; new tasks are always `pending`.
The tool validates supplied fields before writing, avoids fixed body templates, reports the effective agent mode, and does not treat invocation as approval for generated content.

```text
worklog create (spec|task|note) TITLE... [--parent ID] [--tag TAG...] [--paths GLOB...] [--modifies SPEC...] [--blocked-by TASK...] [--project PROJECT]
```

#### `field`

Changes supported mutable fields on one or more current specs, tasks, or notes, including `parent`, `paths`, `modifies`, and `blocked_by`.
It validates field applicability, value types, references, cardinality, and hierarchy and dependency cycles before writing; reports the effective agent mode without claiming to know the caller's authorization; and never infers values from hierarchy, filenames, or implementation.
IDs are immutable, task status is changed only by `task`, and `agent_mode` changes remain deliberate approval-governed document edits.

```text
worklog field set ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field add ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field remove ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field unset ENTITY... --field FIELD [--project PROJECT]
```

#### `task`

Manages task lifecycle, including activation, blocking, resumption, completion, cancellation, and archival.
`finish` and `cancel` each apply the terminal status and archive atomically; the corresponding command also closes an already-resolved but unarchived task after the same preflight, so archival is not a separate lifecycle path.
The tool enforces declared transition and dependency rules and mechanically detectable close-out gates, but leaves semantic verification and approval judgments to the caller; command success is not proof of completion, and `--reason` is required when newly cancelling rather than archiving an already-cancelled task.

```text
worklog task start TASK... [--project PROJECT]
worklog task block TASK... --reason TEXT [--project PROJECT]
worklog task resume TASK... --checked TEXT [--project PROJECT]
worklog task finish TASK... [--project PROJECT]
worklog task cancel TASK... [--reason TEXT] [--project PROJECT]
```

### Implementation

- Tools MUST be written in Python.
  - Each tool SHOULD NOT introduce an additional dependency.
- Tools SHOULD expose workflow operations instead of requiring callers to manipulate entity file frontmatter directly.

### Efficiency and implementation scope

For this section, `n` is the relevant input size, most commonly the number of worklog entries an operation must consider.
An individual tool spec MAY define another measure when appropriate.
Quasi-linear means `O(n polylog n)`, and quasi-constant means `O(polylog n)`.

- Every tool MUST run in quasi-linear time or better with respect to `n`.
- An operation SHOULD admit a quasi-constant-time implementation when all necessary optimizations are assumed, apart from work proportional to explicitly supplied target data and required output.
  - This is an optimizability requirement, not a requirement to implement those optimizations now; a linear entity-ID search satisfies it if indexing could make the search quasi-constant.
- Tools SHOULD NOT require auxiliary tool-specific state files, such as a search index.
  - This preference is not a compatibility guarantee for future worklog versions.
- Tools SHOULD be straightforward to implement.
  - Operations whose correctness depends on open-ended interpretation or support for many unrelated formats SHOULD instead be assigned to an auxiliary agent.

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
  - Examples include creating multiple entities and finishing or cancelling multiple tasks.
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
