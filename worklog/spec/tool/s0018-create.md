+++
id = "s0018"
title = "The create tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/entity_commands.py"]
+++

# The `create` tool

Creates one or more same-type specs, tasks, or notes with allocated standard IDs and minimal valid content.
s0005 governs shared diagnostics, identity discovery, tag inputs, independent batches, and mutation guarantees.
s0002, s0003, s0009, and s0010 define the entity fields; s0012 governs agent modes and approval.

## Usage

```text
worklog create (spec|task|note) TITLE... [--parent ID] [--tag TAG...] [--paths GLOB...] [--modifies SPEC...] [--blocked-by TASK...] [--project PROJECT]
```

All titles in one invocation receive the same supplied optional fields.

| Option | Available to |
| --- | --- |
| `--parent` | spec, task, note |
| `--tag` | spec, task, note |
| `--paths` | spec |
| `--modifies` | task |
| `--blocked-by` | task |

## Creation

- Each title MUST be non-empty.
  Supplied fields MUST have the applicable types and cardinality, and references MUST identify entities of the required types.
- IDs follow the highest reserved numeric value of the created type, including archived tasks.
  Each successful creation reserves its allocated ID for later targets in the invocation.
  Existing files MUST NOT be overwritten.
- New tasks are always `pending` and declare `modifies`, using an empty list when omitted.
- Generated content MUST be minimal valid frontmatter and a title heading, without a fixed body template or invented scope.
  It is marked `NEEDS APPROVAL` unless the effective mode is `autonomous`.
- Results identify each created entity's ID, path, and effective agent mode.
  Invocation and tool success do not approve generated content or establish edit permission.

## Required inputs

ID allocation needs the created type's filename inventory, not those entities' contents or another type's inventory.
Supplied relation targets and any forward relationships needed to validate those inputs are read separately by ID.
Project policy is needed to determine the new entities' effective mode.
Tag database advice is needed only for supplied non-empty tags, as defined by s0005.

An invalid shared option or unavailable required identity inventory prevents the creations that depend on it.
An invalid individual title does not prevent other titles from succeeding.
Unrelated malformed entities, including reference metadata, MUST NOT prevent safe creation or produce diagnostics.
