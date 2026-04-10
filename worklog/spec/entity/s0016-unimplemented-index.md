+++
id = "s0016"
title = "Unimplemented Index"
tags = ["entity", "methodology"]
+++

# Unimplemented Index

A reference file listing all outstanding `UNIMPLEMENTED` items across worklog specs. Lives at `worklog/UNIMPLEMENTED.md`.

## Purpose

Specs use inline `UNIMPLEMENTED` markers for approved items without backing implementation (s0011). These markers are scattered across files. The index provides a single place to see all outstanding items without grepping.

## Format

Markdown list grouped by source spec. Each entry references the spec ID and a brief description of the unimplemented item. Sorted by spec ID.

## Maintenance

Update when adding or resolving an `UNIMPLEMENTED` marker in any spec. When an item is implemented or dropped, remove it from the index.

## Anticipated Changes

- Automated generation via script (s0010) that greps for `UNIMPLEMENTED` markers across spec files and produces the index.
- Validation that all `UNIMPLEMENTED` markers in specs have a corresponding entry in the index.

## Dangers

- Index drifts out of sync with actual markers — resolved items linger, new items missing. Without automation, this is the expected failure mode.
- Overhead of manual maintenance may exceed the value for small projects with few specs. Consider deferring the index until the automated script exists.
