+++
id = "s0001"
title = "Worklog Methodology"
tags = ["methodology"]
paths = ["plugin/skills/worklog/SKILL.md"]
+++

# Worklog Methodology

Spec-driven development methodology for AI agents. Stores project state in flat files so agents can pick up where they left off without relying on session memory.

## Entities

Three entity types in `worklog/`. Entity specs in `worklog/spec/entity/`:

- **Spec** (s0011) — kept-up-to-date design reference. No status field.
- **Task** (s0012) — atomic unit of work. Statuses: pending → active → done | blocked.
- **Decision** (s0013) — permanent record of why a choice was made. Immutable, superseded only.

Scripts (s0010) are Python automation bundled with the plugin, separate from entity files.

## Relationships

Forward-only. Reverse lookups via grep.

- task → spec (modifies)
- task → task (blocked_by)
- decision → spec (relates_to)
- decision → decision (supersedes)
- spec → source files (paths)

## Precedence

1. Spec over source code (divergence = bug in code).
2. Spec over tests (tests derive from spec).
3. Spec suspected wrong → ask user, never silently override.

## Key Rules

- Tests before implementation, derived from spec not code.
- Test isolation: test agent receives spec only, not implementation details.
- Survey before building.
- Explicit approval required; discussion ≠ approval.
- Ask about unclear requirements; escalate when stuck.
- Record non-trivial decisions.
- No antipatterns (injection, unbounded allocations, N+1, bare catch, insecure defaults).
- Session resume from worklog state, not prior context.

## Workflows

Six supported workflows (s0004–s0009): greenfield, bug fix, refactor, investigation, chore, hotfix. Small projects need less process; large projects need more. Workflow specs are not implemented directly — other specs are shaped by them (e.g., a greenfield feature spec follows s0004's flow and forbidden list).

Each workflow spec defines:

1. **Flow** — happy, common, and rare paths merged into a flowchart. Each step names which entity type is created, updated, or archived.
2. **Forbidden** — actions never acceptable in this workflow.
3. **Anticipated Changes** — gaps in entity support, missing relationships, planned tooling.
4. **Dangers** — agent mistakes observed or anticipated for this workflow.

## Drift Detection

Compares when the spec was last touched (via git log) against changes to source files under its `paths` globs. If source changed after the spec, the spec may be stale.

## Delivery

Claude Code skill plugin. `plugin.json` manifest + SKILL.md as single authoritative file.

## Anticipated Changes

- Enforcement mechanism (hooks/gates).
- Scripts (validation, drift, ID assignment).
- Task type field.
- Test ↔ spec traceability.
- Spec-by-ID cross-referencing (replacing fragile relative paths).
- Convention for specs delegating behavioral details to reference docs.
- Additional bundled skills or scripts.

## Dangers

- Without enforcement, agents bypass the methodology (v1 lesson: manual validation gets skipped).
- Implementation details in specs drift immediately and create false authority.
- Test agents receiving implementation knowledge produce implementation-coupled tests.
