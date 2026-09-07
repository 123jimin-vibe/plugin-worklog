+++
id = "t0013"
title = "Implement the tool library foundation"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "done"
modifies = ["s0002", "s0005"]
+++

# Implement the tool library foundation

Implement the initial shared Python library used by worklog tools.
Limit this task to common infrastructure needed before individual tool implementations begin.
The tool-specific child tasks may extend or improve the library as concrete needs emerge.

Complete when tool entry points can use the shared library and its foundational normal and failure behavior is verified.

## Completion evidence (NEEDS APPROVAL)

Delivered a plugin-contained Python library for canonical ID normalization, entity reading, and discovery of nested current entities and flat archived tasks.
Readers retain body whitespace and unknown metadata without writing documents; discovery reports parse failures and ambiguous IDs.
Six behavioral tests pass on Python 3.12.14, covering ID aliases and long IDs, legacy decision metadata, references, optional tags, nested discovery, archives, malformed input, and duplicate identity.
The library uses only the standard library and requires Python 3.11 or newer for `tomllib`.
The existing wording of s0002 and s0005 covers this foundation; tool-level hierarchy, mutation, and lifecycle behaviors remain unimplemented.
