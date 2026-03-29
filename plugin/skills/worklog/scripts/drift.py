# @worklog s0010
"""Report specs whose governed source files changed after the spec was last touched."""

import argparse
import pathlib
import subprocess
import sys

from lib.discover import discover_entities


def _git(cwd, *args):
    """Run a git command and return CompletedProcess."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd, capture_output=True, text=True,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect spec-code drift.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)

    # Find git repo root.
    repo_result = _git(str(root), "rev-parse", "--show-toplevel")
    if repo_result.returncode != 0:
        print("Not inside a git repository.", file=sys.stderr)
        raise SystemExit(1)
    repo_root = repo_result.stdout.strip()

    store = discover_entities(root)
    drifted = []

    for spec in store.specs:
        paths = spec.fields.get("paths", [])
        if not paths:
            continue

        # Last commit that touched the spec file.
        log_result = _git(repo_root, "log", "-1", "--format=%H", "--", str(spec.path))
        commit = log_result.stdout.strip()
        if not commit:
            continue

        # Check for changes to governed files since that commit.
        diff_result = _git(repo_root, "diff", f"{commit}..HEAD", "--", *paths)
        if diff_result.stdout.strip():
            drifted.append(spec)

    if not drifted:
        raise SystemExit(0)

    for spec in drifted:
        print(f"{spec.id}  {spec.title}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
