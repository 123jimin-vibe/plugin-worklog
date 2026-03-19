# Worklog

## Motivation

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

## Key Ideas

--------

<!-- Draft -->

## Ideas

- Manage bug and work tracking in-repo.
- Documentation-driven:
  - Specs become authoritative source on program's functions.
  - Tests are generated from specs, *not* from implementations.

## Previous Attempt

## Pitfalls

- Human-readable manual/documentation is not always suitable to be used as specs.
  - Information duplication happens between documentation and spec.
- AI agents often have problems bookkeeping specs.
- Document-driven not adhered to well in practice.
- Specs must reflect latest code change, but often become out-of-sync in practice.
  - Unexpected inter-spec dependency.
  - Agents writing codes before updating spec.
- Confusion between a 'plan' and a 'spec'.
- Confusion between a 'plan' and a 'task'.

### Writing Specs is not simpler than Writing Code

- Agents (and human) tend to try to define every aspects of public APIs, including signature, ...
- Adhering to it: need to be synced (too) often when minor details are revised.
- Not adhering to it: some "non-document-driven" aspects starts happening.