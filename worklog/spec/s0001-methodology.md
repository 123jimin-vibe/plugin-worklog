+++
id = "s0001"
title = "Worklog Methodology"
tags = ["core"]
paths = ["plugin/**"]
+++

# Worklog Methodology

A spec-driven development methodology that makes AI agents reliable for large projects under minimal human supervision.

## Core Premise

AI agents suffer from finite context, no cross-session memory, and poor strategic judgment. The worklog externalizes project state into flat files so agents can reorient from written artifacts rather than relying on session continuity.

## Entities

Four entity types, each in its own directory under `worklog/`:

- **Spec** — living design reference. Describes observable behavior, constraints, anticipated changes, dangers. Always current; no status field. TOML frontmatter with `paths` globs for drift detection.
- **Task** — atomic unit of work. Statuses: pending → active → done | blocked. Archived when done. References which specs it modifies.
- **Decision** — immutable record of why a choice was made. Never edited after acceptance; superseded by new decisions. Never archived.
- **Script** — Python automation for validation, drift detection, ID assignment.

## Relationships

All forward-only. Reverse lookups via grep.

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
- Approval means explicit confirmation; discussion ≠ approval.
- Surface ambiguity; escalate when stuck.
- Record non-trivial decisions.
- No antipatterns (injection, unbounded allocations, N+1, bare catch, insecure defaults).
- Session resume from worklog state, not prior context.

## Workflows

Six workflows scaling ceremony with project size: greenfield, bug fix, refactor, investigation, chore, hotfix.

## Drift Detection

Uses git history as watermark — compares spec's last-touched commit against source file changes under the spec's `paths` globs. No metadata stored in the spec itself.

## Delivery

Packaged as a Claude Code skill plugin. A `plugin.json` manifest declares name, description, and version. SKILL.md is the single authoritative file — the methodology is defined entirely within it.

## Anticipated Changes

- Enforcement mechanism (hooks/gates) beyond instruction-only rules.
- Scripts for validation, drift reporting, and ID assignment.
- Task type field (implementation, investigation, bugfix, chore, hotfix).
- Test ↔ spec traceability.
- Spec-by-ID cross-referencing (replacing fragile relative paths).
- Convention for specs that delegate behavioral details to external reference docs.
- Additional skills or scripts bundled alongside the core skill.

## Dangers

- Without enforcement, agents bypass the methodology (v1 lesson: manual validation gets skipped).
- Specs that describe implementation details instead of observable behavior drift immediately and create false authority.
- Test agents that read source code or receive implementation knowledge from the parent agent produce implementation-coupled tests.
