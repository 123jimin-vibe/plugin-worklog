+++
id = "t0018"
title = "Implement the field tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0010", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the field tool

After its proposed behavior in s0005 is approved, implement `worklog field` for supported mutable entity fields.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when `set`, `add`, `remove`, and `unset` are shipped and their type, cardinality, reference, hierarchy, dependency, tag, protected-field, batch, failure, and result workflows are verified.

## Completion evidence (NEEDS APPROVAL)

Delivered `worklog field (set|add|remove|unset) ENTITY... --field FIELD [--value VALUE...]` through `worklog.py`, `worklog_lib/entity_commands.py`, and `worklog_lib/editing.py`.
The command modifies supported frontmatter fields while preserving comments, formatting, line endings (including CRLF), and body prose.

Enforces field applicability, scalar versus list semantics, entity reference validity, hierarchy and dependency cycle prevention, and protection of immutable fields (`id`, `status`).
Supports independent batch processing where errors on one entity do not prevent modifications to other valid targets.

Behavioral unit tests in `tests/test_tools.py` cover scalar and list field updates, additions, removals, unsetting, frontmatter comment and CRLF preservation, immutable field protection, and cycle rejection.
Reconciled with governing specs s0002, s0003, s0005, s0008, s0009, s0010, s0012, and s0015; updated implementation paths and cleared tool implementation markers.
