+++
id = "t0006"
title = "Implement the full tool set"
tags = ["implementation", "tooling"]
status = "done"
modifies = ["s0002", "s0003", "s0004", "s0005", "s0008", "s0009", "s0010", "s0011", "s0012", "s0013", "s0015"]
+++

# Implement the full tool set

Implement every tool defined by s0005 and its individual tool specs after their behavior is specified.

Complete when all defined tools are shipped and their normal, failure, and applicable batch workflows are verified.

## Readiness review and execution plan (NEEDS APPROVAL)

### Current delivery state

- All six tools defined by s0005 are delivered: `init`, `tag`, `status`, `create`, `field`, and `task`.
  Their implementations are complete and all `UNIMPLEMENTED` tool markers in s0005 have been cleared.
- All seven child tasks (t0013 through t0019) are delivered, verified, and archived into `worklog/archive/task/`:
  t0013 (foundation), t0014 (`init`), t0015 (`tag`), t0016 (`status`), t0017 (`create`), t0018 (`field`), and t0019 (`task`).
- The plugin contains the full Python library under `plugin/skills/worklog/scripts/worklog_lib/` and the entry point `plugin/skills/worklog/scripts/worklog.py`.
  44 unit tests in `tests/` pass with zero failures.
- SKILL.md and scripts README are updated to document invocation and usage for every tool.
### 1. Settle command contracts before affected implementation

Keep common rules in s0005 and entity rules in their existing specs.
Add individual tool specs only where command-specific detail warrants them.
Propose unresolved behavior for review rather than choose it implicitly in code or tests.

| Area | Details to settle | Owner |
| --- | --- | --- |
| Invocation and compatibility | How the shipped Python entry point realizes `worklog`; supported Python baseline; project selection outside `init`; whether compatibility includes old CLI invocations as well as existing data and workflows. | t0013 |
| Reading and editing | Handling of malformed or ambiguous entities, unrelated invalid data, unknown legacy fields, and invalid project configuration; preservation of body text, comments, and unrelated frontmatter during edits. | t0013, extended by mutation tasks |
| Results and failure | Exit status and diagnostic conventions; duplicate target handling; whether a failed batch target prevents other targets from changing; guarantees for validation failures, write failures, and interrupted multi-file operations. | s0005 and each affected child task |
| `init` | Exact required directories, including optional reference and deprecated decision storage; compatibility checks on existing structure and configuration. | t0014 |
| `tag` | No-op and collision behavior; malformed referring entities; interaction of reference-tag rewrites with reference fidelity and legacy decision preservation. | t0015 |
| `status` | How IDs and paths combine; path and glob matching; related-entity expansion and archived-task inclusion; exact actionability and marker reporting rules. | t0016 |
| `create` | Allocation across current and archived entities; title-to-filename behavior and collisions; minimal generated content and approval markers; applicability of each optional field. | t0017 |
| `field` | Complete mutable-field matrix; scalar versus list operations; empty values, missing values, and no-ops; title/filename interaction; malformed tag-database handling. | t0018 |
| `task` | Allowed source states for each command; dependency gates; storage of reason/check text without a fixed body template; mechanically detectable close-out gates; archive collisions and repeated terminal commands. | t0019 |

The tag-reference interaction needs explicit resolution because s0015 requires renaming every matching reference, while s0011 discourages reference changes and s0002 preserves decision substance.
Do not expand tools into semantic approval, implementation verification, or project-wide certification to fill these gaps.

### 2. Establish the smallest usable foundation — t0013

1. Survey reusable Python capabilities and available dependency choices against the selected runtime baseline.
   Evaluate TOML reading and preservation separately; a parser alone does not establish safe editing.
2. Establish a plugin-contained entry point and a runnable test harness.
   Verify invocation without access to this repository's worklog or other development files.
3. Implement shared discovery and reading needed by the first commands: current entity directories, flat task archives, canonical ID resolution, TOML frontmatter, project modes, and tag normalization.
4. Derive reusable indexes and reverse relationships from one operation's discovered data where needed.
   Check hierarchy and dependency cycles independently and avoid repeated full scans per target.
5. Establish error/result handling and the preflight/write boundary required by `init`.
   Extend mutation support when tag and entity editing provide concrete requirements.

Keep internal module boundaries in implementation planning rather than behavioral specs.
Avoid building an unused generic validation framework, persistent index, or generalized transaction system.

### 3. Deliver commands in reviewable increments

Suggested execution order is t0013 → t0014 → t0015 → t0016 → t0017 → t0018 → t0019.
This is a work sequence, not an additional dependency chain: the child tasks currently depend only on t0013.
Update `blocked_by` only if implementation establishes another actual prerequisite.

| Task | Delivery focus | Decisive verification |
| --- | --- | --- |
| t0014: `init` | First complete invocation, project layout, policy comments, and tag seeding. | New, partial, and complete worklogs; idempotence; conflicting paths; invalid tags; unchanged existing files and no partial changes on specified failures. |
| t0015: `tag` | Database reads and mutations, reference discovery, and coordinated rename. | Unicode normalization; CSV quoting; collisions; referenced removal; current and archived references; unchanged files on rejected changes and failures covered by the agreed contract. |
| t0016: `status` | Read-only orientation over canonical entities and the agreed working set. | ID/path selection; hierarchy distinct from dependency actionability; effective modes; scoped markers; tag diagnostics; no writes or claims of certification. |
| t0017: `create` | ID allocation and minimal same-type single/batch creation. | Archived ID reservation; field applicability; pending tasks; tags with and without a database; generated content authority; filename collisions and agreed batch outcomes. |
| t0018: `field` | Preservation-aware edits using the approved field/operation matrix. | Type/cardinality errors; immutable and protected fields; dangling references; separate hierarchy/dependency cycles; tag normalization; preservation and agreed batch outcomes. |
| t0019: `task` | Lifecycle transitions and completion/cancellation with archival. | Transition matrix; unresolved dependencies; block/resume evidence; review gates; already-resolved tasks; archive collisions; failure consistency and per-target batch results. |

For each child, write behavioral tests from authoritative specs before implementation, implement the smallest complete command, and verify its completion conditions.
Activate the child when its work begins.
Record evidence and reconcile every governing spec before resolving and archiving it.

### 4. Verify the integrated delivery

- Exercise representative n0002 workflows through the shipped entry point: initialize, orient, create entities, edit relationships, start/block/resume tasks, and close tasks after caller-performed spec write-back.
- Use n0003 failure scenarios to challenge authority reporting, marker handling, preservation, and completion claims; derive expected outcomes from specs.
- Verify compatible existing worklogs with missing optional configuration/tag data, nested current entities, archived task references, and legacy decisions.
  Resolve the CLI compatibility boundary before asserting coverage beyond these data/workflow cases.
- Exercise the agreed write-failure guarantees with fault injection, checking affected file contents and archive locations rather than exit codes alone.
- Check complexity from traversal and lookup structure, including graph validation, batch operations, and required output size.
  Respect s0005's distinction between current quasi-linear execution and potential quasi-constant optimization.
- Run from a copy containing only the plugin deliverable to detect accidental development-repository dependencies.
- Review s0004's tool-discovery guidance against delivered commands.
  If skill changes are needed, add s0004 to the responsible task's `modifies` and obtain any required scoped edit permission before changing it.

### Completion boundary

t0006 remains active until all six commands are delivered and verified, applicable spec markers reflect that evidence, and plugin users can discover and invoke the tools.
Before implementation, reconcile each child's scope and `modifies` with the reviewed command contract.
Do not treat this proposed sequence or its unresolved design points as additional approved tool behavior.

## Completion evidence (NEEDS APPROVAL)

Delivered the full tool set specified by s0005 through the plugin entry point `worklog.py` and the `worklog_lib` package:

1. `init` (t0014, s0013): directory scaffolding, project configuration, tag database seeding, idempotence, and creation rollback.
2. `tag` (t0015, s0015): listing, additions, description updates, and atomic rename across active and archived entities with two-phase commit and rollback.
3. `status` (t0016, s0005): read-only whole-worklog and filtered orientation over declared entity state, hierarchy, effective agent modes, next actions, and marker diagnostics without certification.
4. `create` (t0017, s0005): minimal spec, task, and note creation with sequential ID allocation across active and archived entities, option validation, and independent batch handling.
5. `field` (t0018, s0005): metadata modification (`set`, `add`, `remove`, `unset`) preserving frontmatter comments, line endings, and body text; protecting immutable fields and enforcing cycle prevention.
6. `task` (t0019, s0005): lifecycle transitions (`start`, `block`, `resume`, `finish`, `cancel`) with dependency gating, spec review preflight, and atomic archival to `archive/task/`.

Verification evidence:
- Comprehensive test suite: 44 unit tests in `tests/` pass on Python 3.11+, covering foundational reading, initialization, and all tool operations including edge cases and CRLF line-ending preservation.
- Happy-path workflow (n0002): exercised end-to-end lifecycle from initialization, entity creation, tagging, field editing, status orientation, to task completion with atomic archival.
- Failure and pitfall validation (n0003): verified that task closure is blocked when governing specs contain unapproved content (`NEEDS APPROVAL`), cycle detection rejects circular relationships, and batch operations maintain per-target independence.
- Isolated packaging verification: verified invocation of the plugin deliverable from an isolated directory containing only plugin files, confirming zero dependencies on development-repository files and clean execution without bytecode leakage.
- Spec reconciliation: updated source mappings in s0002, s0003, s0008, s0009, s0010, s0011, s0012, and s0015; cleared all tool `UNIMPLEMENTED` markers in s0005; and added tool discovery guidance to `SKILL.md`.

All child tasks t0013 through t0019 are completed, verified, and archived.
