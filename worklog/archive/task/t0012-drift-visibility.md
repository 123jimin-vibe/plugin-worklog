+++
id = "t0012"
title = "drift.py: report what it cannot check"
tags = ["tooling"]
status = "done"
modifies = ["s0010"]
+++

# drift.py: report what it cannot check

drift.py silently skips specs without `paths` and specs not yet committed, and diffs `commit..HEAD` so working-tree changes are invisible. Silence reads as "no drift."

## Scope

- Report skipped specs explicitly: no `paths` (unmonitored) and absent from git history (unverifiable).
- Include uncommitted working-tree changes in the comparison.
- Document the watermark limitation in s0010: any spec edit resets the baseline, even a typo fix.
- Tests before implementation (s0017).

## Outcome

drift.py now diffs each spec's last commit against the working tree (uncommitted changes count as drift) and reports specs it cannot check — no `paths` (unmonitored) or not yet committed (unverifiable) — on stderr, so an empty stdout no longer reads as "all clean." The actionable drift list stays on stdout (exit 1). Git logic factored into `lib/gitdrift.py`, shared with archive.py (t0008). Watermark limitation recorded in s0010 Dangers. Tests added: working-tree drift, stderr coverage reporting; the existing drift tests still pass under the new stdout/stderr split.
