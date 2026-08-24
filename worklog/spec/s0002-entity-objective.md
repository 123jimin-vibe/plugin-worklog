+++
id = "s0002"
title = "Worklog entities: objective specification"
+++

# Worklog entities

## Common rules

### ID

Note: References don't have IDs.

- Standard form: type prefix + at least 4 decimal digits, padded with leading zeroes when necessary.
  - Examples: `s0001`, `t12345`
- Conventional form: MAY omit leading zeroes, down to two digits.
  - Examples: `s01`, `t123`
- Number MUST be unique among entities of that type, including archived ones.
  - Example: `s01` and `s0001` always refer to the same entity.
  - Example: `s01` and `t01` may be present together (different types).
- Numbers SHOULD NOT be changed or reassigned.
- Tools SHOULD accept any non-empty decimal digit part without a length restriction.
  - Example: `s1`, `s001`, and `s00001` are all valid ways of specifying `s0001`.

### File

- Entities are stored as Markdown files `worklog/{type}/**/{filename}.md`.
- Any file or directory SHOULD be named in kebab-case.
- For an entity with an ID, the filename MUST start with its ID in standard form.
  - Example: `s0001-project-overview`
  - Non-ID parts MAY change, RECOMMENDED to be based on title.
- Files may freely move around in `worklog/{type}`.

### TOML frontmatter

- Entities with IDs SHOULD have TOML frontmatter delimited by `+++`.

Fields used by multiple types:

| Field | Description | Types |
| --- | --- | --- |
| `id` | Standard-form ID. | spec, task, note, decision |
| `title` | Human-readable title. | spec, task, note, decision |
| `tags` | Labels for classification and search. | spec, task, note, decision |

## Spec

Authoritative specification of current project behavior.

- ID prefix: `s`.
- MAY declare `paths`: globs for governed project files.

## Task

One unit of work, completable in one session.

- ID prefix: `t`.
- Declares `status` and the spec IDs it `modifies`.
  - Status: `pending`, `active`, `blocked`, `done`, or `cancelled`.
- MAY declare `blocked_by`: IDs of tasks that need to be resolved first.
- Open tasks live in `worklog/task/`.
- Completed or cancelled tasks SHOULD BE moved to `worklog/archive/task/`.

## Note

Non-authoritative project guidance.

- ID prefix: `n`.

## Reference

Material copied from an external source.
 
- ID not assigned.
- RECOMMENDED to be arranged hierarchically under `worklog/ref/`.
- MUST preserve the source's contents.
  - Format conversion and partial extraction are allowed.
  - Rephrasing and added clarification are NOT allowed.

## Decision

Immutable record of rationale.

- ID prefix: `d`.
- Deprecated: new decisions MUST NOT be created.