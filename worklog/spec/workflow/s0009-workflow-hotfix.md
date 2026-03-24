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

## Methodology Evaluation

Potential agent mistakes:
- Skips the post-mortem decision record because the fix is already deployed.
- Uses hotfix precedent to cut corners on subsequent non-urgent work.

Gaps:
- No urgency marker on tasks — a hotfix task looks identical to a normal task in the worklog.
- The "bypass normal process" exception isn't formally bounded — which steps can be skipped?

Tooling/hooks:
- Hook: hotfix tasks require a linked decision record before archiving.
