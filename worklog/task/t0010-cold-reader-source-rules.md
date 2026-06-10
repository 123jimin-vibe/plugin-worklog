+++
id = "t0010"
title = "Cold-reader rules for comments and naming"
tags = ["methodology"]
status = "pending"
modifies = ["s0001", "s0018"]
+++

# Cold-reader rules for comments and naming

While inside a task, agents narrate its context into code: comments restate spec/task content, and names lean on ambient domain context that doesn't travel (new.r-g.kr t0012: comment trim plus catalog→i18n-catalog rename; that project had to add "comments should be concise" to AGENTS.md because the methodology says nothing).

## Scope

Add to s0001 key rules and SKILL.md task rules, under one shared principle — everything written is read without the author's context:

- Comments say what the code cannot (why, invariants, non-obvious constraints). Behavior and rationale live in specs/decisions — reference the ID instead of restating. No task history or process narration in code.
- Public names must be unambiguous where they are imported, without the defining module's context. Carry the domain in the name; prefer the governing spec's vocabulary.

## Constraints

- No concrete naming examples in rule text — agents latch onto the example's incidental scheme (casing, prefixes) as the rule.
- Wording per s0021; existing exams as regression net.
