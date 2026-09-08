+++
id = "t0021"
title = "Split tool specs and implement error and disk I/O rules"
status = "done"
modifies = ["s0005", "s0013", "s0016", "s0017", "s0018", "s0019", "s0020", "s0002", "s0003", "s0008", "s0009", "s0010", "s0011", "s0012", "s0015"]
+++

# Split tool specs and implement error and disk I/O rules

1. Split the tool specifications.
2. Amend s0005 with details on error propagation and disk I/O.
3. Apply the resulting specification changes to the implementation.

Scope errors, warnings, and other diagnostics to the current tool action.
Unrelated diagnostics may teach agents to ignore messages, making them worse than useless.

## Proposed approach and completion conditions

Separate command-specific contracts from common tool rules.
Use the existing s0013 as the governing spec for `init` rather than creating overlapping coverage.
Allocate specs for the other tools as needed, keep shared rules in s0005, and update related-spec references and governed `paths`.
Extend `modifies` with the new tool specs and any other governing specs whose behavior the work touches.

Define error propagation in terms of the operation's required inputs and safety conditions:

- Distinguish advisory diagnostics, target-local failures, and failures of shared prerequisites.
- State which errors prevent an operation or an individual batch target, and which permit useful results or independent work to proceed.
- Define partial-result and exit-status semantics for diagnostics relevant to the requested action, including the selected scope of `status`.
- Address task creation being blocked by unrelated reference metadata errors without emitting those errors as unrelated warnings instead.
  Preserve reference validity requirements; report defects when they fall within the requested action's scope or affect its required inputs or safety conditions.

Define disk I/O requirements, including:

- The scope and frequency of discovery, file reads, and file writes needed by each operation; avoid unnecessary full-tree scans and repeated I/O.
- Preservation of unrelated files and untouched content, including what no-change operations may write.
Filesystem-failure handling is not a primary concern for this task; retain existing safeguards without expanding recovery machinery.

Apply approved contracts to every affected tool and shared implementation path.
Update affected tests, command help, and existing tool documentation to match the resulting behavior.
Verify representative CLI workflows and plausible failure cases, including unrelated malformed references, relevant invalid inputs, independent batch outcomes, and unnecessary file reads or writes.
Verify that unrelated defects neither prevent an otherwise safe action nor produce diagnostic noise, while relevant failures remain visible.
Do not repair the unrelated reference files as a substitute for correcting error propagation.

Coordinate overlapping specification work with t0020, which reviews happy paths and tool sufficiency; this task owns the requested tool-spec split, error/I/O specification, and corresponding implementation changes.

Complete when the split specs have clear, non-duplicated responsibilities, s0005 states the shared error and disk I/O contracts, and the affected implementation and verification evidence agree with the approved specifications.
Required unapproved spec content or unimplemented required behavior prevents completion.

## Completion evidence (NEEDS APPROVAL)

- Split `tag`, `status`, `create`, `field`, and `task` into s0016 through s0020; retained s0013 for `init` and s0005 for shared contracts and the command inventory.
- Implemented lazy type-specific filename discovery, cached entity bytes, relevant relationship traversal, policy and tag reads only when needed, and no-write byte-identical operations.
- Unrelated reference defects no longer block task creation or appear in selected status output; explicitly selecting a defective reference still reports its error.
- Database-only tag operations avoid entity and policy reads; completed initialization avoids entity scans.
- Existing entity validity, mode precedence, tag identity, and task lifecycle contracts remain covered by the unchanged s0002, s0003, s0008 through s0012, and s0015.
  The s0015 reference to s0005 intentionally remains an entry through the tool inventory to s0016.
- Updated existing tool documentation and CLI help; retained existing mutation safeguards without adding filesystem-recovery machinery.
- `python -m unittest discover -s tests`: 61 tests run, 60 passed, one directory-symlink test skipped because Windows denied symlink creation.
  Focused regressions cover forbidden unrelated reads, selected-only diagnostics, policy override and table scope, independent targets, relationship repairs, and no-op preservation.
- An isolated 16-command CLI smoke scenario exercised initialization, creation, tag addition, field mutation, selected status, task start/block/resume, archival, and repeated closure.
  The two expected failures were an explicitly selected malformed reference and closure gated by a governing spec's pending approval.
  The unrelated reference remained byte-for-byte unchanged.
- Removed the obsolete graph helper and temporary smoke project.
  Existing malformed reference files were not repaired or altered.
