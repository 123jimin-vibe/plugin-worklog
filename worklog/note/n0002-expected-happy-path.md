+++
id = "n0002"
title = "Expected happy path"
+++

# Expected happy path

A happy path is the expected sequence of steps when work proceeds normally.
This note lists the expected happy paths for common workflows.

## Developing and continuing a task (NEEDS APPROVAL)

Tasks grow through investigation, implementation, and verification.
The workflows below share this lifecycle.

1. Select an existing task or create one with `status = "pending"`.
   A. State the known outcome, constraints, initial completion conditions, and unresolved questions.
   B. Record known affected specs in `modifies` and task prerequisites in `blocked_by`.
   C. Check current progress and prerequisites when continuing work, then set `status = "active"` before substantive work.

2. Develop the task through execution.
   A. Refine requirements, scope, and verification from implementation results and feedback.
   B. Update governing specs, `paths`, and delivered-state markers as decisions settle and behavior is verified.
   C. Revise task boundaries, relationships, and work order as useful divisions and dependencies emerge.
   D. Keep findings, remaining questions, and next actions clear enough to resume.

3. Verify the completion conditions, including required human acceptance.
   Reconcile affected specs, record any follow-up work, set `status = "done"`, and archive the task.

## Resolving intent and verification (NEEDS APPROVAL)

- Use existing authoritative requirements and resolve new behavior under the effective `agent_mode` before implementing it.
- Choose evidence appropriate to the outcome: contract tests, runtime checks, representative outputs, or human judgment.
  Write changed-contract tests before implementation where they can express the requirement.

## Starting a new project (NEEDS APPROVAL)

1. Define the basic idea, confirm worklog adoption, and initialize the entity directories.

2. Start a task for the first useful outcome.
   Survey dependencies and existing solutions, and develop the outcome and its verification.
   Preserve repeatedly needed external material as references and reusable findings as notes.

3. Develop the minimum governing spec set alongside the work.
   Record enduring behavior, constraints, and known changeability needs; mark authorized but unbuilt behavior.
   Check related specs for overlap or contradiction and identify governed files through `paths`.

## Introducing worklog to an existing project (NEEDS APPROVAL)

1. Confirm adoption and identify the authoritative project record.
   Survey code, tests, documentation, and existing behavior.

2. Establish coverage through a task.
   Create governing specs, resolve unclear intent, add `paths`, and identify remaining coverage and review needs.

3. Begin governed work, extending coverage as additional enduring subjects become known.

## Adding or changing behavior (NEEDS APPROVAL)

1. Start from the requested outcome or an existing undelivered requirement.
   Survey current behavior and related specs enough to begin a task.

2. Investigate and implement in increments, refining requirements and affected specs through the results.
   Extend or create specs where intended behavior changes; use existing specs for behavior already specified.

3. Verify the agreed outcome.
   For specification or design work, the reviewed specification or design is the deliverable.

## Fixing a bug (NEEDS APPROVAL)

1. Start a task around the reported failure.
   Reproduce it and compare observed behavior with governing specs.

2. Diagnose the cause and resolve any missing or incorrect intended behavior.

3. Preserve a failing regression test or repeatable scenario, correct the general cause, and verify the result.

## Investigating or reviewing (NEEDS APPROVAL)

1. Start a task with the question or scope, initial method, required evidence, and stop conditions.

2. Gather evidence and revise hypotheses and next actions as findings develop.
   Retain, discard, or separately govern experimental artifacts.

3. Resolve the findings, including any required review.
   A supported negative or no-change conclusion can complete the task.
   Keep task evidence in the task, reusable guidance in notes, and authoritative behavior in specs.
   Continue into delivery or create follow-up tasks where the outcome calls for them.

## Refactoring (NEEDS APPROVAL)

1. Start a task for the restructuring.
   Identify behavior to preserve and establish a verification baseline.

2. Refactor incrementally and verify unchanged behavior.
   Handle discovered defects or behavioral changes through their applicable workflows.

3. Update spec structure and `paths` where boundaries moved.

## Performing a chore or applying an urgent fix (NEEDS APPROVAL)

1. Assess affected behavior and existing entities; keep urgent work narrowly scoped.

2. Make and verify the change, reassessing task needs if the work grows.

3. Reconcile worklog where needed.
   A. Leave specs untouched when their wording remains accurate and no enduring behavior or constraint needs new or revised coverage.
   B. Leave tasks untouched when the work finishes in the current session with no follow-up or resumable state.
   C. Otherwise, update affected entities and record deferred work.
