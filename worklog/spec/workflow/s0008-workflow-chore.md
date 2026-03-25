+++
id = "s0008"
title = "Workflow: Chore"
tags = ["workflow", "methodology"]
+++

# Workflow: Chore

Maintenance work: dependencies, CI, tooling, documentation.

## Flow

1. Trigger: security advisory, deprecation, tooling need.
2. Task (create) — assess breaking changes, migration effort.
3. Execute change.
4. Verify: CI green, existing tests pass.
5. Spec (update) if stale reference found as side effect.
6. Task (archive).

Branches:
- Dependency update introduces breaking changes → migration larger than expected.
- Chore reveals outdated spec → spec (update).
- Chore escalates into a feature → spec (create), switch to greenfield workflow.
- Blocked by upstream issue → task (set `blocked_by` or document).

## Forbidden

- Behavioral changes introduced as part of a chore without going through spec/task lifecycle.

## Anticipated Changes

- Trigger/source tracking on tasks (security advisory, deprecation notice).
- Way to express "checked N specs, found M stale" after broad changes.
- TODO: drift.py — identify specs that may be stale after dependency or tooling changes.

## Dangers

- Behavioral changes introduced under "it's just a chore" without spec lifecycle.
- Updated dependencies affecting spec-governed behavior go unchecked.
