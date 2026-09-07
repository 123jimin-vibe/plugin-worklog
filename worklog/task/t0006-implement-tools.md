+++
id = "t0006"
title = "Implement the full tool set"
tags = ["implementation", "tooling"]
status = "active"
modifies = ["s0005", "s0013"]
+++

# Implement the full tool set

Implement every tool defined by s0005 and its individual tool specs after their behavior is specified.

Complete when all defined tools are shipped and their normal, failure, and applicable batch workflows are verified.

## Readiness review and execution plan (NEEDS APPROVAL)

### Current delivery state

- s0005 defines six tools: `init`, `tag`, `status`, `create`, `field`, and `task`.
  `init` is delivered; the other five tools remain marked `UNIMPLEMENTED`.
  s0013 specifies `init`; s0015 supplies the tag model and mutation rules.
- t0013 covers the shared foundation; t0014 through t0019 cover the individual commands.
  t0013 and t0014 are delivered; t0015 through t0019 remain pending and contain draft scope marked `NEEDS APPROVAL`.
  The approval prerequisite described for the inventory in t0016 through t0019 is stale relative to current s0005; detailed command contracts still need review.
- The plugin contains a shared Python library and the `init` entry point, with runnable behavioral tests.
  Remaining tool implementations can extend this foundation.
- Existing specifications cover entity identity, hierarchy, modes, tags, and task state.
  They do not yet settle every command's selection, mutation, and failure behavior.

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
