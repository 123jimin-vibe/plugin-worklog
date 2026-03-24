+++
id = "s0003"
title = "Design Research & Case Studies"
tags = ["research"]
paths = ["brainstorm/**"]
+++

# Design Research & Case Studies

The `brainstorm/` directory contains design rationale, empirical observations, and prior-art research that inform the worklog methodology. This material is not part of the deliverable — it is the evidence base behind design decisions in s0001.

## Contents

- **Design rationale** — constraints, goals, and trade-off analysis for the methodology's structure (entity types, spec representation, workflow definitions).
- **Pitfall catalog** — documented AI agent failure modes that the methodology aims to prevent.
- **Case studies** — observations from applying the methodology to real projects, capturing what worked, what didn't, and structural friction.
- **Prior art** — external references and research on related approaches (ADRs, context file effectiveness, development paradigms).

## Relationship to Methodology

Research findings flow into SKILL.md via iterative revision. Case study observations surface problems; methodology changes address them. The brainstorm directory is append-friendly — new observations and studies are added over time; existing entries are updated when findings are refined.

## Anticipated Changes

- New case studies as the methodology is applied to additional projects.
- Consolidation of findings into actionable methodology changes.

## Dangers

- Stale research that contradicts current SKILL.md creates confusion about which is authoritative. SKILL.md always wins (see s0001 precedence rules).
