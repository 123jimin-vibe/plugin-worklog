+++
id = "t0017"
title = "Implement the create tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0010", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the create tool

After its proposed behavior in s0005 is approved, implement `worklog create` for specs, tasks, and notes.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when single and batch creation, ID allocation, type-specific fields, pending task state, tag handling, effective-mode reporting, validation failure, and per-target result workflows are verified.

## Completion evidence (NEEDS APPROVAL)

Delivered `worklog create (spec|task|note) TITLE... [options]` through `worklog.py` and `worklog_lib/entity_commands.py`.
The command allocates sequential canonical IDs across active and archived entities, formats safe filenames from titles, and writes minimal entity files with standard TOML frontmatter.
New tasks initialize in `pending` status.

Supports entity hierarchy via `--parent`, tag associations via `--tag`, and type-specific fields (`--paths` for specs, `--modifies` and `--blocked-by` for tasks).
Validates referenced entities, detects hierarchy cycles, and reports effective agent modes.
Supports independent batch creation where target failures do not prevent other valid targets from succeeding.

Behavioral unit tests in `tests/test_tools.py` cover single entity creation, batch creation, sequential ID allocation, field validation, hierarchy cycle detection, and independent batch failure reporting.
Reconciled with governing specs s0002, s0003, s0005, s0008, s0009, s0010, s0012, and s0015; updated implementation paths and cleared tool implementation markers.
