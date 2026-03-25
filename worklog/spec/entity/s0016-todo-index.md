+++
id = "s0016"
title = "TODO Index"
tags = ["entity", "methodology"]
+++

# TODO Index

A reference file listing all outstanding TODO items across worklog entities. Lives at `worklog/TODO.md`.

## Purpose

Specs and tasks use inline `TODO` markers for unapproved, planned, or incomplete items (s0011, s0012). These markers are scattered across files. The TODO index provides a single place to see all outstanding items without grepping, making it easy to assess what remains unresolved.

## Format

Markdown list grouped by source entity. Each entry references the entity ID and a brief description of the TODO item. Sorted by entity ID within each group.

## Maintenance

Update `TODO.md` when adding or resolving a `TODO` marker in any worklog entity. When a TODO item is resolved (approved, implemented, or dropped), remove it from the index.

## Anticipated Changes

- Automated generation via script (s0010) that greps for `TODO` markers across worklog files and produces the index.
- Validation that all `TODO` markers in entities have a corresponding entry in the index.

## Dangers

- Index drifts out of sync with actual TODO markers — resolved items linger, new items missing. Without automation, this is the expected failure mode.
- Overhead of manual maintenance may exceed the value for small projects with few specs. Consider deferring the index until the automated script exists.
