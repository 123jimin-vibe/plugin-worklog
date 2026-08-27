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
- Self-descriptiveness is desirable: worklog’s directory structure and files SHOULD contain enough in-band guidance for humans and agents without prior worklog knowledge or plugin access to discover the governing entities, interpret their fields and authority, and follow the applicable rules.
  - At minimum, this SHOULD support correct read-only use, including recognizing when content must not be modified.
  - Where modification is permitted, the files SHOULD also provide enough guidance to make safe changes without plugin assistance.
  - Machine-readable files SHOULD use comments or equivalent in-band documentation to explain important fields whose meaning is not self-evident.

## Plugin

- It is this project's deliverable.
- It is an [agent skill](https://agentskills.io/specification) for AI agents to develop software via worklog.
- Whether a project uses worklog is that project's choice, never the plugin's.
- It should be harness-agnostic.
- Plugin users, including agents, MUST be assumed unable to access any repository content outside `plugin/`, including this project's worklog specs and notes.