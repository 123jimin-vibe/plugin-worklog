+++
id = "t0001"
title = "Implement initial exams for entity specs"
tags = ["quality"]
status = "pending"
modifies = ["s0014"]
+++

# Implement initial exams for entity specs

Create two exams — one happy-path, one pitfall-focused — to verify that LLMs follow the entity specs correctly.

## Scope

- **Example project:** a small fictional project (specs, tasks, decisions) provided as context alongside the spec under test. Gives the LLM a concrete worklog to reason about rather than abstract rules.
- **Happy-path exam:** question groups that test correct behavior — creating entities, updating status, following lifecycle, respecting precedence.
- **Pitfall exam:** question groups that probe known failure modes — over-specification, TODO markers skipped, archive without decision, spec-code conflict resolution.

Each exam is a TOML config for prompt-engineer:invoke-llm per s0014. Questions are grouped by topic within each exam.
