+++
id = "t0004"
title = "Introduce task hierarchy"
tags = ["methodology", "tasks"]
status = "pending"
modifies = ["s0005", "s0009"]
+++

# Introduce task hierarchy

## Motivation

Long-running efforts need a way to group related session-sized tasks.
Task hierarchy should provide that structure without creating a second dependency or lifecycle system.

## Intended behavior

- A task MAY declare `child_of`, containing the ID of one broader task.
- A task has at most one parent and MAY be both a parent and a child.
- Children are discovered by reverse lookup of `child_of`; parent frontmatter MUST NOT duplicate a children list.
- Existing tasks without `child_of` remain valid without migration.
- `child_of` has structural validation but no workflow semantics.

## Relationship semantics

- `child_of` expresses decomposition only.
- It does not imply dependency, execution order, status propagation, lifecycle coupling, field inheritance, or approval.
- Use `blocked_by` for execution dependencies.
  - A parent that must wait for a child SHOULD declare that child in `blocked_by`.
- Every task independently follows the ordinary rules for scope, status, `modifies`, agent mode, verification, spec reconciliation, completion, and archival.
- Resolving or archiving one task does not resolve, archive, cancel, or otherwise change another task.
- Archiving a task does not invalidate existing hierarchy references.

## Validation and reporting

- `child_of` MUST reference an existing task.
- A task MUST NOT name itself as its parent or form a `child_of` cycle.
- Validate the hierarchy independently from the `blocked_by` dependency graph.
- A summary view MAY collapse child tasks beneath their parent.
- Actionability MUST be determined from ordinary task status and `blocked_by`, not from hierarchy.
- Reverse lookup SHOULD support relationships involving archived tasks.

## Affected documents (NEEDS APPROVAL)

- s0009 defines `child_of` and its lack of workflow semantics.
- s0005 defines hierarchy validation, reverse lookup, grouping, and actionable reporting.
- s0002 and s0012 require no hierarchy-specific changes.
- Full tool implementation remains in t0006.

## Completion criteria

- The governing specs and guidance consistently treat `child_of` as informative decomposition.
- Existing tasks remain valid without migration.
- Hierarchy and dependency validation remain distinct.
- Task handling and actionability remain governed by existing lifecycle rules and `blocked_by`.
