+++
id = "s0002"
title = "Common entity rules"
+++

# Common entity rules

Worklog records project state in flat files for use across sessions.

## Relevant entries

- s0003 defines spec entities.
- s0008 defines project-level agent policy.
- s0009 defines task entities.
- s0010 defines note entities.
- s0011 defines reference entities.
- n0001 guides writing.
- n0002 describes the expected happy path.
- n0003 records pitfalls.

## Files

- Non-archived entities are Markdown files under `worklog/{type}/**/{filename}.md`, where `{type}` is `spec`, `task`, `note`, `ref`, or `decision`.
- Files and directories under `worklog/` SHOULD be named in kebab-case.
- Every entity MUST have TOML frontmatter delimited by `+++`.
- For an entity with an ID, the filename MUST start with its ID in standard form.
  - Example: `s0001-project-overview.md`.
  - The non-ID portion MAY change and SHOULD be based on the title.
- An entity with an ID retains its identity when its path or the non-ID portion of its filename changes.

## IDs

- An ID consists of a type prefix and a decimal numeric value.
- The type prefix and numeric value determine identity.
- Within one type, each numeric value MUST identify at most one entity, including archived entities.
  - `s01` and `s0001` refer to the same entity.
  - `s01` and `t01` may both exist because their types differ.
- Standard form: prefix the numeric value with leading zeroes until its digit part has four characters. Values already longer than four digits are unchanged.
  - Examples: `s0001`, `t12345`.
- Conventional form: leading zeroes MAY be omitted while retaining at least two digits.
  - Examples: `s01`, `t123`.
- Numbers SHOULD NOT be changed or reassigned.
- Tools SHOULD accept any non-empty decimal digit part without a length restriction and normalize it by numeric value.
  - `s1`, `s001`, and `s00001` all specify `s0001`.

## Common frontmatter

| Field | Type | Required | Available to | Description |
| --- | --- | --- | --- | --- |
| `id` | string | yes | spec, task, note, decision | Standard-form ID. |
| `title` | string | yes | all types | Human-readable title. |
| `tags` | array of strings | no | all types | Classification and search labels. |
| `agent_mode` | string | no | spec, task, note | Entity-specific override of the project policy defined by s0008. |

## Writing

- Write for a reader with no session context.
- Extend an existing entity rather than create an overlapping one.
- Keep each entity to one subject; split entities that cover distinct subjects.
- Record current state and intent, not how they arose.
- Refer to another Worklog entity by ID rather than its file path; entity paths are not stable.
- Express requirement strength with MUST, SHOULD, or MAY.
- An agent MUST NOT present content awaiting human approval as approved. Discussion is not approval.

## Recommended markers

Use markers to expose state that is not evident from the content itself.

- `NEEDS APPROVAL`: content awaits required human approval and is not yet authoritative.
- `UNIMPLEMENTED`: authorized spec behavior is not implemented; it remains authoritative.
- A marker in a Markdown heading applies to the entire section rooted at that heading.
  - Example: `## UX (UNIMPLEMENTED)` marks the entire `UX` section as unimplemented.
  - A marker-only child section, such as `### UNIMPLEMENTED` under `## UX`, MAY be used to mark only part of the parent section.
- A heading marker MUST be removed when it no longer applies to every part of its section.
  - In the same change, apply the marker to every child section or statement that remains affected.
- A marker MUST be removed when its condition no longer applies.

## Human approval

- Apply the `agent_mode` selected by s0008 before creating or changing a spec, task, or note.
- An agent MUST NOT claim human approval that it did not receive.
- It's encouraged to make small changes that can be reviewed in full.
- At the end of a session, report draft changes still awaiting human approval.

## Deprecated decisions

- A decision is an immutable record of rationale.
- ID prefix: `d`.
- New decisions MUST NOT be created.
