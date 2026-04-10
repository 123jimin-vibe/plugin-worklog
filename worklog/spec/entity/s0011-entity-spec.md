+++
id = "s0011"
title = "Entity: Spec"
tags = ["entity", "methodology"]
+++

# Entity: Spec

A kept-up-to-date design reference. Defines observable behavior, constraints, anticipated changes, and dangers for a bounded area of the project.

## Location

`worklog/spec/` — may be organized into subdirectories by topic.

## Frontmatter

TOML fenced with `+++`. Required fields:

| Field   | Type       | Description                                         |
|---------|------------|-----------------------------------------------------|
| `id`    | string     | Unique identifier, format `s` + digits (e.g. `s0001`). |
| `title` | string     | Human-readable name.                                |
| `tags`  | string[]   | Classification (e.g. `core`, `workflow`, `entity`). |
| `paths` | string[]   | Glob patterns for governed source files (see below). |
| `parent`| string     | ID of the parent spec (e.g. `"s0003"`). Optional.    |

`paths` is used by drift detection. Optional — omit when spec governs no source files (e.g. methodology, workflow). Prefer broad globs (`src/auth/**`) over enumerating individual files. When a source file is governed by a spec, annotate it with a `@worklog` comment (e.g. `// @worklog s0001`) to create a reverse link.

<!-- NOTE: `@worklog` markers saw low adoption in bfc (1 of ~40 files). Needs enforcement to be viable: (1) automated injection via post-commit hook or script; (2) a `which-spec <file>` query tool for discoverability without source modification; (3) validation script flagging governed files missing markers. -->

## Required Sections

1. Top-level heading matching `title`.
2. Body describing observable behavior — inputs, outputs, observable effects, ordering guarantees. Written from a consumer's perspective, not implementation.
3. **Constraints** — invariants, limits, and rules that must always or never hold.
4. **Anticipated Changes** — known future work or likely evolution. Informational only — must be promoted to a behavioral section (marked `UNIMPLEMENTED`) or a task before work begins.
5. **Dangers** — risks, pitfalls, or failure modes to watch for.

Optional section: **Proposals** — items discussed but not approved by the user. Distinct from Anticipated Changes (which are observations about likely evolution, not items from conversation). When approved, promote to a behavioral section marked `UNIMPLEMENTED`.

Sections beyond these are discretionary. Approved items without backing implementation must be marked `UNIMPLEMENTED`. Unapproved items belong in Proposals, not behavioral sections.

## Creation

1. Survey existing specs for overlap — default to extending an existing spec rather than creating a new one.
2. Draft: observable behavior, constraints, dangers.
3. User reviews. Approved items without implementation are marked `UNIMPLEMENTED`. Unapproved items move to Proposals or are removed.

## Updating

Triggers: implementation reveals adjustments, drift detected, component boundaries changed, stale reference discovered.

- Structural updates (`paths`, section reorganization, wording clarity) are free.
- Behavioral updates (changing what the system does) require user approval.

Trivial edits (typos, wording) do not require a task.

## Deletion

When: spec is superseded by a newer spec, or the governed feature was removed. Requires a decision record.

## Forbidden

- Delete without a decision record explaining why.
- Archive. Specs have no status lifecycle.
- Present unapproved or speculative content as decided. Discussion ≠ approval.
- Implementation details (API signatures, class names, concrete technology choices, file paths, version numbers, directory layouts) in spec body. (`paths` frontmatter uses globs for drift detection — the only place file references belong.)

## Anticipated Changes

- Spec-by-ID cross-referencing to replace fragile relative paths.
- Convention for specs delegating behavioral details to reference docs.
- Distinguishing governance paths from behavioral-extension paths in `paths`.

## Dangers

See s0019 (Agent Pitfalls).
