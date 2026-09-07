+++
id = "t0016"
title = "Implement the status tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0010", "s0011", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the status tool

After its proposed behavior in s0005 is approved, implement `worklog status` without turning it into a validator or certification mechanism.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when the command is shipped and its whole-worklog, selected-entity, path-selected, hierarchy, actionability, agent-mode, marker, tag-database, failure, and result workflows are verified.

## Completion evidence (NEEDS APPROVAL)

Delivered `worklog status [ENTITY...] [--path PATH...]` through `worklog.py` and `worklog_lib/status_command.py`.
The command provides read-only orientation over declared worklog state, entity hierarchy, effective agent modes, next actionable steps, and unapproved/unimplemented markers without acting as a validator or claiming certification.

Supports whole-worklog orientation as well as target-filtered reporting by canonical entity ID, file path, or glob patterns.
Hierarchy traversal derives children relationships dynamically and distinguishes parent relationships from dependency actionability.
Diagnostics report missing, malformed, or duplicate tag database entries and unknown entity tags.

Behavioral unit tests in `tests/test_tools.py` cover full-worklog orientation, ID-filtered and path-filtered status, effective agent modes, workflow marker discovery, dependency actionability, and tag diagnostics.
Reconciled with governing specs s0002, s0003, s0005, s0008, s0009, s0010, s0011, s0012, and s0015; updated implementation paths and cleared tool implementation markers.
