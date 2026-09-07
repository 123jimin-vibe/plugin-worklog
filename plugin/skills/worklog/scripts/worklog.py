"""Worklog workflow commands, runnable from an installed plugin."""

import argparse
import sys
from pathlib import Path

if sys.version_info < (3, 11):
    raise SystemExit("worklog requires Python 3.11 or newer (standard-library TOML support).")

from worklog_lib.initialization import PreflightError, RollbackError, initialize


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="worklog", description="Manage worklog workflows.")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Initialize an explicitly adopted worklog.",
                               description="Create missing worklog structure, preserving existing data.",
                               epilog="Running init means the project has chosen to use worklog; it does not establish spec coverage.")
    init.add_argument("project", nargs="?", default=".", metavar="PROJECT",
                      help="Project directory (default: current directory).")
    args = parser.parse_args(argv)
    try:
        result = initialize(Path(args.project))
    except RollbackError as exc:
        print(f"Initialization failed: {exc}\nInspect the reported paths before retrying.", file=sys.stderr)
        return 1
    except (PreflightError, OSError, UnicodeError) as exc:
        print(f"Initialization failed: {exc}\nNo worklog changes retained. Resolve the reported problem and retry.", file=sys.stderr)
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
