---
name: worklog
description: "Spec-driven development methodology via flat-file worklog. Trigger on: create task, plan work, track progress, initialize worklog, manage specs, check drift, what should I work on, resume work."
---

<skill id=worklog>

# Worklog

Specs define what the system is. Tasks change it. Decisions record why.

Root: `worklog/`. If absent, create `worklog/{spec,task,decision}/` and `worklog/archive/task/`.

## Entities

ID: prefix + digits (`s0001`, `t0012`, `d0001`); allocate via `next_id.py`. Filename: `{id}-kebab-name.md`. Frontmatter: TOML fenced by `+++`.

### Spec

```toml
+++
id = "s0001"
title = "User Authentication"
tags = ["auth"]
paths = ["src/auth/**", "src/middleware/session*"]
+++
```

Required sections: Observable Behavior, Constraints, Anticipated Changes, Dangers.

Behavioral items bind. Write only user-stated behavior + its direct entailments. Litmus before writing an item: would you ask the user to confirm it? yes => not stated => Proposals (or Anticipated Changes), never a behavioral section. Stated = approved: don't re-ask; ask only what is genuinely undecided.

`UNIMPLEMENTED` = approved-but-unbuilt; marking an item != approving it. New spec for unbuilt work => every behavioral item starts `UNIMPLEMENTED`. Remove a marker only against verified implementation (archive write-back, or direct code inspection) — user claim != verification. Spec stays authoritative regardless of markers.

`paths` — globs for governed source files; prefer broad (`src/auth/**`). Omit for cross-cutting or conceptual specs.

Every sentence binds. Specs are always current: no status fields/sections, no dates, no history or narration — git holds history, tasks hold work state. Cut sentences adding no behavior, constraint, or danger; keep qualifiers that change behavior. One rule, one place.

Describe what the system does, not how code is structured — no API signatures, class names, file paths, version numbers in spec body.

Structural edits (typos, wording, `paths`, reorganization): no approval needed. Behavioral changes: explicit user confirmation required. Discussion != approval.

Before updating: check specs with overlapping tags or `paths` for contradictions; extend existing specs over creating new ones.

Precedence: spec > code > tests. Divergence from spec = code bug. Spec seems wrong => ask; never silently override.

Drift detection: spec's last git commit vs subsequent changes under its `paths`; non-empty diff => potential drift.

### Task

Atomic unit of work, completable in one session. Frontmatter: `id`, `title`, `tags` as in spec, plus:

- `status` — `pending` → `active` (set on start) → `done` (set on finish; then archive). Also: `blocked` → `active` when unblocked; `cancelled` requires explanation (decision record recommended).
- `modifies` — spec IDs whose governed behavior this task touches; empty only for chores outside all spec-governed behavior.
- `blocked_by` — task IDs that must complete first.
- `priority` — optional int >= 0 (0 = most urgent); ranks task in `backlog.py` triage. Absent = untriaged.

Archiving = write-back, not a check. Not delegatable, not skippable, even if user claims reviewed or already updated the specs.

1. `archive.py <task-id>` without `--confirm` — prints each `modifies` spec + its drift. Never `--confirm` first.
2. Write-back each spec in `modifies`: fold in the new current state (or confirm wording already covers it); remove markers the work resolved. Assert only what the delivered work verifiably does — re-read spec and delivered work. Stub or partial delivery => markers stay (or get added); never present stubs as complete.
3. `archive.py <task-id> --confirm` — moves the task (`git mv` when tracked).

Future agents read specs — state recorded only in archived tasks or decisions is lost. Decision-introduced constraint => into the spec too; decision keeps the why.

Rules:

- Tests precede implementation; derive them from spec, not code.
- Test isolation: test agent gets spec only — no function names, signatures, implementation details; must not read source under spec `paths`. Insufficient spec = spec deficiency => surface it.
- Survey before building: check in-repo code + dependencies first; reimplementing existing functionality forbidden.
- Scope unclear => ask; don't assume.
- Stuck => escalate: no spiraling, no silent bailing, no effort-vs-value judgment without user input.
- No antipatterns: injection, unbounded allocations, N+1 queries, bare catch, insecure defaults.
- Session resume: re-orient from worklog state, not prior session context — worklog is your memory.
- Plan in worklog: task/spec files are the planning medium; no external planning tools when worklog suffices.
- Comments: only what code can't say (why, invariants, non-obvious constraints) — cite the governing spec/decision ID, don't restate it. No task history or process narration in code.
- Names travel without context: public names read unambiguously at import sites — carry the domain; prefer the governing spec's vocabulary.

Forbidden:

- Implementation without a covering spec.
- Tests verifying implementation structure instead of spec behavior.
- Behavioral changes disguised as refactoring.
- Regression test written after the fix (must fail before fix).
- Routing around a bug instead of fixing or reporting it.
- Fixing only the observed failure without checking if it generalizes.
- Modifying spec behavior during task work without approval.

### Decision

Immutable record of why. Frontmatter: `id`, `title`, `relates_to` (spec IDs concerned), `supersedes` (decision IDs replaced).

Body: context → choice → rationale → consequences. Rationale = reasons actually given; never invent motives for the record. Never edit substance — supersede instead; typo/formatting fixes only. Archive only when superseded.

Create when: non-trivial choice, design flaw, requirement change, feature abandonment. Small projects: recording in the task body is acceptable.

### Relationships

Stored on the referencing entity only — `task.modifies` → spec · `task.blocked_by` → task · `decision.relates_to` → spec · `decision.supersedes` → decision · `spec.paths` → source files. Reverse lookup: grep.

## Scripts

Scripts ship with the plugin at `${CLAUDE_SKILL_DIR}/scripts/` — never inside the repository: no `<repo>/scripts/`, no `<repo>/worklog/scripts/`. `-w` sets worklog root (default `./worklog`). This section is authoritative. Invoke:

```
python ${CLAUDE_SKILL_DIR}/scripts/<script>.py [args] [-w PATH]
```

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
| Greenfield | spec → task(s) → decision(s) | Tests before implementation |
| Bug fix | task → spec (if gap revealed) | Regression test must fail before fix |
| Refactor | task → spec (if boundaries change) | No behavioral change; existing tests as safety net |
| Investigation | task → decision / spec / nothing | Output is knowledge, not code; findings in task body |
| Chore | task | New observable behavior is never a chore |
| Hotfix | task → decision | Compressed process; post-mortem mandatory |

Ceremony scales with project size; small projects (<10 specs): spec + single task suffices.

</skill>
