+++
id = "t0014"
title = "Implement the init tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0005", "s0008", "s0012", "s0013", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the init tool

Implement `worklog init` according to s0013 and the common tool rules in s0005.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when the command is shipped and its new-worklog, compatible-existing-worklog, idempotent, conflict, tag-database, and no-partial-change workflows are verified.

## Completion evidence (NEEDS APPROVAL)

Delivered the plugin-contained `worklog.py init [PROJECT]` entry point, usage documentation, and shared configuration, CSV, and filesystem support.
The command preflights the required paths and existing metadata, creates only missing structure, preserves existing file bytes, and rolls back its own creations on caught write failures.
It reports created/existing paths and does not imply adequate spec coverage.

The full standard-library unittest suite runs 21 tests on Python 3.12.14: 20 pass and one directory-symlink test is skipped because Windows denies symlink creation.
Coverage includes new and partial worklogs, idempotence, every entity type and archived-task tag seeding, quoted CSV descriptions, normalized duplicates, invalid configuration, structural conflicts, partial file writes, rollback, and isolated plugin execution without bytecode writes.
A regression test covers valid TOML multiline strings containing fence-like lines.
The implementation uses sorted traversal and set/dictionary lookups; it creates no persistent index or recovery state.
Crash recovery and concurrent writers are not verified or supported by this implementation.

Reviewed s0002, s0005, s0008, s0012, s0013, and s0015 against the delivery.
Their existing behavior covers this work; added source mappings and removed only the delivered `init` implementation markers.
The other tools and their implementation markers remain owned by t0006.

## Repository fixture finding (NEEDS APPROVAL)

Initialization of a disposable copy of this repository reports pre-existing reference metadata problems: ten reference files lack `title`, and the copied pitfalls reference lacks opening TOML frontmatter.
These files do not meet s0002's entity metadata requirements.
The initialization preflight rejects them; no reference repair is included in this task.
