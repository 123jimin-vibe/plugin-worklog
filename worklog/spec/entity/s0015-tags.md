+++
id = "s0015"
title = "Tags"
+++

# Tags

## Related entities

- s0002 defines common entity fields and storage.
- s0005 defines common tool behavior and the `tag` tool.
- s0013 defines tag database initialization.

## Principles

- Tags classify worklog entities for search and grouping.
- `worklog/tags.csv` is project-owned semantic data, not a derived index or other auxiliary tool state.
- A worklog without a tag database remains compatible.

## Database

- The canonical tag database is `worklog/tags.csv`.
- It MUST be UTF-8 CSV with exactly the columns `tag` and `description`, in that order.
- Each row MUST define one tag.
- CSV quoting MUST preserve commas, double quotes, and line breaks in descriptions.
- A description MAY be empty and has no behavioral effect.
- Row order has no meaning.
  Tools MUST write rows sorted by normalized tag name.

## Identity

- A tag name MUST be a string whose normalized value is non-empty.
- Normalize a tag name by removing surrounding whitespace and applying Unicode case folding.
- Normalized names determine tag identity and comparison.
  - Case variants identify the same tag.
  - Punctuation is not normalized, so `agent-mode` and `agent_mode` identify different tags.
- Tools MUST normalize tag names before storing them.
- Tag names SHOULD use lower-case words separated by `_`.
- Database rows MUST be unique by normalized tag name.
- One entity MUST NOT contain the same normalized tag name more than once.

## Entity references

- An entity's `tags` field contains tag names.
- When the database exists, every entity tag SHOULD match a database row by normalized name.
- Tag resolution includes current entities and archived tasks.
- An entity tag without a matching row is unknown.
- A database row without an entity reference is unused. Unused tags remain valid.

## Changes

- Adding a tag adds one normalized, unique database row.
- Changing a description changes no tag behavior or entity reference.
- Renaming a tag MUST store the normalized new name and update every matching current and archived reference as one operation.
- A tag SHOULD NOT be removed while any entity refers to it.
- A change affecting the database and entity references SHOULD validate the complete change before writing and SHOULD NOT leave a partial result on failure.

## Compatibility

- An absent tag database MUST NOT invalidate an otherwise compatible worklog or its existing tag values.
- Creating a missing database for an existing worklog MUST add one normalized row with an empty description for each distinct entity tag without rewriting entity files.
- An existing valid database MUST be used unchanged.

## Known failure modes

- Database rows and entity tags can drift, leaving unknown references or misleading unused entries.
- Case variants can collide after normalization even when their stored text differs.
- A failed rename can split one logical tag across the database and entity files if writes are not atomic.
