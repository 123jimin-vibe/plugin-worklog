+++
id = "s0001"
title = "Meta-spec for this project"
paths = ["worklog/spec/**/*.md"]
agent_mode = "read_only"
+++

- This governs this project's specs.

## Worklog

- It is a durable record of the project's intent, shared by humans and agents working on it.
- It consists of multiple types of entities, including specs (authoritative behaviors) and tasks (each one unit of work).
- It supports varying human involvement across development stages, from review of every entity and code change to fully autonomous agentic development.

## Plugin

- It is this project's deliverable.
- It is an [agent skill](https://agentskills.io/specification) for AI agents to develop software via worklog.
- Whether a project uses worklog is that project's choice, never the plugin's.
- It should be harness-agnostic.