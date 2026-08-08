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
   - **Spec** — fields, required sections, `UNIMPLEMENTED` markers, `paths`, register rules, the no-implementation-details rule, the structural-versus-behavioral approval gate, the overlap check that precedes an update, precedence, drift detection.
   - **Task** — fields, lifecycle, archiving as a numbered pipeline (including stub honesty), execution rules, forbidden list.
   - **Decision** — fields, immutability, supersession.
   - **Relationships** — forward links, reverse-via-grep rule.
3. **Scripts** — invocation template and the explicit negative against repo-local script paths, then a table of scripts with flags and purpose.
4. **Workflows** — summary table (name, flow, key constraint). No full flowcharts.

Rules and forbidden lists are co-located with the entity they most naturally govern, not kept as separate top-level sections.

## Source Mapping

Each section traces to source specs:

| SKILL.md section | Source specs |
|------------------|-------------|
| Worklog | s0001 |
| Entities: Spec | s0011; s0001 (precedence, drift detection) |
| Entities: Task | s0012; s0001, s0017 (rules); s0016 (priority); s0004–s0009 (forbidden) |
| Entities: Decision | s0013 |
| Entities: Relationships | s0001 |
| Scripts | s0010; s0016 (backlog view) |
| Workflows | s0004–s0009 |

Rules across sections are additionally informed by s0019 — every Must/High severity pitfall carries a covering rule. s0021 governs the register the artifact is written in; s0014 is the gate every revision passes through.

When a source spec changes, the corresponding SKILL.md section must be reviewed.

## Composition Principles

- **Concise over complete.** Verbose context hurts agent performance. Prefer terse rules over explanatory prose.
- **Actionable over informational.** Anticipated Changes and Dangers from specs are omitted — they inform spec authors, not working agents.
- **Flat over nested.** Minimize heading depth. Agents scan better than they parse hierarchy.
- **`UNIMPLEMENTED` markers propagate.** If a spec `UNIMPLEMENTED` item affects agent behavior, it appears in SKILL.md. Internal spec items (governance, tooling plans) stay in specs.
- **No emphasis.** Bold and italic markup carry no measured performance weight and cost tokens in pairs.
- **Telegraphic register.** The artifact reads as program code in natural language, not prose: articles, copulas, and grammatical scaffolding are dropped wherever the sentence still parses unambiguously. Every condition and qualifier survives — grammar is removed, meaning is not.
- **ASCII connectives.** `->` for a state transition or forward link, `=>` for implication, `!=` and `=` for (non-)equivalence. ASCII rather than the unicode glyphs, which cost several times more in the deployed tokenizer (s0021).
- **Numbered pipelines.** A protocol whose steps must run in order is written as a numbered list, not prose.
- **Measured preventing power.** A clause earns its tokens by preventing its pitfall. A clause that was present while its pitfall fired, that duplicates a rule stated elsewhere in the artifact, or that maps to no catalogued mechanism, is a cut candidate — subject to the verification below.

## Updating

Update SKILL.md when:

- An entity spec (s0011–s0013, s0015, s0016) changes observable behavior.
- A workflow spec (s0004–s0009) changes its flow or forbidden list.
- The methodology spec (s0001) changes rules, precedence, or relationships.
- A script's interface changes or a new script is added (s0010).
- A new Must or High severity pitfall is catalogued (s0019).
- The register guidelines change (s0021).

Wording-only edits for clarity do not require a task.

## Verification

A revision is measured, never assumed — the artifact is a prompt, so its effect on behavior is a false-belief question that only observation answers.

1. Weak-model comprehension probes gate first: the revised wording must parse correctly for a reader weaker than the deployment model. A register change that a weak reader misparses is reverted regardless of its token saving.
2. The exam suite (s0014) runs against stored baselines captured on the same exam files as the prior revision. A verdict measured against a baseline captured on older exam files is unattributable.
3. Each change is a separately identifiable lever, and each lever names the questions watching it. A verdict regression or worse failure shape on a lever's watching questions, attributable to that lever, reverts that lever; other levers stand.

Levers stay separable so a regression can be bisected. Tail-end edits made after the last measured run are forbidden — they ship unverified.

## Constraints

- Single file. No includes or multi-file delivery.
- Wrapped in `<skill id=worklog>` tags so agents can distinguish worklog prompts from other loaded context.
- Frontmatter uses YAML `---` fences (plugin convention), not TOML `+++`.

## Proposals

- Reconciling self-containment with measured preventing power. A rule a source spec asserts but the artifact omits is unreachable by consuming agents, yet the cut criterion above can retire a rule the source spec still binds. Undecided: whether an omission obliges retiring the source rule, or whether a source spec may hold rules the artifact deliberately does not ship.

## Anticipated Changes

- Token budget target. Campaign measurements now exist; no budget is set.
- New sections as entity types or tooling capabilities are added.

## Dangers

- A spec rule that never reaches SKILL.md is invisible to drift detection: the watermark only compares the artifact against s0018, never a source spec against the artifact.
- Over-condensing loses rules agents need; under-condensing bloats context and degrades performance.
- SKILL.md becoming the de facto spec instead of a derived artifact. Edits should flow from specs to SKILL.md, not the reverse.
