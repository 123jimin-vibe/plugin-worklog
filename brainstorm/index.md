# Worklog

Brainstorm for a plugin that enforces software development methodology on AI agents. Starts with problem analysis and requirement gathering; design decisions follow once reasoning justifies them.

- `resource/` — external references (research papers, prior art, paradigm evaluations). Raw material, not conclusions.
  - `worklog-skill-v1.md` and `development-paradigms.md` are prior attempts — not authoritative. Ideas from them require independent justification before adoption.
  - Empirical findings (e.g. `context-file-effectiveness.md`) can be treated as evidence.
- `pitfalls.md` — catalog of AI agent failure modes relevant to this plugin.
- `case-study-bfc.md` — observations from a project that used the previous worklog system.
- `expr-spec-structure.md` — evaluation of spec representation approaches (in-source docgen, per-directory README, flat/hierarchical separate directory, wiki-style, ADRs, etc.), with simulations against bfc.
- `expr-documentation.md` — documentation structure (TODO).
- `expr-workflows.md` — typical project workflows, entity analysis, git utilization, mistake/history tracking.

## Motivation

### [Software Architecture Principles](./software-architecture-principles.md)

### Idealistic AI Agent Workflow

With infinite context and perfect retention, an agent would: receive all files + full history, write code, remember feedback, resume perfectly across sessions. This would obsolete `AGENTS.md`/`CLAUDE.md`, design docs, task tracking, and context management.

### Consequences of Imperfect Context

Real agents have finite context and no cross-session memory. This causes:

- **Loss of continuity**: re-onboard each session, no learning from failures. `CLAUDE.md`/`AGENTS.md` [are ineffective](./resource/context-file-effectiveness.md).
- **DRY violations**: re-implementing existing features, especially undocumented ones.
- **Stale related artifacts**: failing to update code, docs, and specs together.

### Problems Even with Perfect Context

- Implementation leaking into tests.
- Strategic judgment failures: no abort/continue calibration, blindness to tech debt, append-only bias.

## Goals

**Meta-goal:** make AI agents **reliable** for large projects under minimal human supervision.

**Goal:** enforce domain/language-agnostic development methodology for AI agents.

**Empirical stance:** methods validated through real-world usage. TDD assumed as baseline; other methods require empirical justification.

**Non-goal (for now):** performance of knowledge base operations. Linear scan acceptable. Correctness first.

## Design Sketch

### Constraints

- **Assumes `git`.** History, authorship, diffs via `git log`/`git blame` — don't duplicate in metadata. Multi-agent coordination via worktrees/branches/merges.
- **SKILL.md is the comprehensive reference.** In-repo files contain only concise triggers pointing to the skill.
- **Intuitive by default.** Conventions inferable from file structure, frontmatter keys, naming. Minimizes token cost ([context-file-effectiveness.md](./resource/context-file-effectiveness.md)).
- **Concise files.** No padding, no reiteration. Say it once, precisely.
- **TODO aspects clearly labelled.** In specs and tasks, unfinished/planned items must be visually distinct from completed/current-state items.
- **Agent-agnostic.** Methodology is generic; portable via `AGENTS.md`, explicit prompt segments, etc. First implementation targets Claude Code skill.
- Markdown with TOML frontmatter. Python scripts for management.

### Entities

| Entity | Purpose | Location | Lifecycle |
|--------|---------|----------|-----------|
| **Spec** | Authoritative design reference (observable behavior, constraints, dangers, anticipated changes). | `/worklog/spec/**/s0000-name.md` | Created (items start as TODO) → items marked done as tasks complete → updated in-place. |
| **Task** | Atomic unit of work. | `/worklog/task/t0000-name.md` | `pending` → `active` → `done` (or `blocked`). Archived when done. |
| **Decision** | Immutable record of *why* a choice was made. | `/worklog/decision/d0000-name.md` | `accepted` → possibly `superseded`. Never archived. |
| **Script** | Bookkeeping automation (validation, summarization, reverse-lookup). | `/worklog/script/` | — |

### Relationships

```
task ──modifies──────▶ spec       (which specs this task changes)
task ──blocked_by────▶ task       (ordering dependency)
decision ──relates_to──▶ spec     (which spec this decision is about)
decision ──supersedes──▶ decision (replaces a prior decision)
spec ──sources─────────▶ paths    (which source files this spec governs)
```

All references are forward-only. Reverse lookups computed by script or grep — never stored.

### Precedence

1. Spec over source code (divergence = bug).
2. Spec over tests (tests derive from spec).
3. If spec suspected wrong → ask user.

### Supported Workflows

See [`expr-workflows.md`](./expr-workflows.md) for full catalog with happy paths, incidents, and forbidden cases.

| Workflow | Entities involved | Notes |
|----------|-------------------|-------|
| Greenfield feature | spec → task(s) → decision(s) | Tests before implementation. |
| Bug fix | task → spec (if gap revealed) | Regression test must fail before fix. |
| Refactoring | task → spec (if boundaries change) | No behavioral change. Existing tests as safety net. |
| Investigation | task → decision / spec / nothing | Output is knowledge, not code. |
| Chore | task | Rarely touches specs. |
| Hotfix | task → decision (post-mortem) | Compressed process. Post-mortem mandatory. |

### TODO

- Cross-cutting specs (logging, error handling policy).
- Test ↔ spec traceability.
- Enforcement mechanism: hooks/gates/validation vs. reference docs. Includes enforcing prompt lifecycle updates (spec marked done as tasks complete).
- Task types (`implementation`, `investigation`, `bugfix`, `chore`) — explicit field vs. inferred from relationships.

