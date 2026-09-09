---
name: worklog
description: "Spec-driven development methodology. Trigger on: init worklog, managing/executing tasks/specs on a worklog-adopted project."
---

# Worklog

Treat an adopted `worklog/` as durable project state shared across sessions.
Its absence may mean worklog does not apply; initialize only after explicit project adoption, never from skill activation alone.

## Entities

Entities: `worklog/{spec,task,note,ref}/**/*.md`, with `+++` TOML frontmatter and `title`.
Only tasks may be archived, to flat `worklog/archive/task/`.
Decision worklog entries are deprecated and should not be created.
IDs are type-unique including archives; filenames start with standard-form IDs, e.g. `s0001`.
Refer by ID, not path.

- Spec (`s`): authoritative current behavior above code/tests; divergence is an implementation defect. Optional `paths` map governed files.
- Task (`t`): one work unit, normally one session; `status`, governing specs in `modifies`, optional task dependencies in `blocked_by`.
- Note (`n`): reusable guidance or findings, never behavior authority.
- Reference: faithful external material, no ID or mode. Interpret in a citing task, note, or spec; avoid later edits.

Optional `parent` organizes same-type specs/tasks/notes only; it implies no authority, dependency, order, status, or lifecycle.

## Authority

Durable behavior needs a spec; check related specs for contradictions.
Tasks grant neither approval nor edit permission and remain subordinate to specs.

For specs/tasks/notes, resolve `agent_mode`: entity override → type policy in `worklog/project.toml` (itself `read_only`) → default (`propose` for specs; `draft` for tasks/notes).

- `read_only`: agents must not create or edit; should not prepare changes unless a human asks.
- `propose`: get content approval or scoped edit permission before editing; mark unapproved agent content `NEEDS APPROVAL`.
- `draft`: may edit; mark unapproved agent content `NEEDS APPROVAL`.
- `autonomous`: may edit; agent content is authoritative.

Approval covers stated content and direct entailments; edit permission grants no authority and applies only within scope.
Neither implies the other; discussion is not approval.
Never claim approval you did not receive or add or relax an override without prior human approval.

A human instruction to execute a task approves only its then-stated requirements and direct entailments, permitting needed edits only to then-listed `modifies` specs except `read_only`.
It approves no inferred/out-of-scope behavior or implementation state.
The target spec's mode governs; implement only authoritative behavior.

`NEEDS APPROVAL` (or `NEEDS REVIEW`) is unauthoritative; agents must not remove it.
`UNIMPLEMENTED` is authoritative but undelivered.
Updating verified implementation state, including removing `UNIMPLEMENTED`, needs no content approval; the target edit mode still applies.

## Carrying Out Work

Reviewable work SHOULD have a task before substantive work.
A chore or urgent fix MAY omit one if finished this session with no follow-up or resumable state.
State known scope, initial completion conditions, and unresolved questions.
Finalizing `modifies` before activation is RECOMMENDED to expose planned scope.
Keep `status` (`pending`, `active`, `blocked`, `done`, `cancelled`) current; set `active` before starting.
Refine scope, completion conditions, `modifies`, and `blocked_by` as understanding develops; preserve findings and next actions for continuation.

Verify the stated outcome with appropriate evidence and required human acceptance.
Findings or a reviewed spec may be the outcome; stubs, mocks, and placeholders are not completion.
Keep governing specs and verified implementation markers current; reconcile every `modifies` spec or confirm coverage before archiving.
Required `NEEDS APPROVAL` spec content or a required `read_only` spec change blocks completion and archival.
Resolved tasks (`done` or `cancelled`) SHOULD be archived promptly.
Archives are history: use specs for current state and new tasks for further work.
Report remaining approval needs and material verification limits at session end.

## Tools

When authority, scope, work order, completion, or archival is uncertain, consult the bundled `worklog-advisor` before acting.
It returns a proceed, conditional, blocked, or insufficient-information verdict with blocking findings and the smallest safe next action; its verdict is not approval.

Run `python <skill-directory>/scripts/worklog.py ...` with Python 3.11+.
Use command/subcommand `--help` for arguments; `scripts/README.md` for details.

| Command | When to use → result |
| --- | --- |
| `init [PROJECT]` | Initialize after adoption → created/existing paths, no semantic entities or coverage claim. |
| `status` | Orient/resume, optionally by IDs or project paths → declared state, modes, relationships, markers, next actions; no certification. |
| `tag` | Inspect/maintain the tag database → rows, diagnostics, or affected references. |
| `create` | Allocate minimal specs/tasks/notes → IDs, paths, effective modes; tasks start pending. |
| `field` | Edit supported metadata after applying the effective mode → per-target changes and modes; IDs, status, and mode overrides are protected. |
| `task` | Start/block/resume/finish/cancel tasks → per-target state; finish/cancel also archive after mechanical preflight. |

Except `init`, commands accept `--project PROJECT` (default: current directory).
Create, field, and task batches return independent results; inspect successes and failures before retrying.
Before finish/cancel, perform verification, approval review, and spec write-back yourself; tool success establishes neither authority nor completion.
