---
name: worklog
description: "Spec-driven development methodology. Trigger on: init worklog, managing/executing tasks/specs on a worklog-adopted project."
---

# Worklog

Root: `worklog/`. Treat an adopted worklog as durable project state shared across sessions.
If absent, the project may not use this methodology; initialize only after explicit project adoption. Skill activation does not confirm adoption.

## Entities

`worklog/{spec,task,note,ref}/**/*.md` with `+++` TOML frontmatter and `title`.
Only tasks get archived to flat `worklog/archive/task/`.

IDs are type-unique including archives. Filenames start with standard form, such as `s0001`. Refer to entities by ID, not path.

- Spec (`s`): authoritative current behavior; optional `paths` map governed files.
- Task (`t`): one-session work with `status`, governing specs in `modifies`, and optional task dependencies in `blocked_by`.
- Note (`n`): reusable guidance, never behavior authority.
- Reference: faithful external material with no ID or mode; interpretation belongs in a citing spec or note; avoid later edits.

For specs/tasks/notes, optional `parent` organizes same-type entities; it implies no authority, dependency, order, status, or lifecycle.

## Authority

Specs define authoritative current behavior above code/tests; divergence is an implementation defect.
Durable behavior needs a spec; check related specs for contradictions.
Tasks are subordinate and grant no approval or edit permission.

For specs/tasks/notes, effective `agent_mode` is:

1. optional frontmatter entity override,
2. optional policy as stated in `worklog/project.toml` (the file itself is `read_only`),
3. default (spec `propose`; task/note `draft`).

- `read_only`: read-only for agents; should not prepare changes to it unless explicitly asked by a human.
- `propose`: before editing, get content approval or scoped permission; mark unapproved agent content `NEEDS APPROVAL`.
- `draft`: may edit; mark unapproved agent content `NEEDS APPROVAL`.
- `autonomous`: may edit; agent content is authoritative.

Approval covers stated content and direct entailments; permission allows only its scope and grants no authority.
They are independent; discussion is not approval. Never claim approval or add or relax an override without prior human approval.

An explicit human instruction to execute a task approves only its then-stated requirements and direct entailments and permits needed edits only to then-listed `modifies` specs, excluding `read_only` specs.
It approves no inferred or out-of-scope behavior or implementation state; the target spec's mode governs, and only authoritative behavior may be implemented.

`NEEDS APPROVAL` (or `NEEDS REVIEW`) is unauthoritative; an agent must not remove it.
`UNIMPLEMENTED` is authoritative but undelivered; verified implementation-state updates need no content approval, but the target edit mode applies.

## Carrying Out Work

Reviewable work SHOULD have a one-session task created before substantive work.
Keep its `status` (values: `pending`, `active`, `blocked`, `done`, `cancelled`) current; set `active` before starting.
State scope and completion conditions; keep every touched governing spec in `modifies` as scope changes.

After work, verify those conditions; stubs, mocks, and placeholders are not completion.

Before archiving, fold delivered state into every `modifies` spec or confirm coverage, then update implementation markers from verified evidence.
Required `NEEDS APPROVAL` spec content or a required `read_only` spec change prevents completion and archival.
Resolved tasks (`done` or `cancelled`) SHOULD be archived promptly.

Archives are history; use specs for current state and a new task for further work.
Report remaining approval needs and material verification limits at session end.
