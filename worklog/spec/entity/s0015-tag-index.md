+++
id = "s0015"
title = "Tag Index"
tags = ["entity", "methodology"]
+++

# Tag Index

A reference file listing all tags used across specs with descriptions. Lives at `worklog/tags.csv`.

## Purpose

Tags classify specs for cross-cutting queries (e.g., "all specs that define the methodology"). The tag index provides a single place to discover available tags and their meanings, preventing tag drift and inconsistent usage.

## Format

CSV with header row. Columns: `tag`, `description`. Sorted alphabetically by tag. Reverse lookup (which specs use a tag) is done via grep, consistent with the forward-only relationship model.

## Maintenance

Update `tags.csv` when adding, renaming, or removing tags from spec frontmatter. Prefer reusing an existing tag over creating a new one.

## Anticipated Changes

- Validation that all tags in spec frontmatter appear in the index (via validate.py, s0010).
- Tag descriptions enforced as non-empty.

## Dangers

- Index drifts out of sync with actual spec tags — becomes misleading rather than helpful.
- Too many tags dilute their value. If two tags always co-occur, one is redundant.
