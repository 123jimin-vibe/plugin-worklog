+++
id = "n0002"
title = "Expected happy path"
+++

# Expected happy path

A happy path is the expected sequence of steps when work proceeds normally.
This note lists the expected happy paths for common workflows.

## Common task lifecycle

Tasks grow through investigation, implementation, and verification.
Use this lifecycle for task work, with the scenario-specific steps below.

1. Select an existing task or create one with `status = "pending"`.
   A. State the known outcome, constraints, initial completion conditions, and unresolved questions.
   B. Record known affected specs in `modifies` and task prerequisites in `blocked_by`.
   C. Check current progress and prerequisites when continuing work, then set `status = "active"` before substantive work.

2. Develop the task through execution.
   A. Refine requirements and scope from investigation, implementation results, and feedback.
   B. Use existing authoritative requirements and resolve new behavior under the effective `agent_mode` before implementing it.
   C. Choose evidence appropriate to the outcome: contract tests, runtime checks, representative outputs, or human judgment.
      Write changed-contract tests before implementation where they can express the requirement.
   D. Update governing specs, `paths`, and delivered-state markers as decisions settle and behavior is verified.
   E. Revise task boundaries, relationships, and work order as useful divisions and dependencies emerge.
   F. Keep findings, remaining questions, and next actions clear enough to resume.

3. Verify the completion conditions, including required human acceptance.
   Reconcile affected specs, record any follow-up work, set `status = "done"`, and archive the task.

## Establishing worklog

### Starting a new project

1. Define the basic idea, confirm worklog adoption, and initialize the entity directories.

2. Start a task for the first useful outcome.
   Survey dependencies and existing solutions, and develop the outcome and its verification.
   Preserve repeatedly needed external material as references and reusable findings as notes.

3. Develop the minimum governing spec set alongside the work.
   Record enduring behavior, constraints, and known changeability needs; mark authorized but unbuilt behavior.
   Check related specs for overlap or contradiction and identify governed files through `paths`.

### Introducing worklog to an existing project

1. Confirm adoption and identify the authoritative project record.
   Survey code, tests, documentation, and existing behavior.

2. Establish coverage through a task.
   Create governing specs, resolve unclear intent, add `paths`, and identify remaining coverage and review needs.

3. Begin governed work, extending coverage as additional enduring subjects become known.

## Scenario-specific work

These steps distinguish the outcomes sought, not separate investigation, implementation, or verification phases.

| Scenario | Distinctive steps |
| --- | --- |
| Adding or changing behavior | Compare the requested outcome or undelivered requirement with current behavior. Extend or create governing specs where intended behavior changes; use existing specs for behavior already specified. For specification or design work, the reviewed specification or design is the deliverable. |
| Fixing a bug | Reproduce the failure and compare it with governing specs. Diagnose the cause and resolve any missing or incorrect intended behavior. Preserve a failing regression test or repeatable scenario, then correct the general cause. |
| Investigating or reviewing | Define the question or scope, method, required evidence, and stop conditions. Gather evidence, revise hypotheses, and resolve the findings. A supported negative or no-change conclusion can complete the task. Retain, discard, or separately govern experimental artifacts. |
| Refactoring | Identify behavior to preserve and establish a verification baseline. Restructure while preserving that behavior, updating spec structure and `paths` where boundaries move. |
| Chore or urgent fix | Assess affected behavior and existing entities; keep urgent work narrowly scoped. Make and verify the change, reassessing task needs if the work grows. |

An investigation can be part of a delivery task or have findings as its own outcome.
Keep task evidence in the task, reusable guidance in notes, and authoritative behavior in specs.

For a chore or urgent fix:
- Leave specs untouched when their wording remains accurate and no enduring behavior or constraint needs new or revised coverage.
- Leave tasks untouched when the work finishes in the current session with no follow-up or resumable state.
- Otherwise, update affected entities and record deferred work.
