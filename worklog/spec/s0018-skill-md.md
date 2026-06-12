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

1. **Worklog** — one-line philosophy, root directory, init instruction.
2. **Entities** — ID format, filename convention, frontmatter fence. One subsection per entity type, each carrying the rules that govern it:
   - **Spec** — fields, required sections, `UNIMPLEMENTED` markers, `paths`, precedence, drift detection.
   - **Task** — fields, lifecycle, archiving (including stub honesty), execution rules, forbidden list.
   - **Decision** — fields, immutability, supersession.
   - **Relationships** — forward links, reverse-via-grep rule.
3. **Scripts** — table of scripts with flags and purpose.
4. **Workflows** — summary table (name, flow, key constraint). No full flowcharts.

Rules and forbidden lists are co-located with the entity they most naturally govern, not kept as separate top-level sections.

## Source Mapping

Each section traces to source specs:

| SKILL.md section | Source specs |
|------------------|-------------|
| Worklog | s0001 |
| Entities: Spec | s0011; s0001 (precedence, drift detection) |
| Entities: Task | s0012; s0001, s0017 (rules); s0004–s0009 (forbidden) |
| Entities: Decision | s0013 |
| Entities: Relationships | s0001 |
| Scripts | s0010 |
| Workflows | s0004–s0009 |

Rules across sections are additionally informed by s0019 — every Must/High severity pitfall carries a covering rule.

When a source spec changes, the corresponding SKILL.md section must be reviewed.

## Composition Principles

- **Concise over complete.** Verbose context hurts agent performance. Prefer terse rules over explanatory prose.
- **Actionable over informational.** Anticipated Changes and Dangers from specs are omitted — they inform spec authors, not working agents.
- **Flat over nested.** Minimize heading depth. Agents scan better than they parse hierarchy.
- **`UNIMPLEMENTED` markers propagate.** If a spec `UNIMPLEMENTED` item affects agent behavior, it appears in SKILL.md. Internal spec items (governance, tooling plans) stay in specs.

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
