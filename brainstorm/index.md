# Worklog

Brainstorm for a plugin that enforces software development methodology on AI agents. Starts with problem analysis and requirement gathering; design decisions follow once reasoning justifies them.

- `resource/` — external references (research papers, prior art, paradigm evaluations). Raw material, not conclusions.
  - `worklog-skill-v1.md` and `development-paradigms.md` are prior attempts — not authoritative. Ideas from them require independent justification before adoption.
  - Empirical findings (e.g. `context-file-effectiveness.md`) can be treated as evidence.
- `pitfalls.md` — catalog of AI agent failure modes relevant to this plugin.
- `case-study-bfc.md` — observations from a project that used the previous worklog system.
- `expr-spec-structure.md` — evaluation of spec representation approaches (in-source docgen, per-directory README, flat/hierarchical separate directory, wiki-style, ADRs, etc.), with simulations against bfc.
- `expr-documentation.md` — documentation structure (TODO).

## Motivation

### Goals of Software Architecture

These observations are general to software engineering, not specific to AI agents.

- Small and large projects **require different methodologies**.
  - LEGO house vs. mile-high skyscraper.
- Software development stages:
  1. Requirements
  2. Architecture Design
  3. Detail Design
  4. Implementation
  5. QA / Testing
- Two classes of lifecycle models:
  - Sequential (Waterfall)
  - Iterative (Agile, XP, ...)
  - Iterative is usually superior for software.
  - Fixed requirements are ideal but rare in practice.
    - Requirements change frequently.
    - Premature design decisions become costly under change.
    - True requirements are often discovered through implementation.
- Bug fix cost is lowest when caught at the earliest stage.

These observations imply the following architectural principles:

Requirements must be explicit and capture *intent*:

- Focus on *what* and *why*, not *how*.
- Prefer "XX is problematic" over "YY needs to be improved/implemented for XX".
- Avoid programming-specific framing.
  - Exception: the problem domain itself is programming-related.

Architecture should *localize the impact of changing requirements*:

- Record reasons behind decisions.
- A requirement change should touch as few components as possible.
- Define *building blocks* with:
  - Clearly defined responsibilities.
  - Minimal dependencies on other blocks.
  - Explicitly declared allowed and forbidden inter-block dependencies.
- Clearly specify *business constraints* and their architectural effects.
- UI layer (CLI/GUI/webpage/...) should be easily replaceable.
- Specify required *robustness* level — this also prevents over-engineering robustness.
- Specify anticipated requirement changes and strategies for handling them.
- Be *simple*.
  - Feel "natural and easy".
  - Largely independent from (but still aware of) execution environment and programming language.
  - Exclude unnecessary features.
- Explicitly specify *dangers*.

Detail design should derive from and be consistent with the architecture:

- Minimal complexity.
  - Prefer "simple and obvious" over "clever".
  - Actively remove features outside the project's scope.
- Ease of maintenance.
- Loose coupling.
- Extensibility and reusability.
- Components: high fan-in (used by many), low fan-out (depends on few).

### "Idealistic" AI Agent Workflow

Assume an AI agent with *infinite context window* and *perfect context retention*.

1. Human describes what they want in natural language.
2. Agent receives:
    - Every file in the project.
    - Knowledge base: project docs, dependency docs, relevant articles.
    - Full history: every prior decision and mistake.
3. Agent writes code. Remembers everything.
4. Human reviews and gives feedback. Agent remembers.
5. Next session: agent resumes exactly where it left off.
6. Agent knows precisely what's done, what's pending, what failed, what was decided and why.

This would make the following obsolete:

- `AGENTS.md` / `CLAUDE.md` for preventing repeated mistakes.
- Design documentation: context already contains all necessary information.
- Task tracking (e.g. [beads](https://github.com/steveyegge/beads)).
- Context management.

### Direct Consequences of Imperfectness

A real AI agent has neither infinite context nor perfect retention. Token economy constrains context construction, causing:

- Loss of continuity.
  - Must re-onboard each session.
  - No learning from failures.
  - Existing mitigations (`CLAUDE.md`, `AGENTS.md`) [are ineffective](./resource/context-file-effectiveness.md).
- DRY violations.
  - Re-implementing existing features — especially those too trivial to have been documented, so the agent never discovers them.
- Failing to update related code and documentation.

### Problems under Idealistic Workflow

Issues that persist even with perfect context:

- Implementation leaking into tests.
- Strategic judgment failures:
  - No abort/continue calibration.
  - Blindness to tech debt (future cost-of-change).
  - Append-only bias instead of occasional refactoring.

## Goals

**Meta-goal:** make AI agents usable and **reliable** for large, real-world projects, even under minimal human supervision.

**Goal:** provide and enforce domain- and language-agnostic software development methodology for AI agents.

**Empirical stance:** methods must be validated through real-world usage before being considered effective. TDD is assumed as a baseline; other methods require empirical justification.

**Non-goal (for now):** performance of knowledge base operations. Linear scan over specs/plans/tasks is acceptable. Correctness of methodology comes first.

## Design Sketch

- Information (TBD) stored as Markdown with TOML frontmatter.
  - In-repo Python scripts for managing data (as in worklog v1). Must `.gitignore`.
  - Consider <https://github.com/steveyegge/beads>; prefer simplicity for now.

Scratch directory structure for `/worklog/`:

- `/worklog/spec/**/s0000-spec-name.md`
  - **Authoritative architectural specification** of a component.
    - All tests MUST be derived from specs, and MUST be written BEFORE spec is implemented.
    - If specs contradict with docs/tests/impls, spec takes priority.
      - If a clear mistake is suspected, agents MUST ask user and MUST NOT silently fix specs.
  - Source components (file/class/function/...) tagged with `@worklog s0000` comments.
    - Bikeshedding: exact comment form.
  - Important: nested folders or frontmatter for categorization?
  - Bikeshedding: include `s0000-` prefix in filename?
- `/worklog/task/t0000-task-name.md`
  - A unit of work to be implemented.
  - Bikeshedding: where to put completed tasks?
  - Bikeshedding: `task`, `job`, or `work`?

TODO:

- Onboarding
- Decision Records
- Relationships Between Specs
  - Cross-cutting specs (e.g. logging conventions, error handling policy)
- Specifying Dangers
- Anticipated Changes
- Test <-> Spec Traceability
- Agent Workflow
  - Task lifecycle (creation → implementation → completion)
  - Enforcement mechanisms (hooks, workflow gates, self-validation, ...)
  - Trigger-based rules vs. reference documents (agents don't re-read reference docs on every action; triggers fire at action time)
- Spec Content Guidance
  - What goes inside a spec? Observable behavior vs. implementation details.
  - Over-specification resistance: agents default to API signatures and field names, not behavior.
- Schema Enforcement
  - Canonical frontmatter schema definition.
  - Validation mechanism (bfc showed schema inconsistency creeping in without enforcement).
- Task Types
  - Investigation/research tasks (bfc t0007: started as research, not implementation).
  - Chore tasks (no spec relationship).
  - Implementation tasks (spec-linked).
- Task Sizing
  - bfc evidence: successful tasks completable in a single session.
  - The one large task that worked had an unusually detailed plan.
- Context Budget
  - How much of the worklog should an agent load per session?
  - Avoid "document-directed exploration" trap (context-file-effectiveness.md).

Unanswered questions:

- How to represent **incomplete specs**?
  - Treating plans and specs as entirely separate seems inadequate.
- How should specs evolve? (Versioning? Diff history? Or rely on git history alone?)
- Can a task exist without a corresponding spec?
  - Likely yes for "chore" tasks (e.g. fix typos throughout codebase).
- Can a task create a spec?
- What constitutes empirical validation of a method?
  - Indicator (not metric): natural average LoC per file, average LoC and files edited per commit.
  - Optimizing or prompting agents on these indicators is forbidden — optimizing a metric induces reward-hacking.
- Is the plan tier intentionally removed or deferred?
  - v1 had spec/plan/task; current sketch has spec/task only.
  - The spec/plan boundary was problematic in practice (pitfalls.md, case-study-bfc.md).
- Source code markers (`@worklog`): keep, automate, or drop?
  - bfc evidence: 1 of ~40 files adopted them. Manual maintenance failed.
  - Viable only if fully automated.
- Multi-agent coordination: in scope?
  - Concurrent agents may conflict on spec/task modifications.
  - Sub-agents lose parent context; no inter-agent communication channel.
- Agent-agnosticism: methodology vs. implementation boundary?
  - Methodology is domain- and language-agnostic; first implementation is a Claude Code skill.
  - Should the methodology be portable across agents (Claude Code, Codex, Copilot)?
