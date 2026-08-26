+++
id = "s0002"
title = "Common entity rules"
+++

# Common entity rules

## Related entities

- s0003 defines spec entities.
- s0008 defines project-level agent policy.
- s0009 defines task entities.
- s0010 defines note entities.
- s0011 defines reference entities.
- n0001 guides writing.
- n0002 describes the expected happy path.
- n0003 records pitfalls.

## Principles

- Worklog keeps the project's intent and state in flat files, so humans and agents can continue work across sessions.
- Unless a rule says otherwise, s0002 applies to every entity. An entity-type spec MAY add detail, but MUST NOT conflict with s0002.
- Put rules that apply across entity types in s0002. Put rules for only one type in that type’s spec.
- An inherent property defines what an entity must satisfy to be valid, or gives a yes-or-no requirement.
- A desirable property remains authoritative, but falling short does not make the entity invalid.

## Inherent properties

### Files and storage

- Non-archived entities are Markdown files under `worklog/{type}/**/{filename}.md`, where `{type}` is `spec`, `task`, `note`, `ref`, or `decision`.
- Archived entities are located under `worklog/archive/task/{filename}.md`.
  - Only tasks MAY be archived.
  - Subdirectories are not allowed.
- Every entity MUST have TOML frontmatter delimited by `+++`.
- For an entity with an ID, the filename MUST start with its ID in standard form, followed by a word boundary (`\b`).
  - Example: `s0001-project-overview.md`.
- The non-ID portion of a filename MAY change without changing entity identity.
- An entity with an ID retains its identity when its path changes.

### Identity

- An ID consists of a type prefix and a decimal numeric value.
- The type prefix and numeric value determine identity.
- Within one type, each numeric value MUST identify at most one entity, including archived entities.
  - `s01` and `s0001` refer to the same entity.
  - `s01` and `t01` may both exist because their types differ.
- Standard form prefixes the numeric value with leading zeroes until its digit part has four characters. Values already longer than four digits are unchanged.
  - Examples: `s0001`, `t12345`.
- Conventional form MAY omit leading zeroes while retaining at least two digits.
  - Examples: `s01`, `t123`.

### Common frontmatter

| Field | Type | Required | Available to | Description |
| --- | --- | --- | --- | --- |
| `id` | string | yes | spec, task, note, decision | Standard-form ID. |
| `title` | string | yes | all types | Human-readable title. |
| `tags` | array of strings | no | all types | Classification and search labels. |
| `agent_mode` | string | no | spec, task, note | Entity-specific override of the project policy defined by s0008. |

### Authority and approval

- Apply the `agent_mode` selected by s0008 before creating or changing a spec, task, or note.
- An agent MUST NOT claim human approval that it did not receive.
- An agent MUST NOT present content awaiting human approval as approved. Discussion is not approval.

## Desirable properties

### Organization

- Files and directories under `worklog/` SHOULD be named in kebab-case.
- The non-ID portion of an entity filename SHOULD be based on its title.
- ID numbers SHOULD NOT be changed or reassigned.

### Writing

- Write for a reader with no session context.
- Extend an existing entity rather than create an overlapping one.
- Keep each entity to one subject; split entities that cover distinct subjects.
- Record current state and intent, not how they arose.
- Refer to another Worklog entity by ID rather than its file path; entity paths are not stable.
- Express requirement strength with MUST, SHOULD, or MAY.

### Marker semantics

- `NEEDS APPROVAL` means that content awaits required human approval and is not yet authoritative.
- `UNIMPLEMENTED` means that authorized spec behavior is not implemented; the behavior remains authoritative.
- A marker in a Markdown heading applies to the entire section rooted at that heading.
  - Example: `## UX (UNIMPLEMENTED)` marks the entire `UX` section as unimplemented.
  - A marker-only child section, such as `### UNIMPLEMENTED` under `## UX`, MAY be used to mark only part of the parent section.
- A heading marker MUST be removed when it no longer applies to every part of its section.
  - In the same change, apply the marker to every child section or statement that remains affected.
- A marker MUST be removed when its condition no longer applies.

### Interoperability

- Tools SHOULD accept any non-empty decimal digit part without a length restriction and normalize it by numeric value.
  - `s1`, `s001`, and `s00001` all specify `s0001`.

### Reviewability

- Small changes that can be reviewed in full are encouraged.
- At the end of a session, report draft changes still awaiting human approval.

## Deprecated

### Decisions

- A decision is an immutable record of rationale.
- ID prefix: `d`.
- New decisions MUST NOT be created.
