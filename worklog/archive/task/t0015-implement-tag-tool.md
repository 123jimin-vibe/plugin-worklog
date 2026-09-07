+++
id = "t0015"
title = "Implement the tag tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0005", "s0008", "s0011", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the tag tool

Implement `worklog tag` according to s0005 and s0015.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when `list`, `add`, `update`, and `remove` are shipped and their normalization, diagnostics, reference handling, atomic rename, failure, and result workflows are verified.

## Completion evidence (NEEDS APPROVAL)

Delivered `worklog tag (list|add|update|remove)` through `worklog.py` and `worklog_lib/tag_command.py`.
The command supports inspecting the tag database, creating new tags with optional descriptions, updating tag descriptions, and atomic renaming across all referencing entities (specs, tasks, notes, decisions, references, and archived tasks) using two-phase write preflight with rollback.
Tag removal is prevented when referencing entities exist.

Tag handling enforces Unicode NFC normalization, duplicate tag rejection, and RFC 4180 CSV formatting with quotation when descriptions contain commas, quotes, or newlines.
Missing tag databases are diagnosed informatively without failing non-mutating commands.

Behavioral unit tests in `tests/test_tools.py` cover database creation, listing, tag additions, description updates, atomic rename propagation across active and archived entities, and reference protection on removal.
Reconciled with governing specs s0002, s0005, s0008, s0011, s0012, and s0015; updated implementation paths and cleared tool implementation markers.
