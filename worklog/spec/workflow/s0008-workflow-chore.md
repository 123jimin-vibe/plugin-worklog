+++
id = "s0008"
title = "Workflow: Chore"
tags = ["workflow", "methodology"]
+++

# Workflow: Chore

Maintenance work: dependencies, CI, tooling, documentation.

## Flow

1. **Trigger** — security advisory, deprecation, tooling need.
2. **Create task** — assess scope and breaking changes.
3. **Execute** the change.
4. **Verify** — CI green, existing tests pass.
5. **Check specs** for stale references caused by the change. Update if found.
6. **Archive task**.

Branches:
- Dependency update introduces breaking changes → migration larger than expected.
- Chore reveals outdated spec → update spec.
- Chore escalates into a feature → create spec, switch to greenfield workflow.
- Blocked by upstream issue → set `blocked_by` or document.

## Forbidden

- Behavioral changes introduced as part of a chore without going through spec/task lifecycle.

## Anticipated Changes

- Way to express "checked N specs, found M stale" after broad changes.

## Dangers

- Behavioral changes introduced under "it's just a chore" without spec lifecycle.
- Updated dependencies affecting spec-governed behavior go unchecked.
