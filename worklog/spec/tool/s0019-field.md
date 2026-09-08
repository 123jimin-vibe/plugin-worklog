+++
id = "s0019"
title = "The field tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/entity_commands.py"]
+++

# The `field` tool

Changes supported mutable metadata on one or more current specs, tasks, or notes.
s0005 governs shared diagnostics, identity and hierarchy rules, tag inputs, independent batches, and mutation guarantees.
s0002, s0003, and s0009 define the fields; s0012 governs agent modes and approval.

## Usage

```text
worklog field set ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field add ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field remove ENTITY... --field FIELD --value VALUE... [--project PROJECT]
worklog field unset ENTITY... --field FIELD [--project PROJECT]
```

| Field | Applicable types | Operations |
| --- | --- | --- |
| `title` | spec, task, note | set |
| `parent` | spec, task, note | set, unset |
| `tags` | spec, task, note | set, add, remove, unset |
| `paths` | spec | set, add, remove, unset |
| `modifies` | task | set, add, remove |
| `blocked_by` | task | set, add, remove, unset |

## Changes

- The tool MUST validate field applicability, value types, cardinality, required references, and proposed hierarchy or dependency cycles before writing each target.
- `set` replaces the field value.
  Scalar fields require exactly one value; titles MUST be non-empty.
- List `add` retains existing values in order and appends missing supplied values.
  List `remove` removes matching values and retains the other values in order.
  Supplied values MUST NOT contain duplicates after applicable normalization.
- `unset` removes an optional field.
  Unsetting an already absent optional field succeeds without a change.
  Required fields cannot be unset.
- A title change preserves the filename and identity.
  The tool MUST NOT infer field values from hierarchy, filenames, or implementation.
- IDs are immutable, task status changes belong to s0020, and `agent_mode` changes remain deliberate approval-governed document edits.
  Archived entities are not mutable targets.
- Each result reports whether the target changed and its effective agent mode.
  Mode reporting describes obligations without claiming to determine the caller's identity, permission, or approval.

## Required inputs

The action reads selected entities and configuration needed for their modes.
It reads relationship targets and the forward closure needed to validate the proposed relation, not disconnected graphs or reverse relationships.
Cycle checks MUST evaluate the proposed result rather than let replaced or removed edges prevent a valid repair.
Removing a relation value does not require resolving the removed target; unsetting a relation does not require traversing it.
Remaining required references and relationships are still validated.

Editing a non-relationship field MUST NOT trigger relationship scans.
Editing a non-tag field MUST NOT trigger tag database reads or tag diagnostics.
Tag advice and byte-identical no-op writes follow s0005.
An invalid selected entity or proposed field change is a target-local failure; independent targets remain eligible to succeed.
