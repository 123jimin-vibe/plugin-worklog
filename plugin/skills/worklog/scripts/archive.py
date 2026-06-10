# @worklog s0010
"""Archive a completed task, surfacing its governing specs first.

Archiving is the moment to confirm each governed spec reflects the finished
work. This script refuses to archive a task that is not done (or a cancelled
task with no explanation), prints every spec the task modifies in full, and
reports drift on their governed paths — so the spec text is in front of you
before the task leaves the active set. The move happens only with --confirm.
"""

import argparse
import pathlib
import shutil
import subprocess
import sys

from lib.constants import normalize_id
from lib.discover import discover_entities
from lib.gitdrift import classify_spec, find_repo_root


def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def _is_tracked(repo_root, path):
    """True if *path* is tracked by the git repo at *repo_root*."""
    return _git(repo_root, "ls-files", "--error-unmatch", str(path)).returncode == 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="Archive a completed task.")
    parser.add_argument("task_id", help="ID of the task to archive.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    parser.add_argument("--confirm", action="store_true",
                        help="Perform the move (default: report only).")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)
    store = discover_entities(root)
    by_id = {normalize_id(e.id): e for e in store.entities}

    task = by_id.get(normalize_id(args.task_id))
    if task is None:
        print(f"No entity with ID '{args.task_id}'.", file=sys.stderr)
        raise SystemExit(1)
    if task.type != "task":
        print(f"{task.id} is a {task.type}, not a task.", file=sys.stderr)
        raise SystemExit(1)
    if task.archived:
        print(f"{task.id} is already archived.", file=sys.stderr)
        raise SystemExit(0)

    status = task.fields.get("status")
    if status == "cancelled":
        if not task.body.strip():
            print(f"{task.id} is cancelled but has no explanation in its body; "
                  f"add one before archiving.", file=sys.stderr)
            raise SystemExit(1)
    elif status != "done":
        print(f"{task.id} has status '{status}'; only done or cancelled tasks "
              f"are archived.", file=sys.stderr)
        raise SystemExit(1)

    # Surface the governing specs in full — the archive-time consistency check.
    repo_root = find_repo_root(root)
    specs = []
    for ref in task.fields.get("modifies", []):
        spec = by_id.get(normalize_id(ref))
        if spec is None:
            print(f"warning: modifies '{ref}' resolves to no spec.", file=sys.stderr)
            continue
        specs.append(spec)

    if specs:
        for spec in specs:
            print("=" * 70)
            header = f"{spec.id}  {spec.title}    ({spec.path})"
            if repo_root is not None:
                header += f"\ndrift: {classify_spec(repo_root, spec)}"
            print(header)
            print("=" * 70)
            print(spec.path.read_text(encoding="utf-8"))
            print()
        print("Confirm each spec above reflects the finished work.")
    else:
        print(f"{task.id} modifies no specs.")

    if not args.confirm:
        print("\nReport only. Re-run with --confirm to archive.")
        raise SystemExit(0)

    # Move into archive/task, preserving git history when the file is tracked.
    dest_dir = root / "archive" / "task"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / task.path.name

    if repo_root is not None and _is_tracked(repo_root, task.path):
        result = _git(repo_root, "mv", str(task.path), str(dest))
        if result.returncode != 0:
            print(result.stderr, file=sys.stderr)
            raise SystemExit(1)
    else:
        shutil.move(str(task.path), str(dest))

    print(f"Archived {task.id} -> {dest}")


if __name__ == "__main__":
    main()
