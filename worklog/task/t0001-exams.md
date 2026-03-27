+++
id = "t0001"
title = "Implement initial exams for entity specs"
tags = ["quality"]
status = "active"
modifies = ["s0014"]
+++

# Implement initial exams for entity specs

Create two exams — one happy-path, one pitfall-focused — to verify that LLMs follow the entity specs correctly.

## Scope

- **Example project:** a small fictional project (specs, tasks, decisions) provided as context alongside the spec under test. Gives the LLM a concrete worklog to reason about rather than abstract rules.
- **Happy-path exam:** question groups that test correct behavior — creating entities, updating status, following lifecycle, respecting precedence.
- **Pitfall exam:** question groups that probe known failure modes — over-specification, TODO markers skipped, archive without decision, spec-code conflict resolution.

Each exam is a TOML config for prompt-engineer:invoke-llm per s0014. Questions are grouped by topic within each exam.

## System prompt

SKILL.md — that's what agents actually receive. If SKILL.md doesn't convey entity rules well enough, we want to find out.

## Directory structure

```
exams/
└── entity/
    ├── context.md           # fictional project worklog state
    ├── happy-path.toml
    ├── pitfalls.toml
    └── results/             # gitignored output
```

## TOML structure

Both exams share the same shape. SKILL.md as system prompt, project context injected via `[vars]`, questions as a user prompt array.

```toml
[generation]
model = "claude-sonnet-4-6"
temperature = 0.0

[vars]
project = "context.md"

[[prompts]]
role = "system"
file = "../../plugin/skills/worklog/SKILL.md"

[[prompts]]
role = "system"
prompt = "You are working on the following project:\n\n{{project}}"
substitute = true

[[prompts]]
role = "user"
prompt = [...]

[output]
file = "results/<exam>-results.jsonl"
```

## Example project (context.md)

A fictional "recipe app" worklog:

- **s0001** — Recipe storage (paths: `src/recipes/**`). Has a TODO for batch import.
- **s0002** — Notification system (paths: `src/notify/**`).
- **t0001** — Add recipe tagging (modifies s0001, status: active).
- **t0002** — Fix email delivery bug (modifies s0002, status: done, still in task/ not archived).
- **t0003** — Hotfix: rate limiter bypass (modifies s0002, status: done, archived).
- **d0001** — Post-mortem for t0003 hotfix (relates_to: s0002).

