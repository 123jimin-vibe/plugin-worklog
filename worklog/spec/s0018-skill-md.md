+++
id = "s0018"
title = "SKILL.md Composition"
tags = ["methodology"]
paths = ["plugin/skills/worklog/SKILL.md"]
+++

# SKILL.md Composition

SKILL.md is the single context file agents receive when the worklog skill activates. It must be self-contained: an agent follows the methodology from SKILL.md alone, without reading individual specs.

SKILL.md is a curated summary, not a concatenation of specs. It optimizes for agent consumption — brevity, scanability, and actionable rules.

## Structure

Sections in order:

1. **Worklog** — one-line philosophy and root directory.
2. **Entities** — ID format, filename convention, frontmatter. One subsection per entity type covering fields, lifecycle, and key constraints.
3. **Relationships** — forward-link table and the reverse-via-grep rule.
4. **Precedence** — spec > code > tests, and the ask-user escalation.
5. **Rules** — flat list of behavioral rules for agents.
6. **Forbidden** — flat list of actions agents must never take.
7. **Workflows** — summary table (name, flow, key constraint). No full flowcharts.
8. **Drift Detection** — how to check, what triggers action.
9. **Scripts** — table of available scripts with invocation patterns.

## Source Mapping

Each section traces to source specs:

| SKILL.md section | Source specs |
|------------------|-------------|
| Entities | s0011, s0012, s0013 |
| Relationships | s0001 |
| Precedence | s0001 |
| Rules | s0001, s0017 |
| Forbidden | s0001, s0004–s0009 |
| Workflows | s0004–s0009 |
| Drift Detection | s0001 |
| Scripts | s0010 |

When a source spec changes, the corresponding SKILL.md section must be reviewed.

## Composition Principles

- **Concise over complete.** Verbose context hurts agent performance. Prefer terse rules over explanatory prose.
- **Actionable over informational.** Anticipated Changes and Dangers from specs are omitted — they inform spec authors, not working agents.
- **Flat over nested.** Minimize heading depth. Agents scan better than they parse hierarchy.
- **TODO markers propagate.** If a spec TODO affects agent behavior, it appears in SKILL.md. Internal spec TODOs (governance, tooling plans) stay in specs.

## Updating

Update SKILL.md when:

- An entity spec (s0011–s0013) changes observable behavior.
- A workflow spec (s0004–s0009) changes its flow or forbidden list.
- The methodology spec (s0001) changes rules, precedence, or relationships.
- A script's interface changes or a new script is added (s0010).

Wording-only edits for clarity do not require a task.

## Constraints

- Single file. No includes or multi-file delivery.
- Wrapped in `<skill id=worklog>` tags so agents can distinguish worklog prompts from other loaded context.
- Frontmatter uses YAML `---` fences (plugin convention), not TOML `+++`.

## Anticipated Changes

- Token budget target once empirical data on context size vs. agent performance exists.
- New sections as entity types or tooling capabilities are added.

## Dangers

- Manual sync between specs and SKILL.md drifts silently — no enforcement exists yet.
- Over-condensing loses rules agents need; under-condensing bloats context and degrades performance.
- SKILL.md becoming the de facto spec instead of a derived artifact. Edits should flow from specs to SKILL.md, not the reverse.
