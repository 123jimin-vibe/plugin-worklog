---
name: worklog
description: "Spec-driven development methodology via flat-file worklog. Trigger on: create task, plan work, track progress, initialize worklog, manage specs, check drift, what should I work on, resume work."
---

<skill id=worklog>

# Worklog

Specs define what the system is. Tasks change it. Decisions record why.

Root: `worklog/`. If absent, create `worklog/{spec,task,decision,script}/` and `worklog/archive/task/`.

## Entities

IDs: 4-digit per class (`s0001`, `t0001`, `d0001`). Scan existing files + archive when assigning. Filename: `{id}-kebab-name.md`. TOML frontmatter delimited by `+++`.

### Spec

Living design reference. Describes observable behavior, constraints, anticipated changes, dangers.

```toml
+++
id = "s0001"
title = "User Authentication"
tags = ["auth"]
paths = ["src/auth/**", "src/middleware/session.ts"]
+++
```

`paths` — glob patterns for source files this spec governs (used for drift detection). Omit for cross-cutting or conceptual specs. **TODO:** drift detection for specs without `paths` (AI inference or derived from task/commit history).

No status field — specs are always current. No dates — git tracks history. Body uses TODO markers for unfinished items; tasks mark them done.

**Not implementation details.** Describe *what the system does and why*, not *how the code is structured*. `paths` values must be glob patterns (`src/auth/**`), not individual files (`src/auth/login.ts`). See also Forbidden.

### Task

Atomic unit of work. Keep small — completable in one session.

```toml
+++
id = "t0001"
title = "Add session expiry"
status = "pending"
tags = ["auth"]
modifies = ["s0001"]
blocked_by = ["t0003"]
+++
```

Statuses: `pending` → `active` → `done` | `blocked`. Move to `worklog/archive/task/` when done. If a task delivers stubs rather than complete implementations, the governing spec must retain TODO markers for the real implementation — stubs must never be presented as complete.

**TODO:** task type field (`implementation`, `investigation`, `bugfix`, `chore`, `hotfix`) — explicit field vs. inferred from relationships/body.

### Decision

Immutable record of *why* a choice was made.

```toml
+++
id = "d0001"
title = "No recursion in macros"
status = "accepted"
relates_to = ["s0007"]
supersedes = []
+++
```

Body: context → options considered → decision → consequences. Never edit after acceptance — supersede with a new decision. Never archived.

## Relationships

```
task ──modifies──────▶ spec       (which specs this task changes)
task ──blocked_by────▶ task       (ordering dependency)
decision ──relates_to──▶ spec     (which spec this decision concerns)
decision ──supersedes──▶ decision (replaces a prior decision)
spec.paths ───────────▶ source    (which files this spec governs)
```

All forward-only. Reverse lookups via grep — never stored.

## Precedence

1. **Spec over source code.** Code diverging from spec = bug in the code.
2. **Spec over tests.** Tests derive from the spec.
3. **Spec suspected wrong → ask user.** Never silently override a spec.

## Rules

- **Tests before implementation.** Tests derive from spec, not code. **TODO:** should tests be written before task creation (pre-task gate) or as the first step within a task? The former enforces spec→test→code more strictly; the latter is more practical when test shape isn't clear upfront.
- **Test isolation.** When a separate agent writes tests, it receives the **spec** as its sole input — not function names, signatures, internal structure, or behavioral enumerations derived from reading the code. The parent agent must not compensate for spec gaps by front-loading implementation knowledge into the prompt. The test agent must not read source files under the spec's `paths`. If the spec is insufficient to write tests from, that is a spec deficiency — surface it to the user instead of reading the implementation.
- **Survey before building.** Check in-repo code and dependencies before implementing anything. Reimplementing existing functionality is forbidden.
- **Approval means explicit confirmation.** Discussion, questions, and brainstorming do not constitute approval. To modify a spec's observable behavior, the user must explicitly confirm the proposed change. When in doubt, ask.
- **Surface ambiguity.** When scope is unclear (N items, concurrency, security level), ask the user — don't assume degenerate or maximal case.
- **Escalate when stuck.** Surface difficulty to the user. No spiraling into rewrites, no bailing silently, no effort-vs-value judgment without user input.
- **Record decisions.** Non-trivial choices get a decision record. For small projects, inline in the task body is acceptable.
- **No antipatterns.** Injection, unbounded allocations, N+1 queries, bare catch, insecure defaults are never acceptable — satisfying the task does not override defensive concerns.
- **Session resume.** Re-orient from worklog state (specs, task statuses, decisions), not prior session context. The worklog is your memory.

## Forbidden

- Implementation without a covering spec.
- Implementation before tests.
- Modifying a spec's observable behavior without user approval.
- Tests that verify implementation structure instead of spec behavior.
- Behavioral changes disguised as refactoring.
- Regression test written after the fix (must fail before fix to prove it captures the bug).
- Distorting code to route around a bug instead of fixing or reporting it.
- Fixing only the observed failure without evaluating whether it's a general problem.
- Implementation details in specs: API signatures, function names, field names, file/directory layouts, version numbers, or concrete file paths in prose. These drift immediately and create false authority. (`paths` frontmatter uses globs for drift detection — that is the only place file references belong.)
- Test agent reading source files or receiving implementation details (function names, signatures, internal structure) from the parent agent. Tests must be derivable from the spec alone.

**TODO:** enforcement mechanism. Rules above are instructions only — no hooks or gates enforce them yet. v1 lesson: validation that requires deliberate invocation gets skipped.

## Workflows

| Workflow | Flow | Key constraint |
|----------|------|----------------|
| **Greenfield** | spec → task(s) → decision(s) | Tests before implementation |
| **Bug fix** | task → spec (if gap revealed) | Regression test must fail before fix |
| **Refactor** | task → spec (if boundaries change) | No behavioral change; existing tests as safety net |
| **Investigation** | task → decision / spec / nothing | Output is knowledge, not code; findings in task body |
| **Chore** | task | Rarely touches specs |
| **Hotfix** | task → decision | Compressed process; post-mortem mandatory |

Ceremony scales with project size. Small projects (<10 specs): spec + single task is sufficient. Skip decision records for tooling, config, and dependency choices — note them inline in the task body. Reserve decision records for choices that affect observable behavior or constrain future work.

**TODO:** when does detailed design (module boundaries, internal interfaces) happen? Must be after spec but before tests — tests need to know what to import. But locking design too early over-constrains implementation.

## Drift Detection

Detect source files that changed after the governing spec was last touched:

```bash
spec_commit=$(git log -1 --format=%H -- worklog/spec/s0001-auth.md)
git diff "$spec_commit"..HEAD -- src/auth/** src/middleware/session.ts
```

Non-empty diff = potential drift. `paths` in spec frontmatter provides the file mapping; git history provides the watermark. Nothing stored in the spec.

## Scripts

`worklog/script/`. Python. Accept `-w PATH` for worklog root (default: `./worklog`).

| Script | Purpose |
|--------|---------|
| `validate.py` | Dangling refs, invalid statuses, missing required fields |
| `drift.py` | Spec-code drift report for all specs with `paths` |
| `next-id.py <type>` | Next available ID (scans active + archive) |

**TODO:** scripts not yet implemented.

**TODO:** test ↔ spec traceability — no design yet for linking test files/cases back to the spec they verify.

</skill>
