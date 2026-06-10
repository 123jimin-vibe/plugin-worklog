+++
id = "t0012"
title = "drift.py: report what it cannot check"
tags = ["tooling"]
status = "pending"
modifies = ["s0010"]
+++

# drift.py: report what it cannot check

drift.py silently skips specs without `paths` and specs not yet committed, and diffs `commit..HEAD` so working-tree changes are invisible. Silence reads as "no drift."

## Scope

- Report skipped specs explicitly: no `paths` (unmonitored) and absent from git history (unverifiable).
- Include uncommitted working-tree changes in the comparison.
- Document the watermark limitation in s0010: any spec edit resets the baseline, even a typo fix.
- Tests before implementation (s0017).
