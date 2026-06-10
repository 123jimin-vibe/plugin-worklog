+++
id = "t0011"
title = "Make script location unmistakable in SKILL.md"
tags = ["tooling"]
status = "pending"
modifies = ["s0010", "s0018"]
+++

# Make script location unmistakable in SKILL.md

Agents frequently invoke nonexistent `<repo>/worklog/scripts/*` or `<repo>/scripts/*`. SKILL.md states the skill-directory location once, but not saliently enough to override the repo-local habit.

## Scope

- SKILL.md Scripts section: a concrete invocation template and an explicit negative — scripts ship with the plugin; they never exist inside the repo or under `worklog/`.
- Record the same in s0010.
- Pitfall entry belongs to t0016; exam coverage to t0018.
