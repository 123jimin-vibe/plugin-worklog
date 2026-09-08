"""Worklog workflow commands, runnable from an installed plugin."""

import argparse
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("worklog requires Python 3.11 or newer (standard-library TOML support).")

from worklog_lib.initialization import PreflightError, RollbackError, initialize
from worklog_lib.context import Context
from worklog_lib.tag_command import run_tag
from worklog_lib.entity_commands import run_create, run_field
from worklog_lib.status_command import run_status
from worklog_lib.task_command import run_task


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="worklog", description="Manage worklog workflows with action-scoped diagnostics and file access.")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Initialize an explicitly adopted worklog.",
                               description="Create missing worklog structure, preserving existing data.",
                               epilog="Running init means the project has chosen to use worklog; it does not establish spec coverage.")
    init.add_argument("project", nargs="?", default=".", metavar="PROJECT",
                      help="Project directory (default: current directory).")
    tag = commands.add_parser("tag", help="Inspect and maintain the tag database.")
    actions = tag.add_subparsers(dest="action", required=True)
    for action in ("list", "add", "update", "remove"):
        sub = actions.add_parser(action)
        sub.add_argument("--project", default=".", metavar="PROJECT")
        if action != "list":
            sub.add_argument("tag", metavar="TAG")
        if action in ("add", "update"):
            sub.add_argument("--description")
        if action == "update":
            sub.add_argument("--name")
    status = commands.add_parser("status", help="Orient from declared worklog state (not certification).",
                                 description="Summarize the selected relationship working set; omit selectors for the whole worklog.",
                                 epilog="Diagnostics concern the requested results. Relevant errors retain useful partial output and return a nonzero exit status.")
    status.add_argument("entities", nargs="*", metavar="ENTITY")
    status.add_argument("--path", nargs="+", action="extend", metavar="PATH")
    status.add_argument("--project", default=".", metavar="PROJECT")
    create = commands.add_parser("create", help="Create minimal specs, tasks, or notes.")
    create.add_argument("kind", choices=("spec", "task", "note"))
    create.add_argument("titles", nargs="+", metavar="TITLE")
    create.add_argument("--parent")
    for option in ("tag", "paths", "modifies", "blocked-by"):
        create.add_argument("--" + option, nargs="+", action="extend")
    create.add_argument("--project", default=".", metavar="PROJECT")
    field = commands.add_parser("field", help="Edit supported fields; preserve other metadata and body text.")
    actions = field.add_subparsers(dest="action", required=True)
    for action in ("set", "add", "remove", "unset"):
        sub = actions.add_parser(action)
        sub.add_argument("entities", nargs="+", metavar="ENTITY")
        sub.add_argument("--field", required=True)
        if action != "unset":
            sub.add_argument("--value", nargs="+", required=True)
        sub.add_argument("--project", default=".", metavar="PROJECT")
    task = commands.add_parser("task", help="Transition tasks; finish/cancel also archive.")
    actions = task.add_subparsers(dest="action", required=True)
    for action in ("start", "block", "resume", "finish", "cancel"):
        sub = actions.add_parser(action, epilog="Targets are independent. Before closure, verify delivery and write back governing specs; command success does not prove completion.")
        sub.add_argument("entities", nargs="+", metavar="TASK")
        sub.add_argument("--project", default=".", metavar="PROJECT")
        if action in ("block", "cancel"):
            sub.add_argument("--reason", required=action == "block")
        if action == "resume":
            sub.add_argument("--checked", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command != "init":
            operation = {"tag": run_tag, "status": run_status, "create": run_create, "field": run_field, "task": run_task}[args.command]
            messages, errors = operation(Context(args.project), args)
            for message in messages:
                print(message)
            for error in errors:
                print(error, file=sys.stderr)
            return int(bool(errors))
        result = initialize(Path(args.project))
    except RollbackError as exc:
        print(f"{args.command} failed: {exc}\nInspect the reported paths before retrying.", file=sys.stderr)
        return 1
    except (ValueError, OSError, UnicodeError) as exc:
        print(f"{args.command} failed: {exc}\nNo worklog changes retained. Resolve the reported problem and retry.", file=sys.stderr)
        return 1
    print(result.message)
    print(f"Project: {result.project}")
    for path in result.created:
        print(f"Created: {path.relative_to(result.project)}")
    for path in result.existing:
        print(f"Existing: {path.relative_to(result.project)}")
    print("Initialization does not establish adequate spec coverage.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
