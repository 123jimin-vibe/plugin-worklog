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
| `paths` | string[]   | Glob patterns for governed source files. Used by drift detection. Optional — omit when spec governs no source files (e.g. methodology, workflow). |

## Required Sections

1. Top-level heading matching `title`.
2. Body describing observable behavior and constraints.
3. **Anticipated Changes** — known future work or likely evolution.
4. **Dangers** — risks, pitfalls, or failure modes the agent must watch for.

Sections beyond these are discretionary and topic-dependent.

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
| Create | New area of behavior needs governing. |
| Update | Implementation reveals adjustments, gap found, component boundaries changed, stale reference discovered. |
| Delete | Spec is superseded by a newer spec, or the governed feature was removed. Requires a decision record. |

## Forbidden Actions

- Delete without a decision record explaining why.
- Archive. Specs have no status lifecycle.
- Modify observable behavior without user approval.

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

- Implementation details in specs drift immediately and create false authority.
- Over-granular specs (one per function) fragment governance — prefer extending an existing spec.
- Specs without `paths` escape drift detection silently.

--------

## Proofread Findings

Unreviewed findings from cross-referencing s0011 against case studies (BFC, prompt-engineer), pitfalls, design sketch (index.md), software architecture principles, and workflow specs (s0004–s0009).

### Flaws Not Addressed by Forbidden / Dangers

1. **Spec modified outside task lifecycle.** Agents edit specs inline during implementation without a task with `modifies` pointing at the spec. s0011 says nothing about this. (Pitfalls: "Lifecycle Bypassed"; BFC: "validation is manual and therefore skipped")

2. **No prohibition on implementation details in spec body.** Dangers says they "drift immediately" — an observation, not a rule. Forbidden doesn't ban them. Agents write API signatures, file paths, version numbers, directory layouts into specs. (Pitfalls: "Specs Over-Specify"; prompt-engineer: version drift, script path mismatch, "Structure" section listing directories)

3. **`paths` as enumerated files instead of globs.** Agents list `["plugin/lib/foo.py", "plugin/lib/bar.py"]` instead of `["plugin/lib/**"]`. Brittle — adding a file requires updating the spec. Not mentioned anywhere in s0011. (prompt-engineer observation)

4. **`paths` overlap between multiple specs.** Two specs both claiming `plugin/lib/**` is structurally valid but drift detection can't know which spec to flag. Not in Dangers. (prompt-engineer: "`paths` conflates ownership with relevance")

5. **No conciseness constraint.** Design sketch says "Concise files. No padding, no reiteration. Say it once, precisely." s0011 is silent on this. (index.md constraints)

6. **Append-only accumulation.** Agents add to specs but never remove obsolete content. Specs grow monotonically. Not in Dangers. (Pitfalls: "Append-Only Bias")

7. **Cross-spec consistency.** A spec update can contradict another spec. Nothing in s0011 addresses this. (Pitfalls: "No Self-Consistency across Sessions")

8. **No TODO/WIP marking convention.** Design sketch says "TODO aspects clearly labelled." s0011 Required Sections says nothing about distinguishing approved behavior from planned/unapproved items. (prompt-engineer: "Spec not marked as WIP"; index.md: "items start as TODO")

### Flows an Incompetent Assistant Would Walk Into

1. **Brainstorm → spec as fact.** User says "what if we added X?" Agent creates a complete spec with no TODO markers, no WIP indication, treating discussion as approval.

2. **Edit spec mid-implementation with no task.** Agent hits a snag, tweaks the spec to match what it built, keeps coding. No task references the spec. Lifecycle completely bypassed.

3. **Invert precedence.** Code diverges from spec. Agent "fixes" the spec to match the code instead of treating divergence as a code bug. Silently flips the authority hierarchy.

4. **One spec per function.** Agent creates `s0015-render-table.md` instead of extending the existing lib spec. Fragments governance surface.

5. **Implementation as spec content.** Agent writes "The `parse_config()` function returns a `Dict[str, Any]`" into the spec body. First refactor makes this false; spec now has false authority.

6. **Enumerate files in `paths`.** Agent writes `paths = ["src/auth/login.py", "src/auth/logout.py", "src/auth/session.py"]`. A new `src/auth/refresh.py` is ungoverned.

7. **Silent spec rot.** Agent adds a new section to a spec but never removes the three paragraphs it replaced. Spec contradicts itself internally.

8. **Refactor touches spec behavior.** During refactor, agent updates spec "to reflect new structure" but the structural change masks a behavioral change. No guardrail distinguishes the two.

### Workflows / Actions Not Well Supported

1. **Refactor (s0006).** s0006 explicitly distinguishes structural spec changes (allowed) from behavioral spec changes (forbidden). s0011 has no notion of this distinction — "Update" is one undifferentiated action.

2. **Investigation → spec creation (s0007).** An investigation may produce a draft spec that isn't approved yet. s0011 has no draft/WIP state — a spec is either created or it doesn't exist. No intermediate "proposed" status.

3. **Spec delegation to reference docs.** When a spec says "see reference doc X for details," X becomes part of the spec's behavioral surface. s0011 has no way to express this relationship. Drift detection won't catch reference doc changes. (In Anticipated Changes but the absence is not flagged as a Danger.)

4. **Spec scope decisions.** No guidance on when to create a new spec vs. extend an existing one. This is the single most common agent mistake across both case studies, but s0011 only mentions it as a Danger observation ("over-granular specs") with no actionable rule.
