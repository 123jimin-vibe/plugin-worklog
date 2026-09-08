+++
id = "s0017"
title = "The status tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/status_command.py"]
+++

# The `status` tool

```text
worklog status [ENTITY...] [--path PATH...] [--project PROJECT]
```

Read-only orientation from declared state, not an integrity check or certification of authority, coverage, implementation, verification, or completion.
Shared rules follow s0005.

## Selection

- Without selectors, start with all current entities.
- Combine ID and path selections.
  Paths select entity files/directories; absolute paths MUST be within the project.
- Source paths select specs through case-sensitive Python `fnmatch` matching against `paths`.
  Directory selections also match entity paths and declared path prefixes.
- Expand through `parent`, `blocked_by`, and `modifies` in both directions.
  Identify reached archived tasks as history.

## Output and scope

Report selected entities' canonical IDs, paths, types, modes, governing specs, hierarchy/children, governing tasks, status, declared/unresolved dependencies, and mechanically available next actions.
Actionability follows s0020; close-out actions MUST retain verification and spec write-back obligations.
Report approval/review/implementation markers in prose, excluding code examples.

Selection MAY inspect broader relationship and spec-path metadata.
It MUST NOT validate unrelated fields or read unselected reference contents merely for ID summaries or filename matching.
Requested entities and their required relationships are validated; unrelated defects MUST NOT appear in diagnostics or affect exit status.
Relevant failures MUST identify affected or incomplete results while retaining independent useful output.

Tag reporting:

- A missing database is informational; a malformed one is an error when the requested result requires it.
- Selected summaries report advisory unknown tags only for their working set, without scanning all tags for unrelated usage diagnostics.
- Worklog-wide summaries use current entities and archived tasks to report advisory unknown tags and unused rows.
  They MUST NOT claim complete usage results when coverage fails.
