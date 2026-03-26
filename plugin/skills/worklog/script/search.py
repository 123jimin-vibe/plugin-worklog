# @worklog s0010
"""Query worklog entities by combinable filters (AND logic)."""

import argparse
import pathlib

from lib.constants import normalize_id
from lib.discover import discover_entities


def _select_entities(store, args):
    """Pick the narrowest starting set based on explicit type or implied type."""
    if args.type:
        return {"spec": store.specs, "task": store.tasks,
                "decision": store.decisions}[args.type]

    # status/modifies imply tasks, relates-to implies decisions.
    if args.status or args.modifies:
        return store.tasks
    if args.relates_to:
        return store.decisions

    return store.entities


def _apply_filters(entities, args):
    """Apply all active filters (AND logic)."""
    filters = []

    if args.tag:
        filters.append(lambda e: args.tag in e.tags)
    if args.status:
        filters.append(lambda e: e.fields.get("status") == args.status)
    if args.modifies:
        norm = normalize_id(args.modifies)
        filters.append(lambda e: norm in e.fields.get("modifies", []))
    if args.relates_to:
        norm = normalize_id(args.relates_to)
        filters.append(lambda e: norm in e.fields.get("relates_to", []))

    for e in entities:
        if all(f(e) for f in filters):
            yield e


def main(argv=None):
    parser = argparse.ArgumentParser(description="Search worklog entities.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    parser.add_argument("--tag", help="Filter to entities with this tag.")
    parser.add_argument("--status", help="Filter to tasks with this status.")
    parser.add_argument("--modifies", help="Filter to tasks that modify a given spec ID.")
    parser.add_argument("--type", choices=["spec", "task", "decision"],
                        help="Filter to entity type.")
    parser.add_argument("--relates-to", help="Filter to decisions related to a given spec ID.")
    args = parser.parse_args(argv)

    store = discover_entities(pathlib.Path(args.w))
    results = sorted(_apply_filters(_select_entities(store, args), args),
                     key=lambda e: e.id)

    if not results:
        print("(none)")
        return

    for e in results:
        print(f"{e.id}  {e.title}")


if __name__ == "__main__":
    main()
