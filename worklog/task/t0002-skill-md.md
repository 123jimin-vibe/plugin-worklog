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
