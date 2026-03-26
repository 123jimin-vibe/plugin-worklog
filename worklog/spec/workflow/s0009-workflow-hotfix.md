+++
id = "s0009"
title = "Workflow: Hotfix"
tags = ["workflow", "methodology"]
+++

# Workflow: Hotfix

Urgent fix with compressed process.

## Flow

1. **Incident detected**.
2. **Create task** — minimal triage, rapid fix.
3. **Fix and deploy**.
4. **Create decision** (mandatory) — post-mortem: root cause, what went wrong, what was accepted as tech debt.
5. **Create follow-up task(s)** if tech debt introduced or cleanup needed.
6. **Archive task**.

Branches:
- First fix doesn't resolve → multiple iterations under time pressure.
- Hotfix introduces regression → rollback or patch.
- Tech debt accepted for speed → follow-up task to clean up.
- Hotfix bypasses normal review → decision documents why.

## Forbidden

- Hotfix without a post-mortem decision record.
- Hotfix used as precedent to bypass process for non-emergencies.

## Anticipated Changes

- Formal bounds on which process steps can be skipped during hotfix.

## Dangers

- Post-mortem decision record skipped because the fix is already deployed.
- Hotfix precedent used to cut corners on subsequent non-urgent work.
