# @worklog s0010
"""Git-based spec-to-code drift classification.

Shared by drift.py (reports every spec) and archive.py (checks one task's
governing specs). A spec's drift is measured against its last commit, so any
edit to the spec file — even a typo fix — resets the baseline.
"""

import subprocess


def _git(cwd, *args):
    """Run a git command in *cwd* and return the CompletedProcess."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd, capture_output=True, text=True,
    )


def find_repo_root(path):
    """Return the git repository root containing *path*, or None if not a repo."""
    result = _git(str(path), "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def classify_spec(repo_root, spec):
    """Classify a spec's drift against the files it governs.

    Returns:
        "unmonitored"  — spec declares no ``paths``; nothing to check.
        "unverifiable" — spec has ``paths`` but is not yet in git history,
                         so there is no baseline commit to diff against.
        "drifted"      — governed files changed since the spec's last commit,
                         including uncommitted working-tree changes.
        "clean"        — governed files match the spec's last commit.
    """
    paths = spec.fields.get("paths", [])
    if not paths:
        return "unmonitored"

    log = _git(repo_root, "log", "-1", "--format=%H", "--", str(spec.path))
    commit = log.stdout.strip()
    if not commit:
        return "unverifiable"

    # Diff the spec's last commit against the working tree, so both committed
    # and uncommitted changes to governed files register as drift.
    diff = _git(repo_root, "diff", commit, "--", *paths)
    return "drifted" if diff.stdout.strip() else "clean"
