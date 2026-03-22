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

- **Assumes `git`.** Entities version-tracked with source. Lean on `git log`/`git blame` for history, authorship, diffs — don't duplicate in metadata.
- **SKILL.md is the comprehensive reference.** Full instructions: entity schemas, lifecycle, validation, commands.
  - In-repo files (`AGENTS.md`, spec headers, etc.) contain only concise reminders pointing agents to the skill — not full documentation. Short triggers, not reference material.
- **Intuitive by default.** Conventions inferable from file structure, frontmatter keys, and naming alone.
  - Minimizes token economy impact ([context-file-effectiveness.md](./resource/context-file-effectiveness.md): over-specified context costs >20% more tokens for negligible gain).
- **Concise files.** All worklog content (specs, tasks, decisions, brainstorm docs) must avoid padding phrases, needless reiteration, and filler. Say it once, say it precisely.
- Markdown with TOML frontmatter. Python scripts for management (version-tracked; `.gitignore` for `.pyc`/`__pycache__/`).

Scratch directory structure for `/worklog/`:

- `/worklog/spec/**/s0000-spec-name.md` — **Authoritative architectural specification.**
  - Tests MUST derive from specs, written BEFORE implementation.
  - Spec takes priority over docs/tests/impls. If mistake suspected, agents MUST ask user.
  - Bikeshedding: nested folders vs. frontmatter for categorization? Filename prefix?
- `/worklog/task/t0000-task-name.md` — Unit of work.
  - Bikeshedding: archive location? Naming (`task`/`job`/`work`)?
- `/worklog/script/` — Bookkeeping scripts.
  - Validation (schema, dangling refs, stale `blocked_by`).
  - Summarization (onboarding / context budget).
  - Reverse-lookup search.

TODO:

- Onboarding
- Decision Records
- Cross-cutting spec relationships (logging, error handling policy)
- Specifying dangers and anticipated changes
- Test ↔ spec traceability
- Agent workflow: task lifecycle, enforcement (hooks/gates/validation), trigger-based rules vs. reference docs
- Spec content guidance: observable behavior vs. implementation details; over-specification resistance
- Task types: implementation, investigation (bfc t0007), chore
- Task sizing: single-session completion (bfc evidence); large tasks need detailed specs
- Context budget: how much worklog to load per session; avoid "document-directed exploration" trap

Unanswered questions:

- **Incomplete specs**: plans and specs as separate entities seems inadequate → see `expr-workflows.md` (spec-with-progression alternative).
- **Spec evolution**: versioning? Diff history? Or rely on git?
- **Specless tasks**: yes for chores. Can a task create a spec?
- **Empirical validation**: indicators (LoC/file, LoC/commit) not metrics — optimizing them induces reward-hacking.
- **Plan tier**: removed or deferred? v1's spec/plan boundary was problematic (pitfalls.md, case-study-bfc.md).
- **Multi-agent coordination**: concurrent agents may conflict on spec/task modifications.
- **Agent-agnosticism**: methodology is generic; first implementation is Claude Code skill. Portable to Codex/Copilot?
