+++
id = "t0006"
title = "Implement the full tool set"
tags = ["implementation", "tooling"]
status = "pending"
modifies = ["s0005"]
+++

# Implement the full tool set

Implement every tool defined by s0005 after its behavior is specified.

Complete when all defined tools are shipped with focused verification of their workflows.

## Inputs from t0009 (NEEDS APPROVAL)

Before s0005 establishes a tool as the primary provider for an n0005 unit, it must guarantee that the unit reaches the caller before the affected choice.
The required result categories are:

- valid IDs, files, frontmatter, hierarchy, fields, and marker scope for create and edit operations;
- precise status, dependency, and relationship validation for task operations;
- self-descriptive generated files and project configuration;
- workflow-local constraints, state-change reporting, permission to proceed, and the next required action;
- safe initialization, batching, and failure behavior; and
- close-out prompts that surface spec reconciliation, marker verification, and archival conditions.

The tool specification may satisfy several inventory units through one operation.
It should not copy general methodology into every result.
