# Typical Project Workflows

Brainstorm: what kinds of work actually happen in a software project, and what does this imply for worklog entity design?

## Workflow Catalog

### 1. Greenfield Feature Development

A new capability is designed and built from scratch.

**Sequence:**
1. Requirement surfaces (user request, product decision, technical need).
2. Architecture/design: what components, how they interact, what constraints.
3. Implementation plan: break the design into buildable chunks.
4. Implementation: code, tests, spec updates.
5. Review/QA: verify against design intent.
6. Release/merge.

**Entities touched:** requirement → spec → plan → task(s) → spec updates.
**Git interaction:** feature branch per plan or per task. Commits reference task IDs.

### 2. Bug Fix

Something doesn't work as specified (or as expected when no spec exists).

**Sequence:**
1. Bug report (user, CI, monitoring).
2. Triage: severity, affected component, is it a spec violation or a spec gap?
3. Investigation: reproduce, root-cause.
4. Fix: code change, test regression.
5. Spec update if the bug revealed a spec gap.

**Entities touched:** bug report → task (investigation) → task (fix) → possibly spec update.
**Distinct from feature work:** may not have a plan. Often starts with investigation. May reveal spec deficiencies.

### 3. Investigation / Research

Exploring a question without a predetermined outcome.

**Sequence:**
1. Question or hypothesis (e.g., "why is the lexer slow?", "can we use library X?").
2. Experimentation: benchmarks, prototypes, reading.
3. Findings documented.
4. Decision: leads to plan, leads to nothing, leads to more questions.

**Entities touched:** task (investigation type) → possibly plan → possibly spec.
**Key observation:** output is *knowledge*, not code. Must be preserved across sessions. bfc t0007 is a perfect example — benchmarks, root causes, what was fixed, what was deferred.

### 4. Refactoring / Tech Debt

Restructuring code without changing external behavior.

**Sequence:**
1. Motivation: code smell, coupling, performance, maintainability.
2. Scope definition: what moves where, what invariants must hold.
3. Implementation: incremental restructuring with tests as safety net.
4. Verification: all existing tests pass, no behavioral change.

**Entities touched:** task (chore type) → possibly spec update (if component boundaries change).
**Distinct from feature work:** no new behavior. Spec changes are structural (component reorganization), not behavioral.

### 5. Dependency / Tooling Update

Upgrading libraries, build tools, CI configuration.

**Sequence:**
1. Trigger: security advisory, deprecation, new feature needed.
2. Assessment: breaking changes, migration effort.
3. Migration: update configs, fix breaking changes.
4. Verification: CI green, no regressions.

**Entities touched:** task (chore). Rarely touches specs unless the dependency is architecturally significant.

### 6. Documentation

Writing or updating docs for users, contributors, or operators.

**Sequence:**
1. Trigger: new feature landed, user confusion, onboarding need.
2. Write/update docs.
3. Review for accuracy.

**Entities touched:** task (chore). Orthogonal to specs (specs describe design intent; docs describe usage/operation). See `expr-documentation.md`.

### 7. Release / Deployment

Cutting a version, deploying to production.

**Sequence:**
1. Decide what's included (feature freeze, changelog).
2. Version bump, changelog generation.
3. Build, test, publish.
4. Post-release: monitor, hotfix if needed.

**Entities touched:** mostly operational — outside worklog's scope? Or does worklog track release milestones?

### 8. Hotfix / Emergency Response

Production is broken, immediate fix needed.

**Sequence:**
1. Incident detected.
2. Immediate triage and fix (minimal process).
3. Post-mortem: what went wrong, what was the root cause.
4. Follow-up tasks: proper fix, test coverage, spec update.

**Entities touched:** task (urgent) → post-mortem (decision record?) → follow-up tasks.
**Distinct:** process is compressed. Full ceremony is counterproductive during emergencies. Post-mortem is where the value lives.

---

## Entity Analysis

### What entities emerge from the workflows?

| Entity | Role | Examples from workflows |
|--------|------|----------------------|
| **Spec** | What the design currently IS | Architecture decisions, component contracts, behavioral specifications |
| **Plan** | Ordered work to achieve a goal | Feature implementation plan, migration strategy |
| **Task** | Atomic unit of work | Implementation, investigation, bugfix, chore |
| **Decision Record** | Why a choice was made (immutable) | "We chose X over Y because Z" — survives archival |
| **Bug Report** | Something doesn't match expectation | Deviation from spec, or unexpected behavior where no spec exists |
| **Milestone** | Release/deployment boundary | "v2.0 includes plans P1-P5" |

### Do we need all of these as first-class entities?

**Spec** — Yes. Proven in v1. Living reference, no status, always current.

**Plan** — Probably yes, despite v1's boundary problems. Workflows 1, 3, and 4 all naturally produce multi-task initiatives that need coordination. The fix isn't removing plans — it's clarifying the boundary: plans describe *work to be done*; specs describe *what currently exists*. A plan is consumed (archived) when its tasks complete; a spec persists.

**Task** — Yes. Proven in v1. The atomic work unit.

**Decision Record (ADR)** — Strong case. bfc case study showed design rationale gets buried in archived plans. Post-mortems (workflow 8), investigation conclusions (workflow 3), and "why not X?" decisions all need a permanent home. ADRs are immutable by convention — you don't update an ADR, you supersede it with a new one.

**Bug Report** — Probably NO as a separate entity. A bug is just a task with a specific origin. The task body documents the bug. If the project uses GitHub Issues, bug tracking lives there — duplicating it in worklog adds friction.

**Milestone** — Probably NO as a first-class entity. Tags or a simple metadata field on plans/tasks can group things by release. Full milestone tracking is project management, not development methodology.

### Recommended first-class entities: **spec, plan, task, decision**

---

## Frontmatter Field Analysis

### What fields do entities need?

#### Universal fields (all entities)
- `id` — unique identifier with type prefix
- `title` — human-readable name
- `created` — creation date
- `tags` — categorization

#### Spec
- No `status` (always current, proven in v1)
- `updated` — last modification date
- Consider: `supersedes` — for when a spec replaces another (rare but possible)

#### Plan
- `status`: `draft` → `active` → (archived when done/abandoned)
  - v1 had `approved` — is this useful? In a solo-dev + AI context, "approved" = "human said go ahead". Maybe just `draft`/`active`/`blocked`.
- `targets` — spec IDs this plan creates or modifies
- `blocked_by` — IDs blocking this plan
- Consider: `priority` — but priority is relative and changes constantly. Maybe not worth the maintenance cost.

#### Task
- `status`: `pending` → `active` → `done` (or `blocked`)
- `type`: `implementation` | `investigation` | `bugfix` | `chore`
  - v1 didn't have this, but it emerged as a natural classification in bfc. Investigation tasks (t0007) behave differently from implementation tasks (t0004).
  - Alternatively: infer type from relationships (has `implements` → implementation, has neither → chore). But investigation is hard to infer.
- `implements` — plan IDs
- `modifies` — spec IDs
- `blocked_by` — IDs blocking this task
- Consider: `branch` — git branch name associated with this task. Enables branch↔task traceability.

#### Decision Record
- `status`: `accepted` | `superseded` | `deprecated`
  - Superseded by another decision, not modified in-place.
- `supersedes` — ID of previous decision this replaces
- `context` — what prompted this decision (could be body content instead)
- `relates_to` — spec/plan IDs this decision affects

---

## Relationship and Precedence

### Entity hierarchy

```
decision ──relates_to──▶ spec, plan
plan ──targets──────────▶ spec
task ──implements───────▶ plan
task ──modifies─────────▶ spec
task ──blocked_by───────▶ task, plan
plan ──blocked_by───────▶ task, plan
```

### Precedence (conflict resolution)

When entities conflict, which is authoritative?

1. **Spec vs. source code**: Spec wins. Code diverging from spec is a bug. (Already established in v1.)
2. **Spec vs. test**: Spec wins. Tests must be derived from specs.
3. **Spec vs. plan**: Spec describes *current* state; plan describes *intended future*. No conflict possible — they describe different time horizons.
4. **Decision vs. spec**: Decision explains *why*; spec describes *what*. Complementary. If a decision says "we chose X" but spec describes Y, the spec was updated without a decision record — the fix is adding a new decision, not changing the old one.
5. **Task vs. plan**: Plan is authoritative for scope; task may discover that plan needs adjustment. Tasks should flag plan deviations, not silently diverge.

---

## How Git Should Be Utilized

### Git as the backbone

The worklog assumes git. This has several implications:

#### 1. History and audit trail
- **Spec evolution**: git diff/log on spec files shows exactly what changed and when. No need for `updated_by` fields or change logs within specs.
- **Decision timeline**: git log on decision records shows when decisions were made relative to code changes.
- **Task completion**: git log shows what commits were made while a task was active. If task IDs are in commit messages, `git log --grep=t0004` reconstructs the full implementation.

#### 2. Branching strategy
- **Task branches**: one branch per task is natural. Branch name includes task ID (e.g., `t0004-known-counter-opts`).
- **Plan branches**: for multi-task plans, a feature branch that task branches merge into. But this adds complexity — maybe only for large plans.
- **Spec branches**: specs change on the branch where the modifying task lives. They merge with the task.

#### 3. Commit conventions
- Commit messages SHOULD reference worklog IDs: `t0004: implement multiply-add expansion`.
- This creates bidirectional traceability: task → commits (via `git log --grep`) and commit → task (via message).
- NOT enforced by hooks (too much friction), but encouraged by the skill.

#### 4. Worklog-specific git patterns
- **Archival**: `archive.py` moves files. Git tracks the move. Archive history is recoverable via `git log --follow`.
- **Validation as pre-commit hook**: `validate.py` could run as a pre-commit hook. But v1 showed manual validation is skipped — hooks are the enforcement mechanism.
- **Conflict resolution**: worklog files (especially specs) can conflict on merge. TOML frontmatter conflicts are usually resolvable automatically (different fields changed). Body conflicts require human judgment.

#### 5. What git provides for free (don't duplicate)
- Change history (don't add `updated_by` or changelog fields)
- Authorship (don't track who modified what — `git blame` does this)
- Diff context (don't store "what changed" in frontmatter)
- Branching/merging (don't build a parallel branching concept)

#### 6. What git does NOT provide (worklog must fill)
- **Intent**: why was this change made? → decision records, task descriptions
- **Status**: what's the current state of work? → task/plan status fields
- **Relationships**: how do components relate? → cross-references in frontmatter
- **Design authority**: what SHOULD the code do? → specs
- **Future work**: what's planned but not started? → plans, pending tasks

---

## Mistakes and Work History

### How should mistakes be tracked?

Mistakes are high-value cross-session knowledge. An agent that repeats a mistake the previous session already solved is wasting human attention. Categories:

#### 1. Design mistakes → Decision Records
"We tried approach X but it failed because Y. We chose Z instead."
This is exactly what ADRs capture. The decision record is immutable — it permanently documents the dead end and the reasoning.

**Example from bfc:** p0005 was abandoned with 4 open questions documented. This is a decision record in disguise — "we decided NOT to do this, here's why." If a future agent considers the same idea, the abandoned plan (or a decision record) prevents re-exploration.

#### 2. Implementation mistakes → Task body / git history
"I tried implementing X this way but it broke Y. The fix was Z."
This lives in the task body (investigation findings, dead ends encountered) and in git history (the actual code changes, reverts, fixes).

**Key insight:** the task body should document *what was tried and failed*, not just the final approach. This is the investigation task pattern (bfc t0007).

#### 3. Recurring agent mistakes → Spec / decision record
"Agents keep doing X wrong" — this is a systemic issue. Solutions:
- If it's a design constraint: add it to the relevant spec as an explicit danger/constraint.
- If it's a methodology issue: decision record explaining the anti-pattern and the correct approach.
- If it's project-specific: `CLAUDE.md` or equivalent (but these are [ineffective](./resource/context-file-effectiveness.md) for context injection — better to encode as spec constraints or validation hooks).

#### 4. Mistakes caught by validation → Automated prevention
The best mistake tracking is making the mistake impossible. `validate.py` as a hook, schema enforcement, test-before-implement workflow. This isn't "tracking" — it's prevention.

### How should work history be tracked?

#### What "work history" means
- What was done, in what order, and why
- What was tried and abandoned
- What decisions were made along the way

#### Mechanisms by layer

| Layer | What it captures | Retrieval |
|-------|-----------------|-----------|
| **Git log** | Code changes, timestamps, authorship | `git log`, `git blame`, `git log --grep=tNNNN` |
| **Task body** | Intent, approach, findings, dead ends | Read task file (or archived task) |
| **Plan body** | Scope, strategy, task breakdown | Read plan file |
| **Decision records** | Why X over Y, what was rejected | Read decision file; `find-refs.py` for related decisions |
| **Spec history** | How design evolved | `git log spec/sNNNN-*.md` |
| **Archive** | Completed/abandoned work | `archive/` directory; `git log --follow` for full history |

#### Anti-patterns to avoid
- **Changelog fields in frontmatter**: duplicates git log. Don't.
- **"Session log" entities**: tempting to log every agent session, but creates noise. The task body captures what matters; git captures the rest.
- **Tracking metrics in worklog**: LoC per commit, time per task, etc. These are indicators, not data to store. Compute them from git on demand.

### The gap: post-mortems

Workflows 3 (investigation) and 8 (hotfix/emergency) both produce valuable "lessons learned" that don't fit neatly into tasks or specs. A decision record can capture "we chose X because Y failed," but a richer post-mortem format might be warranted for incidents:

- What happened?
- What was the root cause?
- What was the immediate fix?
- What follow-up work is needed?
- What should we do differently?

This could be a task subtype (`type = "postmortem"`) or a decision record. Leaning toward decision record — the post-mortem's value is the *decision* about what to do differently, not the incident timeline (which lives in git/task history).

---

## Open Questions from This Brainstorm

1. **Decision record format**: ADR-style (numbered, immutable, supersede chain) or lighter-weight? Full ADR ceremony might be overkill for "we tried X, it didn't work."
2. **Plan necessity**: can small projects skip plans entirely and go spec → task? Probably yes — plans are overhead for projects small enough that a single task covers the work.
3. **Task type field**: explicit `type` field vs. inferred from relationships? Explicit is clearer but adds a field that agents might get wrong.
4. **Branch tracking**: should tasks track their git branch? Useful for traceability but adds maintenance burden. Could be inferred from branch naming conventions.
5. **Milestone/release tracking**: out of scope? Or a lightweight tag-based grouping?
6. **Post-mortem as entity type**: separate from decision records, or a subtype?
7. **Emergency workflow**: should the worklog have a "minimal ceremony" mode for hotfixes, or is a single task sufficient?
