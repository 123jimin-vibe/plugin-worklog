# @worklog s0010
"""Report specs whose governed source files changed after the spec was last touched.

stdout carries the actionable drift list (exit 1 when non-empty). stderr carries
coverage diagnostics — specs that could not be checked — so an empty stdout never
silently hides "nothing was checked."
"""

import argparse
import pathlib
import sys

from lib.discover import discover_entities
from lib.gitdrift import classify_spec, find_repo_root


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect spec-code drift.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)

    repo_root = find_repo_root(root)
    if repo_root is None:
        print("Not inside a git repository.", file=sys.stderr)
        raise SystemExit(1)

    store = discover_entities(root)
    drifted, unmonitored, unverifiable = [], [], []
    for spec in store.specs:
        category = classify_spec(repo_root, spec)
        if category == "drifted":
            drifted.append(spec)
        elif category == "unmonitored":
            unmonitored.append(spec)
        elif category == "unverifiable":
            unverifiable.append(spec)

    # Coverage diagnostics: what the report could not check, and why.
    for spec in unmonitored:
        print(f"unmonitored (no paths): {spec.id}  {spec.title}", file=sys.stderr)
    for spec in unverifiable:
        print(f"unverifiable (spec not committed): {spec.id}  {spec.title}",
              file=sys.stderr)

    if not drifted:
        print(f"No drift in {len(store.specs) - len(unmonitored) - len(unverifiable)} "
              f"monitored spec(s).", file=sys.stderr)
        raise SystemExit(0)

    for spec in drifted:
        print(f"{spec.id}  {spec.title}")
    raise SystemExit(1)


if __name__ == "__main__":
    main()
