+++
id = "s0020"
title = "Hook Auto-Approval"
tags = ["tooling"]
paths = ["plugin/hooks/**", "plugin/scripts/**"]
+++

# Hook Auto-Approval

A PreToolUse hook intercepts Bash tool calls whose command string matches the plugin's skill script path pattern. A validator script checks that the command invokes `python` on a `.py` file at exactly `skills/<name>/scripts/<file>.py` under `CLAUDE_PLUGIN_ROOT`. If all checks pass, the hook emits an "allow" decision. If any check fails, it exits silently (no opinion — falls back to manual approval).

## Constraints

- Pessimistic by default — unknown or malformed inputs are never auto-approved.
- No dependencies beyond the Python stdlib (no venv needed).
- The case-statement pre-filter in hooks.json must match only this plugin's cache path.

## Anticipated Changes

- Venv check if the plugin gains pip dependencies.

## Dangers

- An overly broad case pattern could auto-approve commands targeting a different plugin's scripts.
- Silently broken hook (Python error, missing env var) degrades to manual approval — safe but invisible.
