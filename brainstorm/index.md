# Worklog

- `resource/`
- `pitfalls.md`

## Motivation

### Goals of Software Architecture

These well-known observations are not specific to AI Agent programming.

- Small toy-project and large project **can't be developed using the same methodology**.
  - LEGO house vs. a mile-high skyscraper.
- Software development is typically classified in 5 stages:
  1. Requirements
  2. Architecture Design
  3. Detail Design
  4. Implementation
  5. QA / Testing
- Broadly speaking, there are two classes of lifecycle models:
  - Sequential (Waterfall)
  - Iterative (Agile, XP, ...)
  - For software development, iterative methods are usually better.
  - Fixed requirements is best-case scenario, but rarely achievable in practice.
    - Frequent modifications based on changing requirements is common.
    - This makes premature design decisions more costly.
    - One also discovers true requirements through the act of implementation itself.
- Cost of fixing bugs is lowest when caught at the earliest stage possible.

Those observation imply principles on software architecture design:

Requirements must be explicit, and must capture *intent*:

- Focus on *what* and *why*, but not *how*.
- Prefer "XX is problematic" but not "YY needs to be improved/implemented for XX".
- Must be written in a way that avoids programming-related aspects.
  - Exception: problem domain itself is relevant to programming.

Architecture should be optimized for *localizing changes on changing requirements*:

- Reasons behind decisions should be specified.
- A requirement change should touch as few components as possible.
- Define *building blocks*, where:
  - Responsibilities are clearly defined.
  - Dependency to other building blocks should be kept at minimum.
  - Communication between blocks should be clearly defined, including endorsement or prohibition on dependence relationship.
- *Business constraints* should be clearly specified, including its effect on the architecture.
- Changing UI (CLI/GUI/webpage/...) should be easily done.
- Should specify required amount of *robustness*, which also serves as a guide that prevents *over-engineering robustness*.
- Should specify expected requirement changes with strategy to execute them.
- Should be *simple*.
  - Should feel "natural and easy".
  - Largely independent (but still non-ignorable) from execution environment and programming langauge.
  - Should exclude unnecessary features.
- Should explicitly specify *dangers*.

Detail design should be derived from and consistent with the architecture:

- Minimal complexity.
  - Avoid "clever" solutions, prefer "simple" solutions that are easy to understand.
  - Always find opportunity to *remove* features that are not relevant to the scope of the project.
- Ease of maintenance.
- Loose connection.
- Extensibility and reusability.
- Components: high fan-in (used by many) and low fan-out (depends on few).

### "Idealistic" AI Agent Workflow

Let's assume that an AI agent has *infinite context window* with *perfect context retention*.

1. Human describes what they want in natural language.
2. Agent is fed with following resources:
    - Contents of every file in the project.
    - Knowledge base, including documentation for the project and dependencies, relevant articles, ...
    - All history, including every prior decisions and mistakes.
3. Agent writes code. Agent remembers.
4. Human reviews, give feedback. Agent remembers.
5. Next session: agent picks up exactly where it left off, as if it's been working on a second ago.
6. Agent exactly knows what's done, what's pending, what's tried and failed, what's decided and why.

This would make the following practices obsolete:

- `AGENTS.md` and `CLAUDE.md` to prevent agents from committing common mistakes.
- Design documentations: context likely contains all necessary information for design.
- Task tracking (such as [beads](https://github.com/steveyegge/beads)).
- Context management.

### Direct Consequences of Imperfectness

However, a *real* AI agent neither has infinite context window nor prefect context retention.
"Token economy" has to be taken into account when building context, results in following side-effects.

- Loss of continuity.
  - Have to onboard each time.
  - No "learning from failures".
  - Existing counter-measures (`CLAUDE.md`, `AGENTS.md`) [don't work well](./resource/context-file-effectiveness.md).
- Violation of DRY.
  - Re-implementing existing features, especially when it's something "trivial" to be documented.
- Failure to take care of relevant code and/or documentation.

### Problems under Idealistic Workflow

On the other hand, there are a few issues that may happen even with perfect context.

- "Leakage" of implementation into tests.
- Strategic judgment failures.
  - No abort/continue calibration.
  - Blindness to tech debt (future cost-of-change).
  - Defaults to append *only* instead of occasional refactor.

## Goals

The **meta-goal** of this plugin is to make using AI agents for large, real-world projects to be usable while remaining to be **reliable** even with minimal (but present) human supervision.

The goal of this plugin is to provide and enforce domain and language-agnostic software development methodology to AI agents.

## Method (Plan)

## Method (Concrete)