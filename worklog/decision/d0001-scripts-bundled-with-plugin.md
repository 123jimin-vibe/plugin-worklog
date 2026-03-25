+++
id = "d0001"
title = "Bundle scripts with the plugin, not the consumer worklog"
relates_to = ["s0010", "s0001"]
+++

## Context

The tooling spec (s0010) anticipated scripts at `worklog/script/` — inside each consumer project's worklog directory. This meant every project adopting the methodology would get its own copy of the scripts.

## Choice

Scripts live at `plugin/skills/worklog/script/`, shipped with the plugin. Consumer projects do not maintain their own copies. Scripts accept `-w PATH` to locate the worklog data directory.

## Rationale

- Scripts are methodology tools, not project data. `validate.py`, `drift.py`, `next-id.py` operate generically on worklog structure — nothing in them is project-specific.
- Single source of truth. Updating a script in the plugin updates it for every consumer. With per-project copies, bug fixes would need propagating to every repo.
- Cleaner boundary. `worklog/` in consumer repos is pure state (specs, tasks, decisions). Mixing executable tooling into the data directory conflates what the plugin provides (behavior) with what the project provides (content).
- The `-w PATH` flag already decouples script location from data location.

## Consequences

- `worklog/script/` in consumer repos is no longer needed for tooling. The directory may still exist in this repo (the plugin's own worklog) but holds no scripts.
- SKILL.md's Root initialization and Scripts section need updating to reflect the new location.
- Drift detection for scripts is now governed by s0010 with `paths = ["plugin/skills/worklog/script/**"]`.
