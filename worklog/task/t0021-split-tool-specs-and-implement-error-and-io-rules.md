+++
id = "t0021"
title = "Split tool specs and implement error and disk I/O rules"
status = "pending"
modifies = ["s0005", "s0013"]
+++

# Split tool specs and implement error and disk I/O rules

1. Split the tool specifications.
2. Amend s0005 with details on error propagation and disk I/O.
3. Apply the resulting specification changes to the implementation.

## Proposed approach and completion conditions (NEEDS APPROVAL)

Separate command-specific contracts from common tool rules.
Use the existing s0013 as the governing spec for `init` rather than creating overlapping coverage.
Allocate specs for the other tools as needed, keep shared rules in s0005, and update related-spec references and governed `paths`.
Extend `modifies` with the new tool specs and any other governing specs whose behavior the work touches.

Define error propagation in terms of the operation's required inputs and safety conditions:

- Distinguish advisory diagnostics, target-local failures, and failures of shared prerequisites.
- State which errors prevent an operation or an individual batch target, and which permit useful results or independent work to proceed.
- Define partial-result and exit-status semantics, including `status` output accompanied by diagnostics.
- Address task creation being blocked by unrelated reference metadata errors without hiding those errors or weakening reference requirements merely to bypass the failure.

Define disk I/O requirements, including:

- The scope and frequency of discovery, file reads, and file writes needed by each operation; avoid unnecessary full-tree scans and repeated I/O.
- Preservation of unrelated files and untouched content, including what no-change operations may write.
- Filesystem failure handling and the promised atomicity, rollback, and partial-change boundaries for single-target, multi-file, and batch operations.

Apply approved contracts to every affected tool and shared implementation path.
Update affected tests, command help, and existing tool documentation to match the resulting behavior.
Verify representative CLI workflows and plausible failure cases, including unrelated malformed references, relevant invalid inputs, independent batch outcomes, and disk I/O failures.
Do not repair the unrelated reference files as a substitute for correcting error propagation.

Coordinate overlapping specification work with t0020, which reviews happy paths and tool sufficiency; this task owns the requested tool-spec split, error/I/O specification, and corresponding implementation changes.

Complete when the split specs have clear, non-duplicated responsibilities, s0005 states the shared error and disk I/O contracts, and the affected implementation and verification evidence agree with the approved specifications.
Required unapproved spec content or unimplemented required behavior prevents completion.
