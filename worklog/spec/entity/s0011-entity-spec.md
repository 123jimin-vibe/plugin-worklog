+++
id = "s0011"
title = "Entity: Spec"
tags = ["entity"]
paths = ["worklog/spec/**"]
+++

# Entity: Spec

A kept-up-to-date design reference. Defines observable behavior, constraints, anticipated changes, and dangers for a bounded area of the project.

## Location

`worklog/spec/` — may be organized into subdirectories by topic.

## Frontmatter

TOML fenced with `+++`. Required fields:

| Field   | Type       | Description                                         |
|---------|------------|-----------------------------------------------------|
| `id`    | string     | Unique identifier, format `sNNNN`.                  |
| `title` | string     | Human-readable name.                                |
| `tags`  | string[]   | Classification (e.g. `core`, `workflow`, `entity`). |
| `paths` | string[]   | Glob patterns for governed source files (see below). |

`paths` is used by drift detection. Optional — omit when spec governs no source files (e.g. methodology, workflow). Prefer broad globs (`src/auth/**`) over enumerating individual files. When a source file is governed by a spec, annotate it with a `@worklog` comment (e.g. `// @worklog s0001`) to create a reverse link.

## Required Sections

1. Top-level heading matching `title`.
2. Body describing observable behavior and constraints.
3. **Anticipated Changes** — known future work or likely evolution.
4. **Dangers** — risks, pitfalls, or failure modes the agent must watch for.

Sections beyond these are discretionary and topic-dependent. Unapproved or planned items must be marked `TODO`. Do not present speculative content as decided.

## Relationships

| Direction | Relationship         | Target        |
|-----------|----------------------|---------------|
| Outbound  | `paths`              | Source files   |
| Inbound   | `task.modifies`      | Task           |
| Inbound   | `decision.relates_to`| Decision       |

Inbound relationships are not stored on the spec. Reverse lookup via grep.

## Allowed Actions

| Action | When |
|--------|------|
| Create | New area of behavior needs governing. Default to extending an existing spec; create only when the behavior is clearly independent. |
| Update | Implementation reveals adjustments, gap found, component boundaries changed, stale reference discovered. Trivial edits (typos, wording) do not require a task. |
| Delete | Spec is superseded by a newer spec, or the governed feature was removed. Requires a decision record. |

Structural updates (`paths` after a file move, section reorganization, wording clarity) are freely allowed. Updates that change prescribed observable behavior require user approval.

## Forbidden Actions

- Delete without a decision record explaining why.
- Archive. Specs have no status lifecycle.
- Modify observable behavior without user approval.
- Implementation details (API signatures, file paths, version numbers, directory layouts) in spec body.

## Precedence

1. Spec over source code — divergence is a bug in code.
2. Spec over tests — tests derive from spec.
3. Spec suspected wrong — ask user, never silently override.

## Drift Detection

Compares the spec's last-touched date (via git log) against changes to files matching its `paths` globs. If source changed after spec, the spec may be stale.

## Anticipated Changes

- Spec-by-ID cross-referencing to replace fragile relative paths.
- Convention for specs delegating behavioral details to reference docs.
- Distinguishing governance paths from behavioral-extension paths in `paths`.

## Dangers

- Over-granular specs (one per function) fragment governance — prefer extending an existing spec.
- Specs without `paths` escape drift detection silently.
- Append-only growth — agents add content but never prune obsolete material. Specs grow monotonically and eventually contradict themselves.
- Overlapping `paths` across specs creates ambiguous drift signals — unclear which spec is stale when a shared file changes.
- A spec update can silently contradict another spec. Check related specs (via shared `tags` or overlapping `paths`) when making non-trivial updates.
- Reference docs cited by a spec become part of its behavioral surface but escape drift detection.
