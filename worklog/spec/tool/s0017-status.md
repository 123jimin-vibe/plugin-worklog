+++
id = "s0017"
title = "The status tool"
paths = ["plugin/skills/worklog/scripts/worklog.py", "plugin/skills/worklog/scripts/worklog_lib/status_command.py"]
+++

# The `status` tool

Summarizes declared worklog state so an agent can orient or resume without reading every entity itself.
s0005 governs shared diagnostics, disk I/O, IDs, and hierarchy; s0002, s0009, s0012, and s0015 define entity state, task lifecycle, modes, and tags.

## Usage

```text
worklog status [ENTITY...] [--path PATH...] [--project PROJECT]
```

## Selection

- With no entity or path selectors, the initial selection is every current entity.
- Entity IDs and project-path selections are combined.
  Entity files and their containing directories can be selected by project-relative path.
  Absolute paths MUST be within the project.
- Source paths select governing specs by their declared `paths` globs, using Python's case-sensitive `fnmatch` conventions.
  Directory selections also include matching entity paths and declared path prefixes.
- The selection expands through `parent`, `blocked_by`, and `modifies` relationships in both directions.
  Archived tasks reached through the selection are identified as history, not current-state authority.

## Output

For the selected working set, the tool reports:

- canonical entities, their paths and types, and effective agent modes;
- governing specs, hierarchy and derived children, and tasks governed by a spec;
- task status, declared dependencies, unresolved dependencies, and mechanically available next actions;
- unresolved approval, review, and implementation markers in entity prose, not marker examples in code;
- relevant errors and tag advice within the scope below.

Task actionability follows s0020's transition and dependency rules, not hierarchy.
Available close-out actions MUST retain the caller's verification and spec write-back obligations.
The result is read-only orientation, not a project-wide integrity check or certification of authority, spec coverage, implementation, verification, or completion.

## Required inputs and diagnostics

A selected summary MAY discover relation metadata beyond its selected entities to establish reverse lookups and relationship expansion, and spec path metadata to match path selectors.
This metadata discovery MUST NOT validate unrelated required fields or emit unrelated defects.
Unselected reference contents MUST NOT be read merely to summarize selected IDs or discover entity filenames for path matching.
Full selected records provide their validity, modes, markers, and tag values.

Errors in requested IDs, selected entities, their required relationships, or metadata needed to establish the requested selection are relevant.
A relevant failure MUST identify the affected result or incomplete coverage while retaining independent useful output under s0005.
Unrelated malformed entities or disconnected relationship errors MUST NOT appear as warnings or errors or affect exit status.

Tag reporting is scoped as follows:

- A missing database is informational.
  A malformed database, including duplicate normalized database names, is an error when the requested tag result requires it.
- Selected summaries report unknown tags from their selected working set as advisory information.
  They MUST NOT scan all entity tags merely to diagnose unrelated unknown tags or unused rows.
- An unselected, worklog-wide summary uses current entities and archived tasks to establish tag-usage coverage.
  It reports unknown entity tags and unused database rows as advisory information, not errors.
  It MUST NOT claim complete usage results if a relevant tag-coverage error prevents them.

A worklog-wide summary necessarily has broader discovery and diagnostic scope than a selected summary.
Neither form writes worklog files.
