+++
id = "s0018"
title = "The create tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/entity_commands.py"]
+++

# The `create` tool

```text
worklog create (spec|task|note) TITLE... [--parent ID] [--tag TAG...] [--paths GLOB...] [--modifies SPEC...] [--blocked-by TASK...] [--project PROJECT]
```

Creates same-type entities sharing the supplied optional fields.
Shared rules follow s0005; entity fields follow s0002, s0003, s0009, and s0010.

| Option | Available to |
| --- | --- |
| `--parent`, `--tag` | spec, task, note |
| `--paths` | spec |
| `--modifies`, `--blocked-by` | task |

- Titles MUST be non-empty; supplied fields and references MUST satisfy their type, applicability, and cardinality rules.
- Allocate after the highest reserved number of that type, including archived tasks; each successful creation reserves its ID for later targets.
  Existing files MUST NOT be overwritten.
- New tasks are `pending` with `modifies = []` when omitted.
- Generated content MUST contain only minimal valid frontmatter and a title heading, without a body template or invented scope.
  Mark content `NEEDS APPROVAL` unless the effective mode is `autonomous`.
- Report each created ID, path, and effective mode.
  Invocation does not approve generated content.

Allocation needs only the created type's filename inventory.
Load supplied relation targets and required forward relationships, policy for the new entity's mode, and tag advice for non-empty tags.
Unavailable required inventory or invalid shared options prevent dependent creations; invalid titles fail independently.
Unrelated malformed entities MUST NOT prevent safe creation or produce diagnostics.
