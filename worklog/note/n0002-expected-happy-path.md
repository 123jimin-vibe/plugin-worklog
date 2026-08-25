+++
id = "n0002"
title = "Expected happy path"
+++

# Expected happy path

A happy path is the expected sequence of steps when work proceeds normally.
This note lists the expected happy paths for common workflows.

## Starting a new project

1. Define the project's basic idea.
   A. Initialize Worklog.
      a. Confirm that the project will use Worklog.
      b. Create the entity directories.
   B. Survey relevant dependencies and related work.
      a. Check existing solutions before choosing an approach.
      b. Preserve external material as a reference only when needed repeatedly.
      c. Record reusable non-authoritative findings in a note only when needed.

2. Derive a concrete first deliverable.
   A. Define its completion and verification criteria.
   B. Record anticipated changes when known.

3. Refine the project's identity and boundaries, repeating A and B as needed.
   A. Create the minimum governing spec set.
      a. Allocate IDs and use standard filenames.
      b. Initialize each spec.
      c. Record approved enduring behavior and constraints, and clearly mark
         approved but unbuilt behaviors.
      d. Check related specs for overlap or contradiction.
   B. Create relevant tasks individually or in bulk, then execute them.
      a. Allocate IDs and set `status = "pending"`.
      b. Set `modifies` and any `blocked_by` relationships, and describe the
         work.
      c. Set `status = "active"` before implementation.
      d. Write tests derived from the specs.
      e. Implement and verify the deliverable.
      f. Write the delivered state back to the governing specs.
      g. Set `status = "done"` and archive the task.
      h. Report entities that still require human review.

## Introducing Worklog to an existing project

**NEEDS REVIEW**

1. Establish the current project state.
   A. Confirm that the project will adopt Worklog.
   B. Survey its code, tests, documentation, and existing behavior.
   C. Do not reconstruct project history.

2. Establish Worklog coverage.
   A. Create the minimum governing spec set.
      a. Allocate IDs and initialize each spec.
      b. Record verified current behavior and constraints.
      c. Add `paths` globs for governed files.
      d. Resolve unclear or conflicting intent with the user.
   B. Report new specs that still require human review.

3. Begin governed work.
   A. Create relevant tasks individually or in bulk.
      a. Set `status`, `modifies`, and any `blocked_by` relationships.
      b. Describe the work and follow its applicable happy path.

## Adding or changing behavior

**NEEDS REVIEW**

1. Define the proposed behavior.
   A. Survey current behavior, related work, and governing specs.
   B. Check related specs for overlap or contradiction.

2. Specify the change.
   A. Obtain approval for new behavior.
   B. Extend a governing spec or create the minimum new spec set.
      a. Initialize each changed spec.
      b. Record the approved behavior and constraints.
      c. Clearly mark approved but unbuilt behaviors.

3. Deliver the change, repeating A as needed.
   A. Create relevant tasks individually or in bulk, then execute them.
      a. Allocate IDs, set `status = "pending"`, and describe the work.
      b. Set `modifies` and any `blocked_by` relationships.
      c. Set `status = "active"` before implementation.
      d. Write tests derived from the specs.
      e. Implement and verify the changed behavior.
      f. Write the delivered state back to the governing specs.
      g. Set `status = "done"` and archive the task.

## Fixing a bug

**NEEDS REVIEW**

1. Establish the defect.
   A. Reproduce the failure.
   B. Compare the implementation with the governing specs.

2. Resolve the intended behavior.
   A. If the specs are missing or wrong, obtain approval and update them.
   B. Otherwise, treat the divergence as an implementation defect.

3. Correct the defect.
   A. Create and execute a linked task.
      a. Initialize it with `status = "pending"` and the applicable `modifies`.
      b. Set `status = "active"` before implementation.
      c. Add a regression test that fails before the fix.
      d. Correct the general cause and verify the result.
      e. Write the delivered state back to the governing specs.
      f. Set `status = "done"` and archive the task.

## Refactoring

**NEEDS REVIEW**

1. Define the refactoring boundary.
   A. Identify the governing specs and behavior that must remain unchanged.
   B. Create a task for the refactoring.
      a. Set `status = "pending"` and the applicable `modifies`.
      b. Describe the intended restructuring.

2. Establish a baseline.
   A. Set `status = "active"` before refactoring.
   B. Run the existing verification.

3. Restructure and close the task.
   A. Refactor incrementally.
   B. Verify that observable behavior remains unchanged.
   C. Update spec structure or `paths` when boundaries move.
   D. Write back the specs, set `status = "done"`, and archive the task.

## Performing a chore

**NEEDS REVIEW**

1. Classify the work.
   A. Identify any governing specs.
   B. Use the behavior-change happy path if observable behavior will change.

2. Track the chore.
   A. Create a task.
      a. Set `status = "pending"` and the applicable `modifies`.
      b. Leave `modifies` empty only when no spec governs the work.
      c. Set `status = "active"` before maintenance begins.

3. Complete the chore.
   A. Make and verify the maintenance change.
   B. Check for stale specs or affected behavior.
   C. Write back any affected specs.
   D. Set `status = "done"` and archive the task.

## Applying an urgent fix

**NEEDS REVIEW**

1. Bound the urgent problem.
   A. Create a narrowly scoped task.
      a. Set `status = "pending"` and the applicable `modifies`.
      b. Set `status = "active"` before implementation.

2. Correct and verify the problem.
   A. Make the smallest complete correction.
   B. Run verification covering the urgent failure.

3. Reconcile Worklog.
   A. Write the delivered state back to the governing specs.
   B. Set `status = "done"` and archive the task.
   C. Create pending follow-up tasks for deferred cleanup.

Urgency does not suspend status tracking, verification, or spec write-back.

