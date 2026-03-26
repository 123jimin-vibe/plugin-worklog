+++
id = "t0004"
title = "Slim specs and add missing operational detail"
tags = ["methodology"]
status = "done"
modifies = ["s0004", "s0005", "s0006", "s0007", "s0008", "s0009", "s0011", "s0012", "s0013"]
+++

# Slim specs and add missing operational detail

Two problems, one pass: specs are too verbose in some places and silent in others.

## Slim

- Factor repeated patterns (frontmatter conventions, relationship model, forward-only rule) into s0001 and reference by ID instead of restating.
- Remove sections that restate what's already in SKILL.md.
- Compress tables and prose that could be terser.
- Identify which sections are load-bearing vs. padding.

## Add missing operational detail

### Workflows (s0004–s0009)

Current flows only list major entity state changes ("Spec (create) → Task (create) → Implement → Task (archive)"). Missing:

- **Spec drafting loop** — research, draft, user review, revise, re-review. "Spec (create)" is not atomic.
- **Task scoping loop** — break down, estimate feasibility, re-scope before work starts.
- **Spec revision mid-flight** — implementation reveals spec gaps, triggering spec update, which may change test expectations. Currently listed as an exception branch; it's actually a routine inner loop.
- **Approval checkpoints** — s0001 says "explicit approval required" but no workflow specifies where those gates sit.
- **Test-spec feedback loop** — writing tests surfaces spec ambiguities. That loop is invisible in current flows.

### Entity specs (s0011–s0013)

Define fields and allowed actions but not the step-by-step mechanics of how an entity gets created or refined (draft → review → approve → finalize). Need lightweight lifecycle descriptions per entity type.
