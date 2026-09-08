+++
id = "s0005"
title = "Common tool rules"
paths = ["plugin/skills/worklog/scripts/**"]
+++

# Common tool rules

| Command | Spec |
| --- | --- |
| `init` | s0013 |
| `tag` | s0016 |
| `status` | s0017 |
| `create` | s0018 |
| `field` | s0019 |
| `task` | s0020 |

Entity rules follow s0002, modes follow s0012, and tags follow s0015.
Commands other than `init` accept `--project PROJECT`, defaulting to the current directory, and require an existing worklog.

## Implementation and efficiency

- Tools MUST use Python and SHOULD avoid additional dependencies.
- Tools MAY generate bytecode within their shipped scripts directory; it MUST be ignored by version control.
- Tools SHOULD expose workflow operations rather than raw frontmatter manipulation.
- Tools SHOULD be straightforward; operations requiring open-ended interpretation or many unrelated formats SHOULD instead belong to an auxiliary agent.
- Tools SHOULD NOT require auxiliary state files such as an index.
  This preference is not a future compatibility guarantee.

Let `n` be the relevant input size, unless a command spec defines another measure.
Quasi-linear means `O(n polylog n)`; quasi-constant means `O(polylog n)`.

- Every tool MUST run in quasi-linear time or better.
- An operation SHOULD admit a quasi-constant-time implementation with all necessary optimizations, apart from work proportional to explicit target data and required output.
  This concerns optimizability, not the current implementation's runtime.

## Diagnostics and batches

Action scope comprises requested targets, required inputs, and safety checks—not every discovered file.

- Tools MUST validate required inputs and safety conditions before mutation.
  This does not certify unexamined entities.
- Unrelated defects SHOULD neither block safe actions nor appear as diagnostics, and MUST NOT affect exit status.
- Relevant non-blocking conditions are advisories.
  Exit status MUST be zero for successful results, no-ops, and advisories, and nonzero when an action or required result fails.
- Read-only commands SHOULD retain useful partial results and MUST identify affected results or missing coverage.
- Multi-target operations SHOULD accept independent targets in one invocation and report each outcome.
- `create`, `field`, and `task` process targets in supplied order, handling duplicate entity ID arguments once.
  A failed target MUST NOT prevent independent successes or undo earlier ones.
  Shared-prerequisite failures affect only dependent actions.
- Batches MUST distinguish successful, unchanged, failed, and unattempted targets where applicable.

## Disk I/O and preservation

Tools SHOULD limit discovery, reads, and writes to the action's required files rather than eagerly loading worklog entities, configuration, or tags.

Mutations preflight affected files and stage replacements before publication.
Caught failures roll back the operation; incomplete rollback is reported and prevents further mutations in that invocation.
Preserve body text, unrelated frontmatter, and comments, keeping comments from replaced arrays adjacent to their field.
These guarantees exclude crash recovery, transactional visibility, and coordination with concurrent writers.

## IDs, relationships, and tags

- ID parameters MUST follow s0002; tools SHOULD emit standard-form IDs.
- Tools MUST validate hierarchy under s0002 within the action's relationship scope, including archived parents and cycle checks independent of task dependencies.
- Children and hierarchy groups MUST derive from `parent`, not duplicated metadata.
  Task actionability MUST follow status and `blocked_by`, not hierarchy.
- `create` and `field` normalize tag inputs under s0015.
  When non-empty values require database advice, an existing database MUST be valid before mutation.
  Missing databases are informational and unknown names advisory; neither rejects the change or authorizes database creation or repair.
- Commands unrelated to tags SHOULD NOT read the database or emit tag diagnostics.

## Communication

Messages MAY assume basic worklog vocabulary and refer to the skill for background.
They SHOULD explain the action, result, state changes, whether the caller may proceed, and any next step.
They SHOULD include relevant lifecycle conditions, effective modes, approval or close-out obligations, and safe remediation.
Mode reporting establishes neither edit permission nor content approval.
Messages SHOULD NOT repeat general methodology, obvious argument meanings, or unrelated constraints merely to stand alone.

Generated files SHOULD remain usable without the plugin, with concise comments explaining their purpose and non-obvious fields, authority, and handling.
