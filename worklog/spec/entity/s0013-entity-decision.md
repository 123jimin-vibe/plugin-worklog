+++
id = "s0013"
title = "Entity: Decision"
tags = ["entity", "methodology"]
+++

# Entity: Decision

Permanent record of why a choice was made. Decisions are never edited or archived, only superseded by a new decision.

## Location

`worklog/decision/`

## Frontmatter

TOML fenced with `+++`. Required fields:

| Field        | Type       | Description                                           |
|--------------|------------|-------------------------------------------------------|
| `id`         | string     | Unique identifier, format `d` + digits (e.g. `d0001`). |
| `title`      | string     | Human-readable name.                                  |
| `relates_to` | string[]   | Spec IDs this decision concerns.                      |

Optional fields:

| Field        | Type       | Description                                           |
|--------------|------------|-------------------------------------------------------|
| `tags`       | string[]   | Classification tags. Optional for decisions.          |
| `supersedes` | string[]   | Decision IDs this decision replaces.                  |

## Body

Free-form markdown. Should cover:

- **Context** — what situation prompted the decision.
- **Choice** — what was decided.
- **Rationale** — why this option over alternatives.
- **Consequences** — expected impact, trade-offs accepted.

The rationale records the reasons actually given — by the user or cited evidence. An immutable record must not invent motives.

## Creation

1. Identify the choice being made and why it matters.
2. Write context and options considered.
3. Record the decision and its consequences.
4. Link to affected specs via `relates_to`.

Only action allowed. Decisions are immutable after creation — a decision that needs non-trivial correction is superseded by a new decision. Trivial fixes (typos, formatting, correcting an obvious date) may be edited in place.

Create when: non-trivial choice made, design flaw discovered, requirement changed, cost/benefit abandonment. Not every small choice needs a record — reserve for choices that affect observable behavior or constrain future work.

## Required Creation

A decision record is required (not discretionary) when:

- Refactor abandoned because cost exceeds benefit.

A decision record is recommended (not required) when:

- Task cancelled after significant investment — useful for preserving context.
- Hotfix leads to a design choice (e.g., adding validation to prevent a class of bug). The hotfix itself is not a decision; any preventive measure arising from it may be.

## Forbidden

- Non-trivial edit after creation. Supersede instead. (Trivial fixes — typos, formatting, obvious date corrections — are acceptable.)
- Archive or delete a decision that has not been superseded. Superseded decisions may be archived or deleted.
- Omit `relates_to` — unlinked decisions float free of spec governance and become hard to discover.

## Anticipated Changes

- Structured fields for context/choice/rationale/consequences instead of free-form body.
- Link from decision back to the task that prompted it.

## Dangers

See s0019 (Agent Pitfalls).
