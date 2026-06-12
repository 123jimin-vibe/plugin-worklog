+++
id = "t0011"
title = "Make script location unmistakable in SKILL.md"
tags = ["tooling"]
status = "done"
modifies = ["s0010", "s0018"]
+++

# Make script location unmistakable in SKILL.md

Agents frequently invoke nonexistent `<repo>/worklog/scripts/*` or `<repo>/scripts/*`. SKILL.md states the skill-directory location once, but not saliently enough to override the repo-local habit.

## Scope

- SKILL.md Scripts section: a concrete invocation template and an explicit negative — scripts ship with the plugin; they never exist inside the repo or under `worklog/`.
- Record the same in s0010.
- Pitfall entry belongs to t0016; exam coverage to t0018.

## Outcome

SKILL.md Scripts section rewritten: invocation template (`python ${CLAUDE_SKILL_DIR}/scripts/<script>.py [args] [-w PATH]`) plus the explicit negative (no `<repo>/scripts/`, no `<repo>/worklog/scripts/`). s0010 records the runtime location requirement and cites s0019 X9. Exam evidence pre-fix: baseline/round-2 completion-drift runs invoked invented repo-local paths (`worklog/scripts/archive.py`, `scripts/archive.py`).
