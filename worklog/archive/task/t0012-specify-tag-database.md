+++
id = "t0012"
title = "Specify the tag database"
tags = ["entities", "tooling"]
status = "done"
modifies = ["s0002", "s0005", "s0013", "s0015"]
+++

# Specify the tag database

Create the governing spec for the project-owned CSV database that describes tags used by worklog entities.
Update the existing entity and tool specs to use that definition.
Do not implement the database or any tool; t0006 owns tool and artifact implementation.

## Proposed design

Use `worklog/tags.csv` with the exact header `tag,description`.
Encode it as UTF-8 and use ordinary CSV quoting for commas, quotes, and line breaks in descriptions.
Each subsequent row defines one tag.

A tag is identified by its case-insensitive, non-empty name.
Tools remove surrounding whitespace and case-fold names before storing them.
They do not normalize punctuation, so `agent-mode` and `agent_mode` remain distinct.
Lower-case names with words separated by `_` are recommended.
Duplicate database rows and duplicate tags on one entity are invalid after normalization.
`description` may be empty and has no behavioral effect.
Row order has no meaning, and tools sort rows by normalized tag name.

Do not add aliases, numeric IDs, lifecycle states, timestamps, or a format-version column.
Renaming a tag updates the database and every current or archived entity reference atomically.
A tag may be removed only while unused.
An unused registered tag is valid.

When the database exists, every entity tag must match a row after normalization.
The CSV file is project-owned semantic data and not a disposable tool index.

Existing worklogs without `tags.csv` remain compatible.
Initialization creates one normalized row with an empty description for each distinct existing tag without rewriting entities.
An existing valid database is used unchanged.

## Spec edit plan

### New tag spec

- Allocate a new spec and add its ID to this task's `modifies` before drafting it.
- Define the database's purpose, authority, canonical path, two-column CSV schema, and encoding.
- Define normalized tag identity, the recommended naming form, duplicates, descriptions, and row ordering.
- Define how entity tags resolve, including unknown and unused tags and archived-task references.
- Define add, description change, rename, and removal invariants without specifying implementation structure.
- Define compatibility for a missing database and direct use of an existing valid database.
- Include concise failure modes for registry drift, normalization collisions, and partial multi-file changes.

### s0002 — Common entity rules

- Add the new tag spec to `Related entities`.
- Make the common `tags` frontmatter field defer its identity, validity, and database behavior to that spec.
- Keep the CSV schema and lifecycle rules out of s0002 rather than duplicating them.

### s0005 — Common tool rules

- Add the new tag spec to `Related specs`.
- Define a `tag` tool with these interfaces:

  ```text
  worklog tag list [--project PROJECT]
  worklog tag add TAG [--description TEXT] [--project PROJECT]
  worklog tag update TAG [--name NEW_TAG] [--description TEXT] [--project PROJECT]
  worklog tag remove TAG [--project PROJECT]
  ```

- Define only tool-facing behavior not already governed by the tag spec: command inputs, results, preflight diagnostics, and failure atomicity.
- Make `create`, `field`, and `status` use the tag spec without restating its rules.
- Mark the new and extended tool behavior `UNIMPLEMENTED (t0006)`.

### s0013 — The init tool

- Add the new tag spec to `Related specs`.
- Define creation of a header-only database for a new worklog.
- Define database creation from distinct existing entity tags when the database is absent.
- Preserve an existing valid database unchanged and include it in conflict, idempotency, and result behavior.
- Retain the spec's existing `UNIMPLEMENTED` state under t0006.

## Out of scope

- Creating `worklog/tags.csv` in this repository or any initialized project.
- Implementing or testing `init`, `tag`, `create`, `field`, or `status`.
- Removing implementation markers owned by t0006.

Complete when the dedicated tag spec authoritatively defines the proposed design,
s0002, s0005, and s0013 contain the planned references and behavior without duplication,
the resulting specs are mutually consistent,
and all undelivered tool and artifact behavior remains assigned to t0006.

## Completion evidence

- s0015 defines the tag database, identity, entity references, changes, compatibility, and known failure modes.
- s0002 delegates common tag-field behavior to s0015 without repeating its rules.
- s0005 defines the `tag` interface and tag integration for the existing tool proposals.
- s0013 defines database creation and direct reuse during initialization.
- Every undelivered artifact and tool requirement remains marked `UNIMPLEMENTED (t0006)`.
- No tag database, tool implementation, or tool test was added.
