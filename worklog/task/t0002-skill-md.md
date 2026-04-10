+++
id = "t0002"
title = "Write first proper SKILL.md"
tags = ["methodology"]
status = "active"
modifies = ["s0001", "s0018"]
+++

# Write first proper SKILL.md

Current `plugin/skills/worklog/SKILL.md` is a placeholder. Devise the first proper edition that accurately reflects the current state of the methodology specs.

SKILL.md is the single authoritative file that agents receive. It must be:

- Consistent with s0001 (methodology), s0011–s0013 (entities), s0014–s0016 (supporting entities).
- Informed by s0019 (agent pitfalls) — every Must/High severity pitfall should have a covering rule.
- Concise — context-file-effectiveness research shows verbose context hurts agent performance.
- Complete enough that an agent can operate from SKILL.md alone without reading individual specs.

## Structure

Old SKILL.md had 9 top-level sections. New structure collapses to 4 by co-locating rules with the entities they govern.

```
# Worklog
  One-liner philosophy. Root dir. Init instructions.

## Entities
  ID format, filename, TOML frontmatter fence.

  ### Spec
    Fields, lifecycle, paths/drift detection.
    "Not implementation details" constraint.
    Precedence rules (spec > code > tests; ask user if spec seems wrong).

  ### Task
    Fields, status lifecycle, archival.
    Workflows table (greenfield, bugfix, refactor, investigation, chore, hotfix).
    Execution rules: tests before impl, test isolation, survey before building,
      approval, surface ambiguity, escalate when stuck, no antipatterns.
    Forbidden actions list.

  ### Decision
    Fields, immutability, supersession.
    "Record decisions" rule.

  ### Relationships
    Forward-link table. Reverse via grep.

## Scripts
  Table of scripts + invocation pattern.

## Workflows
  Summary table only (name → flow → key constraint).
```

### Design rationale

- **Relationships / Precedence / Drift** — folded into the entity subsection they bind (Spec for precedence and drift, each entity for its own links).
- **Rules / Forbidden** — distributed into the entity they most naturally govern (mostly Task). Reduces cross-referencing when an agent asks "how do I handle a task."
- **Workflows** — kept as top-level but table-only; key constraints already stated under entities.

## Changes already applied

These SKILL.md edits were made during the UNIMPLEMENTED marker migration:

- `TODO` marker → `UNIMPLEMENTED` (spec line 31, stubs rule line 66).
- Added Proposals section mention (line 31).
- Added "Spec is authoritative regardless of UNIMPLEMENTED markers" (line 31).

## Remaining pitfall gaps

Rules missing from SKILL.md, mapped to s0019 pitfalls. Each needs a covering rule added:

| Pitfall | Gap | Proposed rule |
|---------|-----|---------------|
| S3 | No "check related specs" rule | Before updating a spec, check specs with overlapping tags or paths for contradictions. |
| S4 | No "prefer extending" rule | Default to extending an existing spec rather than creating a new one. |
| S6 | Approval rule doesn't cover spec creation | Write only what the user described or approved. Every behavioral item in a spec is a binding requirement — do not add speculative detail. Unapproved ideas go in Proposals. |
| T1 | No "maintain status" rule | Set status to active when starting work, done when finishing. |
| T6 | No "remove markers" rule | When implementation completes an UNIMPLEMENTED item, remove the marker from the spec. |
| X4 | No "don't modify specs inline" rule | Do not modify spec behavioral content during task implementation without going through the approval flow. |
| X6 | No "use worklog as planning" rule | Use task and spec files as the planning medium. Do not duplicate planning in external tools. |
