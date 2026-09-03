+++
id = "s0005"
title = "Common tool rules"
+++

# Common tool rules

Tools shipped with the plugin for managing worklogs.

Individual tool specs define each tool's usage and behavior.

## Related tools

- s0013 defines the `init` tool.

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
