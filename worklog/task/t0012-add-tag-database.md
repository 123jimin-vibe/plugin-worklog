+++
id = "t0012"
title = "Add a tag database"
tags = ["entities", "tooling"]
status = "pending"
modifies = ["s0002", "s0005", "s0013"]
+++

# Add a tag database

Add a project-owned database for the tags used by worklog entities.
The database describes durable project metadata rather than auxiliary tool state.
Maintain it as CSV.

## Proposed design (NEEDS APPROVAL)

Use `worklog/tags.csv` with the exact header `tag,description`.
Encode it as UTF-8 and use ordinary CSV quoting for commas, quotes, and line breaks in descriptions.
Each subsequent row defines one tag.

A tag is identified by its normalized, non-empty `tag` value.
Comparison is case-insensitive.
Tools normalize surrounding whitespace and letter case but do not change punctuation.
Lower-case names with words separated by `_` are recommended.
Duplicate tag rows and duplicate values in one entity's `tags` field are invalid after normalization.
`description` may be empty and has no behavioral effect.
Row order has no meaning, and tools sort rows by normalized tag name.

Do not add aliases, numeric IDs, lifecycle states, timestamps, or a format-version column.
Changing a tag name is an explicit rename that stores the normalized new name and updates the database and every current or archived entity reference atomically.
A tag may be removed only while unused.
An unused registered tag is valid.

When the database exists, every entity tag must match a row after normalization.
Tools report unknown tags and do not add new unknown references.
The CSV file is project-owned semantic data and not a disposable tool index.

Existing worklogs without `tags.csv` remain compatible.
Their existing tags retain their values, and ordinary reads do not fail because the database is absent.
Initializing such a worklog creates one normalized row with an empty description for each distinct tag without rewriting entities.
If the CSV is malformed or has an unexpected header, tag-aware mutations fail before changing the CSV or any entity.

## Spec edit plan

### s0002 — Common entity rules

- Add `worklog/tags.csv` to the standard worklog files and distinguish it from entities and tool-specific state.
- Add the two-column CSV schema, encoding, quoting, uniqueness, ordering, and description rules from the proposed design.
- Define case-insensitive tag identity, tool normalization, and the recommended lower-case `_` form.
- Change the `tags` frontmatter description from free classification strings to references to registered tags when the database exists.
- Define duplicate, unknown, unused, rename, and removal behavior across current entities and archived tasks.
- Add the missing-database compatibility rule and require migration to preserve existing tag values.

### s0005 — Common tool rules

- Add a `tag` tool with these interfaces:

  ```text
  worklog tag list [--project PROJECT]
  worklog tag add TAG [--description TEXT] [--project PROJECT]
  worklog tag update TAG [--name NEW_TAG] [--description TEXT] [--project PROJECT]
  worklog tag remove TAG [--project PROJECT]
  ```

- Require `update` to receive at least one changed value and make `--name` normalize the new name and update all current and archived references atomically.
- Require `remove` to reject a referenced tag and identify every referring entity.
- Make `create --tag` and tag changes through `field` normalize inputs and reject unregistered tags when the database exists.
  When it does not exist, retain current behavior by accepting normalized non-empty tag strings without creating the database implicitly.
- Extend `status` to report a missing database, malformed or duplicate rows, unknown entity tags, and unused registered tags without treating unused tags as errors.
- Require tag commands to validate all affected CSV and entity data before writing and to leave every file unchanged on failure.
- Apply the existing batch, communication, and quasi-linear efficiency rules without introducing an auxiliary index.

### s0013 — The init tool

- Add `worklog/tags.csv` to the files created for a new worklog.
- Create a header-only database when no entity tags exist.
- When completing an existing worklog without the database, scan current entities and archived tasks and create one normalized row per distinct tag with an empty description.
- Preserve an existing valid database byte-for-byte.
- Treat an incompatible `tags.csv` path or invalid existing database as a preflight failure and make no partial changes.
- Include the database in idempotency requirements and in the command's created-versus-existing path report.

## Verification

- Verify exact CSV parsing and round trips for empty descriptions and quoted commas, quotes, and line breaks.
- Verify case-insensitive identity, normalization idempotence, normalized duplicate rejection, and distinct `agent-mode` and `agent_mode` tags.
- Verify add, description update, rename, and removal, including references from archived tasks.
- Verify unknown and unused tag reporting and failure atomicity for multi-file renames.
- Verify new initialization, migration from a database-free worklog, repeated initialization, and preservation of an existing database.

Complete when s0002, s0005, and s0013 define the tag database and its compatibility and tool behavior,
the required database and tool support are implemented,
and the representative new, existing, and failure workflows above pass.
