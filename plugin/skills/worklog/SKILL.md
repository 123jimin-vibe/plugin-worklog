---
name: worklog
description: "Spec-driven development methodology via flat-file worklog. Trigger on: create task, plan work, track progress, initialize worklog, manage specs, check drift, what should I work on, resume work."
---

<skill id=worklog>

# Worklog

Specs define what the system is. Tasks change it. Decisions record why.

Root: `worklog/`. If absent, create `worklog/{spec,task,decision}/` and `worklog/archive/task/`.

## Entities

IDs: prefix letter + digits (`s0001`, `t0012`, `d0001`). Use `next_id.py` to allocate — it scans active + archive. Filename: `{id}-kebab-name.md`. TOML frontmatter delimited by `+++`.

### Spec

Describes observable behavior, constraints, anticipated changes, dangers.

```toml
+++
id = "s0001"
title = "User Authentication"
tags = ["auth"]
paths = ["src/auth/**", "src/middleware/session*"]
+++
```

Required sections: behavior, constraints, anticipated changes, dangers.

**Behavioral items are binding.** Write what the user stated and its direct entailments; invent nothing. Stated items are approved — don't re-ask; ask only when a needed behavior is genuinely undecided. Before writing any behavioral item, test it: would you ask the user to confirm this? Then it was not stated — it goes to **Proposals** (or Anticipated Changes), never into a behavioral section. `UNIMPLEMENTED` means approved-but-unbuilt, not unconfirmed; marking an inferred item does not license it. In a new spec for unbuilt work, every behavioral item starts `UNIMPLEMENTED`. Markers track implementation status — spec is authoritative regardless. Remove markers when implemented.

`paths` — glob patterns for governed source files. Prefer broad globs (`src/auth/**`). Omit for cross-cutting or conceptual specs.

**Every sentence binds.** Specs are always current: no status fields or sections, no dates, no history or narration — git holds history, tasks hold work state. Cut any sentence that adds no behavior, constraint, or danger; keep qualifiers that change behavior. One rule, one place.

**Not implementation details.** Describe *what the system does*, not *how code is structured*. No API signatures, class names, file paths, or version numbers in spec body.

**Structural vs. behavioral.** Structural edits (typos, wording, `paths`, reorganization) need no approval. Behavioral changes require explicit user confirmation. Discussion is not approval.

**Before updating,** check specs with overlapping tags or `paths` for contradictions. Extend existing specs rather than creating new ones.

**Precedence.** Spec > code > tests. Divergence from spec = code bug. If spec seems wrong, ask — never silently override.

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

`modifies` — spec IDs whose governed behavior this task touches. Empty only for chores outside all spec-governed behavior.

`priority` — optional non-negative int (0 = most urgent); ranks the task in `backlog.py`'s triage view. Absent = untriaged.

**Status lifecycle:** `pending` → `active` → `done` (then archive). Also: `blocked` → `active` when unblocked, `cancelled` (requires explanation; decision record recommended). Set `active` when starting, `done` when finishing.

**Archiving.** Completion is a write-back, not a check: fold the new current state into every spec in `modifies` (or confirm the wording already covers it), remove `UNIMPLEMENTED` markers the work resolved — only then archive. The write-back asserts only what the delivered work verifiably does — re-read the governing spec and the delivered work; stubbed or partial delivery keeps (or gains) markers instead of asserting the behavior. Future agents read specs; archived tasks and decisions are history, not reference — state recorded only there is lost. A constraint introduced by a decision goes into the spec too; the decision keeps the why. Archive in two steps with `archive.py <task-id>`: first without `--confirm` — it prints each spec in `modifies` with its drift for the write-back — then with `--confirm` to move (`git mv` when tracked). Never `--confirm` first. The write-back is not delegatable, not skippable, even if the user claims to have reviewed or already updated the specs.

**Stubs.** If a task delivers stubs, specs in `modifies` must retain `UNIMPLEMENTED` markers. Never present stubs as complete.

**Rules:**

- **Tests before implementation.** Tests derive from spec, not code.
- **Test isolation.** Test agent receives spec only — no function names, signatures, or implementation details. Must not read source under spec `paths`. Insufficient spec = spec deficiency; surface it.
- **Survey before building.** Check in-repo code and dependencies first. Reimplementing existing functionality is forbidden.
- **Approval = explicit confirmation.** Modifying spec behavior requires explicit user confirmation.
- **Surface ambiguity.** When scope is unclear, ask — don't assume.
- **Escalate when stuck.** No spiraling, no bailing silently, no effort-vs-value judgment without user input.
- **No antipatterns.** Injection, unbounded allocations, N+1 queries, bare catch, insecure defaults.
- **Session resume.** Re-orient from worklog state, not prior session context. The worklog is your memory.
- **Plan in worklog.** Task and spec files are the planning medium. Don't use external planning tools when worklog suffices.
- **Comments say what code cannot.** Why, invariants, non-obvious constraints — reference the governing spec/decision ID instead of restating it. No task history or process narration in code.
- **Names travel without context.** Public names must read unambiguously at their import sites: carry the domain in the name; prefer the governing spec's vocabulary.

**Forbidden:**

- Implementation without a covering spec.
- Tests verifying implementation structure instead of spec behavior.
- Behavioral changes disguised as refactoring.
- Regression test written after the fix (must fail before fix).
- Routing around a bug instead of fixing or reporting it.
- Fixing only the observed failure without checking if it generalizes.
- Implementation details in specs.
- Modifying spec behavior during task work without approval.

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

Body: context → choice → rationale → consequences. Rationale records the reasons actually given — never invent motives for the record. Do not edit substance — supersede with a new decision. Trivial fixes (typos, formatting) are the only acceptable edits. Decisions stay in active directory; archive only when superseded.

Create when: non-trivial choice, design flaw, requirement change, feature abandonment. For small projects, recording in the task body is acceptable.

### Relationships

Stored on referencing entity only. Reverse lookup: grep.

```
task ──modifies──────▶ spec       (which specs this task changes)
task ──blocked_by────▶ task       (ordering dependency)
decision ──relates_to──▶ spec     (which spec this decision concerns)
decision ──supersedes──▶ decision (replaces a prior decision)
spec.paths ───────────▶ source    (which files this spec governs)
```

## Scripts

Scripts ship with the plugin at `${CLAUDE_SKILL_DIR}/scripts/` — never inside the repository: there is no `<repo>/scripts/` and no `<repo>/worklog/scripts/`. Invoke:

```
python ${CLAUDE_SKILL_DIR}/scripts/<script>.py [args] [-w PATH]
```

Python. `-w` sets the worklog root (default `./worklog`). This section is authoritative.

| Script | Flags | Purpose |
|--------|-------|---------|
| `validate.py` | | Dangling refs, invalid statuses, missing fields, duplicate IDs, unknown tags, `blocked_by` cycles, archive/cancel rules |
| `next_id.py` | `<type>` | Next available ID (scans active + archive) |
| `drift.py` | | Spec-code drift for specs with `paths` (uncommitted changes included); unverifiable/unmonitored specs to stderr |
| `search.py` | `--tag TAG`, `--status STATUS`, `--modifies ID`, `--relates-to ID`, `--blocked-by ID`, `--type TYPE`, `--archived` | Query entities (excludes archive unless `--archived`) |
| `list.py` | `--type TYPE`, `--group-by {type,status,tag}`, `--sort {id,title}`, `--archived` | List entities |
| `archive.py` | `<task-id>...`, `--confirm` | Archive done/cancelled task(s): prints governing specs + drift, moves on `--confirm` (each ID independent) |
| `backlog.py` | | Triage view: open tasks ranked by `priority`, `UNIMPLEMENTED` items inherit covering task's rank, untriaged surfaced |

## Workflows

| Workflow | Flow | Key constraint |
|----------|------|----------------|
| **Greenfield** | spec → task(s) → decision(s) | Tests before implementation |
| **Bug fix** | task → spec (if gap revealed) | Regression test must fail before fix |
| **Refactor** | task → spec (if boundaries change) | No behavioral change; existing tests as safety net |
| **Investigation** | task → decision / spec / nothing | Output is knowledge, not code; findings in task body |
| **Chore** | task | New observable behavior is never a chore |
| **Hotfix** | task → decision | Compressed process; post-mortem mandatory |

Ceremony scales with project size. Small projects (<10 specs): spec + single task is sufficient.

</skill>
