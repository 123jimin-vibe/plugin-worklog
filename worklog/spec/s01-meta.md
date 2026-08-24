+++
id = "s01"
title = "Meta-spec for this project"
paths = ["worklog/spec/**/*.md"]
+++

- This governs this project's specs.
- Changing s01 requires explicit user approval.

## Worklog

- It is a durable record of the project's intent, shared by humans and agents working on it.
- It consists of multiple types of entities, including specs (authoritative behaviors) and tasks (each one unit of work).

## Plugin

- It is this project's deliverable.
- It is an [agent skill](https://agentskills.io/specification) for AI agents to develop software via worklog.
- Whether a project uses worklog is that project's choice, never the plugin's.
- It should be harness-agnostic.