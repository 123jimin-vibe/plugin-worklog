+++
id = "t0004"
title = "Introduce entity hierarchy"
tags = ["entities", "methodology"]
status = "pending"
modifies = ["s0002", "s0005"]
+++

# Introduce entity hierarchy

## Motivation

Worklogs need a way to group related specs, tasks, and notes independently from file organization.
Entity hierarchy should provide that structure without creating inheritance, dependency, authority, or lifecycle semantics.

## Intended behavior

- A spec, task, or note MAY declare `parent`, containing the ID of one broader entity of the same type.
- An entity has at most one parent and MAY be both a parent and a child.
- Children are discovered by reverse lookup of `parent`; parent frontmatter MUST NOT duplicate a children list.
- Existing entities without `parent` remain valid without migration.
- References continue to use directory hierarchy and do not declare `parent`.
- Deprecated decisions are outside the entity hierarchy model.
- `parent` has structural validation but no other semantics.

## Relationship semantics

- `parent` expresses organization only.
- It does not imply dependency, execution order, status propagation, lifecycle coupling, field inheritance, or approval.
- Each entity independently follows the ordinary rules for its type.
- Tasks use `blocked_by` for execution dependencies.
  - A parent that must wait for a child SHOULD declare that child in `blocked_by`.
- Resolving or archiving a task does not resolve, archive, cancel, or otherwise change related tasks.
- Archiving a task does not invalidate an existing `parent` relationship.

## Validation and reporting

- `parent` MUST reference an existing entity of the same type.
- An entity MUST NOT name itself as its parent or form a `parent` cycle.
- Validate hierarchy independently from type-specific relationships such as the task `blocked_by` graph.
- A summary view MAY group entities beneath their parent.
- Actionability MUST be determined from ordinary task status and `blocked_by`, not from hierarchy.
- Reverse lookup SHOULD support `parent` relationships involving archived tasks.

## Affected documents (NEEDS APPROVAL)

- s0002 defines `parent`, its availability to specs, tasks, and notes, and its lack of non-structural semantics.
- s0005 defines hierarchy validation, reverse lookup, grouping, and task actionability.
- Full tool implementation remains in t0006.

## Completion criteria

- The governing specs consistently treat `parent` as informative organization for specs, tasks, and notes.
- References retain directory hierarchy, and deprecated decisions remain outside the model.
- Existing entities remain valid without migration.
- Hierarchy validation remains distinct from type-specific relationship validation.
- Task handling and actionability remain governed by existing lifecycle rules and `blocked_by`.
