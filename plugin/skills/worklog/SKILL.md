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
- Task (`t`): one unit of work, normally one session, with `status`, governing specs in `modifies`, and optional task dependencies in `blocked_by`.
- Note (`n`): reusable guidance or findings, never behavior authority.
- Reference: faithful external material with no ID or mode; interpretation belongs in a citing task, note, or spec; avoid later edits.

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

Reviewable work SHOULD have a task created before substantive work.
A chore or urgent fix MAY omit a task when it finishes in the current session with no follow-up or resumable state.
State known scope, initial completion conditions, and unresolved questions.
Finalizing `modifies` before activation is RECOMMENDED so other agents can identify the planned scope.
Keep `status` (`pending`, `active`, `blocked`, `done`, `cancelled`) current; set `active` before starting.
Refine scope, completion conditions, `modifies`, and `blocked_by` as understanding develops; keep findings and next actions usable for continuation.

Verify the stated outcome with appropriate evidence and required human acceptance.
Findings or a reviewed specification can be the outcome; stubs, mocks, and placeholders are not completion.

Keep governing specs and verified implementation markers current during work; before archiving, reconcile every `modifies` spec or confirm coverage.
Required `NEEDS APPROVAL` spec content or a required `read_only` spec change prevents completion and archival.
Resolved tasks (`done` or `cancelled`) SHOULD be archived promptly.

Archives are history; use specs for current state and a new task for further work.
Report remaining approval needs and material verification limits at session end.

## Tools

Run `python <skill-directory>/scripts/worklog.py ...` with Python 3.11 or newer.
Use `--help` on a command or subcommand for arguments; see `scripts/README.md` for details.

| Command | Use | Result |
| --- | --- | --- |
| `init [PROJECT]` | Initialize after project adoption. | Created and existing paths; no semantic entities or coverage claim. |
| `status` | Orient or resume, optionally by IDs or project paths. | Declared state, modes, relationships, markers, and next actions; no certification. |
| `tag` | Inspect or maintain the tag database. | Tag rows, diagnostics, or affected references. |
| `create` | Allocate minimal specs, tasks, or notes. | IDs, paths, and effective modes; new tasks are pending. |
| `field` | Edit supported metadata after applying the effective mode. | Per-target changes and modes; IDs, status, and mode overrides are protected. |
| `task` | Start, block, resume, finish, or cancel tasks. | Per-target state; finish/cancel also archive after mechanical preflight. |

Commands other than `init` accept `--project PROJECT`, defaulting to the current directory.
Create, field, and task batches have independent results; inspect successes and failures before retrying.
Before finish/cancel, perform required verification, approval review, and spec write-back yourself.
Tool success does not establish authority or prove completion.
