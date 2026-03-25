+++
id = "s0009"
title = "Workflow: Hotfix"
tags = ["workflow"]
+++

# Workflow: Hotfix

Urgent fix with fewer steps.

## Flow

1. Incident detected.
2. Task (create) — minimal triage, rapid fix.
3. Fix deployed.
4. Decision (create, mandatory) — post-mortem: root cause, what went wrong.
5. Follow-up task(s) (create) if tech debt introduced or cleanup needed.
6. Task (archive). Normal process resumes.

Branches:
- First fix doesn't resolve → multiple iterations under time pressure.
- Hotfix introduces regression → rollback or patch.
- Tech debt accepted for speed → follow-up task (create) to clean up.
- Hotfix bypasses normal review → decision (create) documents why.

## Forbidden

- Hotfix without a post-mortem decision record.
- Hotfix used as precedent to bypass process for non-emergencies.

## Anticipated Changes

- Urgency marker on tasks to distinguish hotfix from normal tasks.
- Formal bounds on which process steps can be skipped during hotfix.
- TODO: Hook — hotfix tasks require a linked decision record before archiving.

## Dangers

- Post-mortem decision record skipped because the fix is already deployed.
- Hotfix precedent used to cut corners on subsequent non-urgent work.
