+++
id = "t0004"
title = "Introduce task hierarchy"
tags = ["methodology", "tasks"]
status = "pending"
modifies = ["s0005", "s0009"]
+++

# Introduce task hierarchy

## Motivation

Surveyed worklogs contained 37 tasks over 100 lines, ten over 200 lines, and one over 500 lines.
Long-running experiments accumulated repeated runs, amendments, recalibration, and resumable state that did not fit the one-session task model.
Task hierarchy should permit durable coordination without weakening task scope, lifecycle accuracy, spec authority, or write-back requirements.

## Intended model

- Add an optional `child_of` field containing the ID of one task that contains the broader work.
- Parent and child are derived roles, not distinct task types.
- A task MAY be both a parent and a child.
- Do not add an explicit children list to parent frontmatter.
  - Discover children by reverse lookup of `child_of`.
- Existing tasks without `child_of` MUST remain valid.
- Keep a single parent per task so the hierarchy remains a tree.
  - Work related to more than one parent should use ordinary references or dependencies rather than multiple parents.
- `child_of` MUST NOT affect how a task being handled in practice.

## Parent task content

- A typical parent states the overall intended outcome and completion criteria.
- The parent refers to its child tasks and delegates their implementation details to them.
- A parent task MUST NOT substitute for the specs governing durable behavior.
- Every parent and child independently declares every applicable spec in `modifies`.
- An overarching `UNIMPLEMENTED` marker MAY continue to name the parent while children deliver partial pieces.
  - A child should own the marker instead when that child alone owns the marked behavior.

## Session scope

- A task remains one unit of work.
- The one-session expectation applies to a task's own work, excluding work delegated to child tasks.
- A task MAY remain open across sessions while its children are unresolved.
- Own work spanning more than one session SHOULD still be split into multiple tasks.
- A parent whose children perform the implementation should retain only session-sized work such as final integration, verification, and reconciliation.

Both the task principle and the desirable scope rule in s0009 must reflect this interpretation.
Changing only the existing “Work spanning more than one session” rule would leave the task principle contradictory.

## Relationship semantics

- `child_of` expresses decomposition only.
- `child_of` does not imply a dependency and does not inherit `modifies`, `blocked_by`, `status`, `agent_mode`, tags, priority, or approval state.
- Each task remains subject to its own effective agent mode under s0012.
- Keep `blocked_by` as the relationship for execution dependencies.
- A parent SHOULD include a direct child in `blocked_by` when the parent's remaining own work cannot proceed until that child is resolved.
  - A parent whose only remaining work is final integration and verification will normally be blocked by all direct children.
  - Do not treat every child as a blocker when parent work can proceed concurrently.
- Parent status reflects the parent's own work.
  - A parent may be active alongside its children when no unresolved dependency prevents that work.

## Validation and lifecycle

- `child_of` MUST reference an existing task.
- `child_of` MUST NOT reference the declaring task or form a hierarchy cycle.
- Validate the `child_of` hierarchy independently from the `blocked_by` dependency graph.
- An unresolved task MUST NOT be attached to a resolved or archived parent.
- A parent MUST NOT become resolved or archived while a direct child remains unresolved.
- Resolving a child does not resolve its parent.
- Cancelling a parent does not implicitly cancel its children.
  - Resolve, reparent, or detach unfinished children before cancelling their parent.
- Historical reverse lookup must continue to work after children are archived.

## Spec reconciliation

- Every child follows the normal verification, spec write-back, status, and archival lifecycle.
- A completed child reconciles the current delivered state into each spec in its own `modifies`, even while its parent remains open.
- Partial delivery MUST leave applicable `UNIMPLEMENTED` markers accurate.
- Child write-back MUST NOT be deferred wholesale until the parent completes.
- The parent performs final integration, verification, and reconciliation required by its own completion criteria.

## Open-task reporting

- A summary view MAY collapse child tasks beneath their parent.
- A collapsed parent is RECOMMENDED TO report the number and states of hidden children and allow them to be expanded.
- An actionable backlog SHOULD expose runnable leaf tasks rather than hide them behind a blocked parent.
- Tools should derive child lists from `child_of` instead of requiring duplicated parent metadata.

## Affected documents (NEEDS APPROVAL)

- s0009 defines the field, hierarchy semantics, session scope, lifecycle, and parent guidance.
- s0005 defines validation and collapsed-versus-actionable task-list behavior.
- n0002 should describe a multi-session path: decompose work, execute and archive children, re-evaluate parent blockers, finish parent verification and write-back, then archive the parent.
- n0003 should record anticipated pitfalls:
  - resolving a parent with open children;
  - mistaking `child_of` for dependency or inheritance;
  - deferring child reconciliation until parent completion;
  - silently hiding actionable children.
- s0002 needs no new field because `child_of` is task-specific and its ID follows existing identity rules.
- s0012 retains its current effective-mode selection because agent mode does not inherit through task hierarchy.
- Implementing the full tool support belongs to t0006 after the behavior is specified.

## Completion criteria

- The governing specs and guidance define one consistent hierarchy model.
- Existing tasks remain valid without migration.
- Hierarchy and dependency validation remain distinct.
- Parent and child lifecycle, write-back, archival, and reporting behavior are unambiguous.
