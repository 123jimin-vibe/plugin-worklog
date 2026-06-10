# @worklog s0010
"""Archive one or more completed tasks, surfacing their governing specs first.

Archiving is the moment to confirm each governed spec reflects the finished
work. This script refuses to archive a task that is not done (or a cancelled
task with no explanation), prints every spec the task(s) modify in full, and
reports drift on their governed paths — so the spec text is in front of you
before the tasks leave the active set. The move happens only with --confirm.

With several task IDs the gate is atomic: if any task cannot be archived,
nothing is moved. Specs shared across the batch are surfaced once.
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


def _gate(task, raw):
    """Classify whether *task* (resolved from *raw*) can be archived.

    Returns (kind, message): kind is "error" (fatal — abort the batch), "skip"
    (already archived — drop it but proceed), or None (ready to archive).
    """
    if task is None:
        return "error", f"No entity with ID '{raw}'."
    if task.type != "task":
        return "error", f"{task.id} is a {task.type}, not a task."
    if task.archived:
        return "skip", f"{task.id} is already archived; skipping."
    status = task.fields.get("status")
    if status == "cancelled" and not task.body.strip():
        return "error", (f"{task.id} is cancelled but has no explanation in its "
                         f"body; add one before archiving.")
    if status not in ("done", "cancelled"):
        return "error", (f"{task.id} has status '{status}'; only done or cancelled "
                         f"tasks are archived.")
    return None, None


def main(argv=None):
    parser = argparse.ArgumentParser(description="Archive completed task(s).")
    parser.add_argument("task_ids", nargs="+", metavar="task-id",
                        help="ID(s) of the task(s) to archive.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    parser.add_argument("--confirm", action="store_true",
                        help="Perform the move (default: report only).")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)
    store = discover_entities(root)
    by_id = {normalize_id(e.id): e for e in store.entities}
    repo_root = find_repo_root(root)

    # Resolve and gate every task before touching anything (atomic batch).
    tasks, errors, skips, seen = [], [], [], set()
    for raw in args.task_ids:
        nid = normalize_id(raw)
        if nid in seen:
            continue  # collapse duplicate IDs
        seen.add(nid)
        kind, message = _gate(by_id.get(nid), raw)
        if kind == "error":
            errors.append(message)
        elif kind == "skip":
            skips.append(message)
        else:
            tasks.append(by_id[nid])

    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        raise SystemExit(1)
    for message in skips:
        print(message, file=sys.stderr)
    if not tasks:
        print("No tasks to archive.")
        raise SystemExit(0)

    # Surface governing specs, deduplicated across the batch, in full.
    spec_tasks = {}  # spec id -> [spec, [task ids]]
    order = []
    no_spec_tasks = []
    for task in tasks:
        modifies = task.fields.get("modifies", [])
        if not modifies:
            no_spec_tasks.append(task.id)
        for ref in modifies:
            spec = by_id.get(normalize_id(ref))
            if spec is None:
                print(f"warning: {task.id} modifies '{ref}' which resolves to "
                      f"no spec.", file=sys.stderr)
                continue
            if spec.id not in spec_tasks:
                spec_tasks[spec.id] = [spec, []]
                order.append(spec.id)
            spec_tasks[spec.id][1].append(task.id)

    print(f"Archiving {len(tasks)} task(s): {', '.join(t.id for t in tasks)}\n")
    for spec_id in order:
        spec, tids = spec_tasks[spec_id]
        print("=" * 70)
        header = f"{spec.id}  {spec.title}    ({spec.path})    [{', '.join(tids)}]"
        if repo_root is not None:
            header += f"\ndrift: {classify_spec(repo_root, spec)}"
        print(header)
        print("=" * 70)
        print(spec.path.read_text(encoding="utf-8"))
        print()
    for tid in no_spec_tasks:
        print(f"{tid} modifies no specs.")
    if order:
        print("\nConfirm each spec above reflects the finished work.")

    if not args.confirm:
        print("\nReport only. Re-run with --confirm to archive.")
        raise SystemExit(0)

    # Move each task into archive/task, preserving git history when tracked.
    dest_dir = root / "archive" / "task"
    dest_dir.mkdir(parents=True, exist_ok=True)
    move_errors = []
    for task in tasks:
        dest = dest_dir / task.path.name
        if repo_root is not None and _is_tracked(repo_root, task.path):
            result = _git(repo_root, "mv", str(task.path), str(dest))
            if result.returncode != 0:
                move_errors.append(f"{task.id}: {result.stderr.strip()}")
                continue
        else:
            shutil.move(str(task.path), str(dest))
        print(f"Archived {task.id} -> {dest}")

    if move_errors:
        for message in move_errors:
            print(message, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
