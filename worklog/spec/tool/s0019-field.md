+++
id = "s0019"
title = "The field tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/entity_commands.py"]
+++

# The `field` tool

```text
worklog field set ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field add ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field remove ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field unset ENTITY... --field FIELD [--project PROJECT]
```

Edits current specs, tasks, and notes under s0005 and the field rules in s0002, s0003, and s0009.

| Field | Applicable types | Operations |
| --- | --- | --- |
| `title` | spec, task, note | set |
| `parent` | spec, task, note | set, unset |
| `tags` | spec, task, note | set, add, remove, unset |
| `paths` | spec | set, add, remove, unset |
| `modifies` | task | set, add, remove |
| `blocked_by` | task | set, add, remove, unset |

- The tool MUST validate applicability, types, cardinality, required references, and resulting relationship cycles before writing each target.
- `set` replaces the value; scalars require one value and titles MUST be non-empty.
- List `add` retains existing order and appends missing values; `remove` deletes matches without reordering.
  Supplied values MUST NOT duplicate after normalization.
- `unset` removes optional fields and is a no-op when absent.
- Title changes preserve filename and identity.
  Values MUST NOT be inferred from hierarchy, filenames, or implementation.
- Archived entities are immutable targets; IDs are immutable, lifecycle changes belong to s0020, and mode edits follow s0012.
- Report whether each target changed and its effective mode.

Read only selected entities, needed mode configuration, and required forward relationship closure.
Cycle checks MUST evaluate proposed results; removed or unset relations need no resolution, but retained relationships remain valid.
Non-relationship edits MUST NOT trigger relationship scans; non-tag edits MUST NOT read the tag database or emit tag diagnostics.
