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
paths = ["src/auth/**", "src/middleware/session*"]
+++
```

Required sections: behavior, constraints, anticipated changes, dangers. Mark unapproved items `TODO`.

`paths` — glob patterns for governed source files. Prefer broad globs (`src/auth/**`), not individual files. Omit for cross-cutting or conceptual specs.

No status field — specs are always current. No dates — git tracks history.

**Not implementation details.** Describe *what the system does and why*, not *how the code is structured*. No API signatures, class names, file paths, version numbers, or directory layouts in spec body.

**Structural vs. behavioral updates.** Structural edits (typos, wording, `paths`, section reorganization) are free. Behavioral changes (what the system does) require user approval. Discussion != approval.

**Precedence.** Spec is authoritative over source code and tests. Code diverging from spec = bug in the code. Tests derive from the spec. If the spec seems wrong, ask the user — never silently override.

**Drift detection.** Compare spec's last git commit against changes to its `paths` globs. Non-empty diff = potential drift.

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

`modifies` — spec IDs whose governed paths this task touches. Empty only for chores outside all spec paths.

**Status lifecycle:** `pending` → `active` → `done` → archived. Also: `blocked` (returns to `active` when unblocked), `cancelled` (requires explanation; decision record recommended if non-trivial context).

**Archiving.** When done, move to `worklog/archive/task/`. Before moving, verify the governing spec is still consistent with the completed work.

**Stubs.** If a task delivers stubs rather than complete implementations, the governing spec must retain TODO markers. Stubs must never be presented as complete.

**Rules:**

- **Tests before implementation.** Tests derive from spec, not code.
- **Test isolation.** Test agent receives the spec only — no function names, signatures, or implementation details. Test agent must not read source files under the spec's `paths`. If the spec is insufficient to write tests, that is a spec deficiency — surface it to the user.
- **Survey before building.** Check in-repo code and dependencies first. Reimplementing existing functionality is forbidden.
- **Approval = explicit confirmation.** To modify a spec's observable behavior, the user must explicitly confirm. When in doubt, ask.
- **Surface ambiguity.** When scope is unclear, ask — don't assume.
- **Escalate when stuck.** No spiraling into rewrites, no bailing silently, no effort-vs-value judgment without user input.
- **No antipatterns.** Injection, unbounded allocations, N+1 queries, bare catch, insecure defaults are never acceptable.
- **Session resume.** Re-orient from worklog state, not prior session context. The worklog is your memory.

**Forbidden:**

- Implementation without a covering spec.
- Implementation before tests.
- Modifying a spec's observable behavior without user approval.
- Tests that verify implementation structure instead of spec behavior.
- Behavioral changes disguised as refactoring.
- Regression test written after the fix (must fail before fix).
- Distorting code to route around a bug instead of fixing or reporting it.
- Fixing only the observed failure without evaluating whether it's a general problem.
- Implementation details in specs (see Spec above).
- Test agent reading source files or receiving implementation details from the parent agent.

### Decision

Immutable record of *why* a choice was made.

```toml
+++
id = "d0001"
title = "No recursion in macros"
relates_to = ["s0007"]
supersedes = []
+++
```

Body: context → choice → rationale → consequences. Never edit after creation — supersede with a new decision. Trivial fixes (typos, formatting) are acceptable. Never archived (unless superseded).

Create when: non-trivial choice, design flaw discovered, requirement changed, cost/benefit abandonment. Reserve for choices that affect observable behavior or constrain future work. For small projects, inline in the task body is acceptable.

### Relationships

All forward-only. Reverse lookups via grep — never stored.

```
task ──modifies──────▶ spec       (which specs this task changes)
task ──blocked_by────▶ task       (ordering dependency)
decision ──relates_to──▶ spec     (which spec this decision concerns)
decision ──supersedes──▶ decision (replaces a prior decision)
spec.paths ───────────▶ source    (which files this spec governs)
```

## Scripts

`plugin/skills/worklog/script/`. Python. Accept `-w PATH` for worklog root (default: `./worklog`).

| Script | Purpose |
|--------|---------|
| `validate.py` | Dangling refs, invalid statuses, missing required fields, duplicate IDs, unknown tags |
| `next_id.py <type>` | Next available ID (scans active + archive) |
| `drift.py` | Spec-code drift report for all specs with `paths` |
| `search.py` | Query entities by tag, status, or relationship |
| `list.py` | List entities with optional grouping and sorting |

## Workflows

| Workflow | Flow | Key constraint |
|----------|------|----------------|
| **Greenfield** | spec → task(s) → decision(s) | Tests before implementation |
| **Bug fix** | task → spec (if gap revealed) | Regression test must fail before fix |
| **Refactor** | task → spec (if boundaries change) | No behavioral change; existing tests as safety net |
| **Investigation** | task → decision / spec / nothing | Output is knowledge, not code; findings in task body |
| **Chore** | task | Rarely touches specs |
| **Hotfix** | task → decision | Compressed process; post-mortem mandatory |

Ceremony scales with project size. Small projects (<10 specs): spec + single task is sufficient. Reserve decision records for choices that affect observable behavior or constrain future work.

</skill>
