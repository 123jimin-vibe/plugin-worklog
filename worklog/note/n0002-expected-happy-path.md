+++
id = "n0002"
title = "Expected happy path"
+++

# Expected happy path

A happy path is the expected sequence of steps when work proceeds normally.
This note lists the expected happy paths for common workflows.

## Starting a new project

**NEEDS REVIEW**

1. Survey available dependencies and related work.
2. Specify the minimum approved behavior and constraints needed for the first
   deliverable.
3. Divide delivery into session-sized tasks linked to the governing specs.
4. Implement and verify each task through the common lifecycle.
5. Expand the worklog as concrete needs emerge.

## Introducing Worklog to an existing project

**NEEDS REVIEW**

1. Confirm that the project will adopt Worklog.
2. Survey its code, tests, documentation, and existing behavior.
3. Capture verified current behavior in a small set of focused specs.
4. Resolve unclear or conflicting intent with the user.
5. Create tasks for desired changes; do not reconstruct project history.

## Adding or changing behavior

**NEEDS REVIEW**

1. Survey the project and existing specs for overlap.
2. Extend a governing spec or create a focused one.
3. Obtain approval for the behavioral change.
4. Create linked tasks, then implement and verify them.
5. Write delivered behavior back to the specs and archive the tasks.

## Fixing a bug

**NEEDS REVIEW**

1. Reproduce the failure.
2. Compare implementation with the governing spec.
3. If intended behavior is missing or wrong, resolve and approve the spec
   change.
4. Create a task and add a regression test that fails before the fix.
5. Correct the general cause and verify the result.
6. Write back affected specs and archive the task.

## Refactoring

**NEEDS REVIEW**

1. Create a task naming affected specs and behavior that must remain unchanged.
2. Establish a working baseline.
3. Restructure incrementally.
4. Verify that observable behavior remains unchanged.
5. Update spec structure or `paths` when component boundaries move.
6. Archive the task.

## Investigating

**NEEDS REVIEW**

1. Create a task stating the question and what counts as an answer.
2. Record findings as they emerge.
3. Put authoritative findings in reviewed specs, reusable guidance in notes,
   and discovered work in follow-up tasks.
4. Discard or separately govern experimental code.
5. Archive the investigation.

## Performing a chore

**NEEDS REVIEW**

1. Create a task; leave `modifies` empty only when no spec governs the work.
2. Make and verify the maintenance change.
3. Check for stale specs or affected behavior.
4. Handle observable behavior changes through the behavior-change scenario.
5. Archive the task.

## Applying an urgent fix

**NEEDS REVIEW**

1. Create and activate a narrowly scoped task.
2. Fix and verify the urgent problem.
3. Update the governing specs and archive the task.
4. Record deferred cleanup as follow-up tasks.

Urgency does not suspend status tracking, verification, or spec write-back.

## Preserving reusable context

**NEEDS REVIEW**

1. Use a note for guidance that does not define project behavior.
2. Move authoritative guidance into a reviewed spec.
3. Use a reference for external material consulted repeatedly or at risk of
   changing or disappearing.
4. Keep commentary in the citing spec or note, not in the reference.

## Handling blocked work

**NEEDS REVIEW**

1. Set the task to `blocked` immediately and state the cause.
2. Set `blocked_by` when another task must resolve first.
3. Resolve the blocker and check that it no longer prevents progress.
4. Restore `active` before resuming work.
