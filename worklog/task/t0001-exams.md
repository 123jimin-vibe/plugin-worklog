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

## Happy-path questions

### Creation & lifecycle

"The team wants to track a new 'user accounts' feature. No spec exists yet. Create the spec file with full content including frontmatter. Source code will live under src/accounts/."
Expected: correct TOML frontmatter (s0003), paths glob, observable-behavior body, anticipated changes, dangers.

"A new requirement came in: add push notifications. Create a task for it, then walk through what happens when the task is finished."
Expected: new task with modifies s0002, status pending. On completion: status to done, move to archive/task/, verify governing spec still consistent.

### Relationships & precedence

"You need to update recipe search to use tags, but that depends on t0001 finishing first. Create the task. Also, while reviewing the codebase you notice src/notify/email.ts retries failed sends 5 times, but spec s0002 says the retry limit is 3. How do you handle both situations?"
Expected: task with blocked_by = ["t0001"], modifies = ["s0001"], status blocked. For the conflict: spec takes precedence, code diverges = bug in code.

### Decisions

"The team decides to switch from email to webhooks for the notification system. Record this decision and explain what happens next to the affected spec."
Expected: decision record with context, choice, rationale, consequences, relates_to = ["s0002"]. Spec update requires separate user approval — the decision does not authorize the change by itself.

## Pitfall questions

### Spec discipline

"Write a spec for a new caching layer. The cache should use Redis with a 5-minute TTL. The CacheManager class should expose get(), set(), and invalidate() methods."
Expected: refuses to include implementation details (Redis, TTL value, class name, method signatures). Describes observable behavior only.

"You just finished implementing batch recipe import as part of task t0001. Spec s0001 has a TODO for batch import. Meanwhile, you're reviewing code and it handles an edge case elegantly that the spec doesn't mention. What do you do about each?"
Expected: remove the TODO (implemented). For the undocumented behavior: surface discrepancy to user, do not silently update spec.

### Entity integrity

"Decision d0001 has a factual error — it says the incident happened on March 3 but it was actually March 5. How do you correct it?"
Expected: supersede with a new decision. Decisions are never edited.

"Task t0003 was a hotfix and it's done. The file is already in archive/task/. Is anything missing?"
Expected: checks for a linked decision record (post-mortem). d0001 exists — nothing missing. Tests whether the LLM checks rather than assumes.

"You're about to start work on t0001, and separately you need to create a chore task to rename variables in src/recipes/ for consistency with no behavior changes. Walk through both."
Expected: first thing for t0001 is set status to active. For the chore: src/recipes/ is governed by s0001, so modifies = ["s0001"] even though behavior doesn't change — the work touches spec-governed files.
