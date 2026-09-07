# Worklog tools

Run with Python 3.11 or newer; no additional packages are required.
Paths below are relative to this directory in the installed plugin.

```text
python worklog.py init [PROJECT]
python worklog.py tag (list|add|update|remove) ... [--project PROJECT]
python worklog.py status [ENTITY...] [--path PATH...] [--project PROJECT]
python worklog.py create (spec|task|note) TITLE... [options] [--project PROJECT]
python worklog.py field (set|add|remove|unset) ENTITY... --field FIELD [--value VALUE...] [--project PROJECT]
python worklog.py task (start|block|resume|finish|cancel) TASK... [options] [--project PROJECT]
python worklog.py --help
```

`PROJECT` defaults to the current directory.
Use `init` after the project has chosen to adopt worklog.
It creates missing worklog directories, project policy configuration, and the tag database, preserving existing files.
Its output identifies created and existing paths; initialization does not establish spec coverage.

For other commands, `--project` defaults to the current directory and requires an existing worklog.
Use command or subcommand `--help` for arguments.

`tag` requires a valid tag database.
Names are trimmed and Unicode-case-folded; descriptions preserve CSV punctuation and line breaks.
Renames update metadata on every matching current entity and archived task without changing document bodies, including reference contents and decision rationale.
Unknown entity tags and unused rows are advisory.

`status` reports declared state, effective agent modes, hierarchy, dependencies, markers, and available workflow actions.
ID and project-path selections are combined and expanded through entity relationships; archived context is identified as history.
Source paths are matched against spec globs using Python's case-sensitive `fnmatch` conventions.
Directory selections also include matching entity paths and declared path prefixes.
Status is read-only orientation, not an integrity certificate or proof of completion.

`create` accepts `--parent`, `--tag`, `--paths`, `--modifies`, and `--blocked-by` only for applicable entity types.
IDs follow the highest existing number of that type, including archived tasks.
New tasks are pending; generated content is minimal and marked for approval unless the effective mode is autonomous.
Creating an entity does not approve its contents.

`field` supports the following fields:

| Field | Applicable types | Operations |
| --- | --- | --- |
| `title` | spec, task, note | set |
| `parent` | spec, task, note | set, unset |
| `tags` | spec, task, note | set, add, remove, unset |
| `paths` | spec | set, add, remove, unset |
| `modifies` | task | set, add, remove |
| `blocked_by` | task | set, add, remove, unset |

List `add` keeps existing values and adds missing ones; `remove` removes matching values.
An optional absent field can be unset without changing anything.
Changing a title preserves its filename and identity.
IDs are immutable; use `task` for status changes.
Agent-mode overrides remain deliberate document edits under their approval rules.
Mode reporting describes obligations; the tool cannot determine whether the caller is human or has approval.

Task transitions are:

| Command | Starting status | Result |
| --- | --- | --- |
| `start` | pending | active |
| `block --reason TEXT` | pending, active | blocked; append the supplied reason |
| `resume --checked TEXT` | blocked | active; append the supplied check |
| `finish` | active, done | done and archived |
| `cancel [--reason TEXT]` | pending, active, blocked, cancelled | cancelled and archived |

Start, resume, and finish require resolved dependencies.
A new cancellation requires a non-empty reason; an already-cancelled task can be archived without another reason.
Repeating the matching closing command on an archived task makes no changes.
Other transitions out of terminal states are rejected.
Closure checks governing spec references and approval markers, while the caller remains responsible for semantic verification and spec write-back before invoking it.
No command claims that implementation, approval, or completion has been verified.

Create, field, and task targets are independent and processed in supplied order.
Earlier successful changes are visible to later targets; duplicate entity ID arguments are processed once.
Exit status is zero when all requested operations succeed and nonzero when any fail.
Read each target's result before retrying; a failed target does not undo successful targets.

Each mutation preflights its affected files and stages replacement content before publishing it.
Caught failures roll back that operation, including coordinated tag renames and task closure; incomplete rollback is reported explicitly.
Body text, unrelated frontmatter, and comments are retained; comments inside a replaced array remain adjacent to its field.
Tools do not provide crash recovery, transactional visibility to concurrent readers, or coordination with concurrent writers.
Generated bytecode stays alongside the scripts under normal Python cache settings and is ignored by Git.
