+++
id = "s0001"
title = "Worklog Methodology"
tags = ["core"]
paths = ["plugin/**"]
+++

# Worklog Methodology

Spec-driven development methodology for AI agents. Externalizes project state into flat files so agents reorient from written artifacts rather than session continuity.

## Entities

Four types under `worklog/`:

- **Spec** — living design reference. Observable behavior, constraints, anticipated changes, dangers. No status field. TOML frontmatter with `paths` globs for drift detection.
- **Task** — atomic unit of work. Statuses: pending → active → done | blocked. Archived when done.
- **Decision** — immutable record of why. Superseded by new decisions, never edited or archived.
- **Script** — Python automation (validation, drift detection, ID assignment).

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
- Surface ambiguity; escalate when stuck.
- Record non-trivial decisions.
- No antipatterns (injection, unbounded allocations, N+1, bare catch, insecure defaults).
- Session resume from worklog state, not prior context.

## Workflows

Six workflows scaling ceremony with project size: greenfield, bug fix, refactor, investigation, chore, hotfix.

## Drift Detection

Git history as watermark — compares spec's last-touched commit against source changes under `paths` globs.

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
