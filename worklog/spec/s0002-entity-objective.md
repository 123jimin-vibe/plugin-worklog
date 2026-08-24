+++
id = "s0002"
title = "Worklog entities: objective specification"
+++

# Worklog entities

Worklog records project state in flat files for use across sessions.
This spec defines entity structure; s0003 defines judgment rules; n0002 describes the expected happy path.

## Common rules

### ID

References do not have IDs.

- An ID consists of a type prefix and a decimal numeric value.
- The type prefix and numeric value determine identity.
- Within one type, each numeric value MUST identify at most one entity,
  including archived entities.
  - `s01` and `s0001` refer to the same entity.
  - `s01` and `t01` may both exist because their types differ.
- Standard form: prefix the numeric value with leading zeroes until its digit
  part has four characters. Values already longer than four digits are
  unchanged.
  - Examples: `s0001`, `t12345`
- Conventional form: leading zeroes MAY be omitted while retaining at least two
  digits.
  - Examples: `s01`, `t123`
- Numbers SHOULD NOT be changed or reassigned.
- Tools SHOULD accept any non-empty decimal digit part without a length
  restriction and normalize it by numeric value.
  - `s1`, `s001`, and `s00001` all specify `s0001`.

### File

- Non-archived entities are Markdown files under
  `worklog/{type}/**/{filename}.md`, where `{type}` is `spec`, `task`, `note`,
  `ref`, or `decision`.
- Files and directories under `worklog/` SHOULD be named in kebab-case.
- For an entity with an ID, the filename MUST start with its ID in standard
  form.
  - Example: `s0001-project-overview.md`
  - The non-ID portion MAY change and SHOULD be based on the title.
- An entity with an ID retains its identity when its path or the non-ID portion
  of its filename changes.

### Archive

The archive contains entities removed from the current working set but retained
as project history.

- Only tasks MAY be archived.
- Archived tasks are stored as `worklog/archive/task/{filename}.md`;
  subdirectories are not allowed.

### TOML frontmatter

- Every entity MUST have TOML frontmatter delimited by `+++`.
- Reference frontmatter is metadata, not part of the copied source contents.

| Field | Type | Required | Available to | Description |
| --- | --- | --- | --- | --- |
| `id` | string | yes | spec, task, note, decision | Standard-form ID. |
| `title` | string | yes | all types | Human-readable title. |
| `tags` | array of strings | no | all types | Classification and search labels. |

## Spec

Authoritative specification of current project behavior.

- ID prefix: `s`.
- MAY declare `paths`: globs for governed project files.

## Task

One unit of work expected to be completable in one session.

- ID prefix: `t`.
- Declares `status` and the spec IDs it `modifies`.
  - `pending`: work has not started.
  - `active`: work is in progress.
  - `blocked`: a dependency or external cause explicitly prevents work.
  - `done`: work is complete.
  - `cancelled`: work will not be completed.
- A blocked task MUST state what prevents work. It is unblocked only after
  checking that the stated cause no longer prevents work.
- MAY declare `blocked_by`: IDs of tasks that need to be resolved first.
- A task is resolved when its status is `done` or `cancelled`.
- Open tasks live in `worklog/task/`.
- Completed or cancelled tasks SHOULD be moved to `worklog/archive/task/`.
- Done, cancelled, and archived tasks SHOULD remain terminal. Further work
  SHOULD be recorded as a separate task.

## Note

Non-authoritative project guidance.

- ID prefix: `n`.

## Reference

Material copied from an external source.

- ID not assigned.
- SHOULD be arranged hierarchically under `worklog/ref/`.
- Frontmatter SHOULD identify the original `source` via URL.
- A partial extraction SHOULD identify its `selection`.

## Decision

Immutable record of rationale.

- ID prefix: `d`.
- Deprecated: new decisions MUST NOT be created.