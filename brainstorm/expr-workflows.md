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

**Spec** — Yes. Proven in v1. Living reference, always current.

**Plan** — **Problematic. See "The Plan/Spec Duplication Problem" below.** The content of a plan IS a proto-spec. In practice, plan content migrates to spec once implemented, creating structural duplication that agents amplify.

**Task** — Yes. Proven in v1. The atomic work unit.

**Decision Record (ADR)** — Strong case. bfc case study showed design rationale gets buried in archived plans. Post-mortems (workflow 8), investigation conclusions (workflow 3), and "why not X?" decisions all need a permanent home. ADRs are immutable by convention — you don't update an ADR, you supersede it with a new one.

**Bug Report** — Probably NO as a separate entity. A bug is just a task with a specific origin. The task body documents the bug. If the project uses GitHub Issues, bug tracking lives there — duplicating it in worklog adds friction.

**Milestone** — Probably NO as a first-class entity. Tags or a simple metadata field on plans/tasks can group things by release. Full milestone tracking is project management, not development methodology.

### Recommended first-class entities: **spec, task, decision** (plan absorbed into spec)

---

## The Plan/Spec Duplication Problem

### The diagnosis

The real problem with plans isn't unclear boundaries — it's that **a plan's core content IS the spec, written before the code exists.** During implementation, agents duplicate this content from plan → spec.

Evidence from bfc:

**p0002 (plan) vs s0010 (spec):** Both describe the same optimizer passes — same code examples, same structure, same level of detail. The plan was written first. As tasks implemented passes, content was copied into the spec. The plan became a stale duplicate.

**p0009 (plan):** Contains TypeScript interfaces, a 5-phase implementation breakdown, a file impact table. This is a complete design specification wearing a "plan" label. Once implemented, all of it would be copy-pasted into a spec file (or the plan just sits there, abandoned, with the same content living in the spec).

**The fundamental issue:** "what the design will be" and "what the design currently is" are the SAME document at different points in time. Splitting them into separate entities forces duplication at the moment of implementation.

### Alternative: Spec with progression

Instead of spec + plan as separate entities, use **a single spec entity with progression tracking**:

```markdown
+++
id = "s0010"
title = "Optimization passes"
created = 2026-03-16
tags = ["optimizer", "bsm"]
+++

## Overview

Optimizations fall into two categories: [...]

## Trivial Optimizations

### Clear Loop ✅

[full description]

### Multiply-Add Loop ✅

[full description]

### Dead Loop at Start ✅

[full description]

## Optimizer Passes

### Clear Loop ✅

[full description]

### Set + Add Fusion

- [ ] Implement in `optimize/set-add-fusion.ts`
- [ ] Test: adjacent Set+Add fused
- [ ] Test: adjacent Set+Set fused

[full description — this is both the "plan" and the "spec"]

### Constant Folding

- [ ] Implement CellState tracker
- [ ] Dead loop elimination via known-zero
- [ ] Set-to-add conversion when value known

[full description]
```

#### How this works

1. **Spec is written first** — describes the intended design, including parts not yet implemented.
2. **Unimplemented sections have checklists** — these ARE the plan. No separate plan entity needed.
3. **Tasks reference spec sections** — "implement s0010 § Set+Add Fusion" rather than "implement p0002 step 3."
4. **As tasks complete, checklists get checked off** — the spec progressively becomes "current state" without any content migration.
5. **Git diff shows the progression** — `git log s0010-optimization.md` shows the spec evolving from design → implemented. No separate plan-to-spec copy step.

#### What this eliminates

- **Content duplication**: the design lives in ONE place at all times.
- **Plan-to-spec migration**: there's nothing to migrate. The spec IS the plan.
- **Stale plans**: can't have a stale plan if plans don't exist separately.
- **The "archive plan" ceremony**: no plan to archive. Tasks archive; specs persist.
- **The agent copy-paste failure mode**: agents can't duplicate content between plan/spec because there's only one file.

#### What this changes about task semantics

Tasks no longer `implement` a plan. Instead:

- `modifies` — spec IDs this task updates (same as v1)
- Tasks describe *what work to do* in their body; the *design* lives in the spec.
- A task body says "implement the Set+Add Fusion pass described in s0010" — it doesn't repeat the design.

#### Concerns and tradeoffs

**Incomplete specs feel wrong?** A spec that describes things that don't exist yet blurs the "spec = current truth" principle. But this is already the reality — p0002 described passes that didn't exist yet, and s0010 was supposed to describe only what existed. The boundary was fictional.

Counter-argument: a spec with unchecked items is MORE honest than a separate plan. The checklist explicitly marks what's real and what's aspirational. A "clean" spec with a hidden plan gives a false sense of completeness.

**Large specs become unwieldy?** If a spec grows to describe 20 planned features, it gets long. But:
- This is a signal that the spec should be split into sub-specs (which is healthy architecture anyway).
- A plan covering 20 features would be equally unwieldy.
- Spec sections can link to child specs: `s0010` → `s0010-a` (trivial opts), `s0010-b` (optimizer passes).

**Multi-task coordination?** Plans coordinated multiple tasks. Without plans, how do you express "tasks T1, T2, T3 should be done in order to complete the Optimization feature"?
- The spec's checklist IS the coordination mechanism. Unchecked items = remaining work. Task dependencies expressed via `blocked_by`.
- For truly large initiatives spanning multiple specs: a "meta-spec" or "epic" that cross-references the component specs. But this is rare — bfc had 7 plans over months, and most targeted a single spec.

**Where does "how to implement" go?** Plans often contained implementation strategy (file impact tables, phasing, etc.) that doesn't belong in a spec. Options:
- Task body: if it's task-specific implementation detail.
- Spec appendix / collapsible section: if it's design rationale that future readers need.
- Decision record: if it's "we chose approach X over Y because Z."
- **Just don't write it**: file impact tables (p0009) are over-specification. The agent can figure out which files to change. Implementation phasing can go in task descriptions.

### Revised entity model

| Entity | Role | Status? | Archive? |
|--------|------|---------|----------|
| **Spec** | Living design reference. Includes planned (unchecked) and implemented (checked) sections. | No explicit status. Progression visible via checklists. | Never archived. Updated in-place. |
| **Task** | Atomic unit of work. | `pending` → `active` → `done` (or `blocked`) | Yes, when done. |
| **Decision** | Immutable record of why a choice was made. | `accepted` / `superseded` | Never archived. Permanent record. |

### Revised relationship graph

```
decision ──relates_to──▶ spec
task ──modifies─────────▶ spec
task ──blocked_by───────▶ task
```

Simpler. No plan tier. No `implements` field. No `targets` field.

---

## Frontmatter Field Analysis

### What fields do entities need?

#### Universal fields (all entities)
- `id` — unique identifier with type prefix
- `title` — human-readable name
- `created` — creation date
- `tags` — categorization

#### Spec
- No `status` (progression visible via checklists in body)
- `updated` — last modification date
- `sources` — source paths this spec governs (e.g., `["src/bsm/optimize/"]`). Enables source→spec discoverability via grep.
- Consider: `supersedes` — for when a spec replaces another (rare but possible)

#### Task
- `status`: `pending` → `active` → `done` (or `blocked`)
- `type`: `implementation` | `investigation` | `bugfix` | `chore`
  - v1 didn't have this, but it emerged as a natural classification in bfc. Investigation tasks (t0007) behave differently from implementation tasks (t0004).
  - Alternatively: infer type from relationships (has `modifies` → implementation, has neither → chore). But investigation is hard to infer.
- `modifies` — spec IDs this task updates
- `blocked_by` — IDs blocking this task
- Consider: `branch` — git branch name associated with this task. Enables branch↔task traceability.

#### Decision Record
- `status`: `accepted` | `superseded` | `deprecated`
  - Superseded by another decision, not modified in-place.
- `supersedes` — ID of previous decision this replaces
- `relates_to` — spec IDs this decision affects

---

## Relationship and Precedence

Two constraints shape how cross-references work:

1. **Change locality** — a single logical change should touch as few files as possible. Every cross-reference is a potential edit cascade: if A references B and B changes, does A need updating? Minimize this.
2. **Discoverability without training** — an agent with zero worklog knowledge, upon viewing or editing any one file, should be able to tell which other files it needs to consult or co-edit. Cross-references must be self-explanatory from the frontmatter alone.

### Reference direction and its consequences

Cross-references can be **forward** (referrer → referent) or **reverse** (referent → referrer). The choice directly affects locality and discoverability:

| Direction | Locality | Discoverability | Example |
|-----------|----------|-----------------|---------|
| Forward only (task → spec) | Good: changing the spec doesn't require updating tasks | One-way: task readers know which spec to consult, but spec readers don't know which tasks exist | `modifies = ["s0010"]` in task |
| Bidirectional (task ↔ spec) | Bad: adding/removing a task requires editing the spec too | Full: both sides know about each other | spec lists its tasks AND task lists its spec |
| Forward + computed reverse | Good: same as forward-only for edits | Full: reverse lookup via script/search | `modifies = ["s0010"]` + `find-refs.py s0010` |

**v1 chose forward + computed reverse.** This is correct. Bidirectional references double the edit surface and create consistency bugs (spec says tasks A,B,C; task D says it modifies the spec but isn't listed).

### The discoverability problem in practice

Forward + computed reverse works for agents that know the worklog system. But the constraint says agents *without* worklog knowledge should also be able to navigate. Three navigation scenarios:

**Agent views a task file** → `modifies = ["s0010"]` is self-explanatory. Any agent seeing this will read `s0010`. Solved by forward reference.

**Agent views a spec file** → no outgoing references to tasks. But does it need them? The spec IS the design authority. An agent reading a spec is learning design, not looking for tasks. If it needs to know "who's working on this," `grep -r s0010 worklog/task/` is trivial and requires no special knowledge.

**Agent edits source code** → this is the hard case. How does the agent know a spec exists for the code it's touching? Options:
- Source markers (`@worklog s0010`): failed in bfc — too high-friction to maintain.
- Spec body lists relevant source paths: e.g., `sources = ["src/bsm/optimize/"]` in frontmatter. Requires maintenance but greppable from source side (`grep -r "src/bsm/optimize" worklog/spec/`).
- Directory convention: all specs for code in `src/foo/` are in `worklog/spec/foo/`. Implicit, fragile, doesn't work for cross-cutting specs.
- **Agent reads a worklog summary on session start**: the skill can inject a brief index. This is the most practical — it's a one-time token cost per session, not per file.

Best approach is probably: **spec frontmatter lists source paths** (cheap, greppable) + **session onboarding summary** (comprehensive, one-time cost). Source markers are out.

### Entity hierarchy (revised — no plan tier)

```
decision ──relates_to──▶ spec         (forward: decision knows which spec it's about)
task ──modifies─────────▶ spec         (forward: task knows which specs it touches)
task ──blocked_by───────▶ task         (forward: blocked task knows its blocker)
spec ──sources──────────▶ source paths (forward: spec knows which code implements it)
```

Reverse lookups (which tasks modify a spec? which decisions relate to a spec?) computed by script or grep — never stored.

### Change locality analysis

| Change | Files edited |
|--------|-------------|
| New task | 1 file (the task). No spec or decision edits needed. |
| Complete task | 1–2 files (task status → done; spec checklist items → checked). |
| New spec | 1 file (the spec). No task or decision edits needed. |
| Update spec design | 1 file (the spec). Tasks referencing it via `modifies` don't need editing — the ID hasn't changed. |
| New decision | 1 file (the decision). Optionally 1 more if it supersedes a prior decision. |
| Unblock a task | 1 file (remove ID from `blocked_by`). The blocker task doesn't need editing. |

Worst case is 2 files for a task completion (task + spec). This is inherent — the task's work changes both the code and the spec. No cross-reference overhead.

### Discoverability summary

| Agent is viewing... | How it finds related files |
|--------------------|--------------------------|
| Task | `modifies` field → read those specs |
| Spec | `sources` field → know which code it governs. Reverse: `grep -r <spec-id> worklog/task/` for tasks. |
| Decision | `relates_to` field → read those specs |
| Source code | `grep -r <path> worklog/spec/` to find governing spec. Or check session onboarding summary. |

No field requires worklog-specific knowledge to interpret. An agent seeing `modifies = ["s0010"]` will naturally look for a file containing `s0010` in its name.

### Precedence (conflict resolution)

1. **Spec vs. source code**: Spec wins. Code diverging from spec is a bug.
2. **Spec vs. test**: Spec wins. Tests derived from specs.
3. **Spec (checked ✅) vs. spec (unchecked)**: Checked = current reality. Unchecked = intended design to build next.
4. **Decision vs. spec**: Complementary. Decision = *why*; spec = *what*. Conflict means a spec change lacked a decision record.
5. **Task vs. spec**: Spec is authoritative for design. If a task discovers the design is wrong, update the spec (with user approval for significant changes).

---

## How Git Should Be Utilized

### Git as the backbone

The worklog assumes git. This has several implications:

#### 1. History and audit trail
- **Spec evolution**: git diff/log on spec files shows exactly what changed and when. No need for `updated_by` fields or change logs within specs.
- **Decision timeline**: git log on decision records shows when decisions were made relative to code changes.
- **Task completion**: git log shows what commits were made while a task was active. If task IDs are in commit messages, `git log --grep=t0004` reconstructs the full implementation.

#### 2. Branching strategy
- **Task branches**: one branch per task. Branch name includes task ID (e.g., `t0004-known-counter-opts`).
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
- **Status**: what's the current state of work? → task status fields, spec checklists
- **Relationships**: how do components relate? → cross-references in frontmatter
- **Design authority**: what SHOULD the code do? → specs
- **Future work**: what's planned but not started? → unchecked spec items, pending tasks

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
