# @worklog s0010
"""List worklog entities with optional filtering, grouping, and sorting."""

import argparse
import pathlib
from collections import defaultdict

from lib.discover import discover_entities


def _format_line(entity):
    """Format a single entity line.  Tasks include status."""
    status = entity.fields.get("status", "")
    if status:
        return f"{entity.id}  {entity.title}  [{status}]"
    return f"{entity.id}  {entity.title}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="List worklog entities.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    parser.add_argument("--type", choices=["spec", "task", "decision"],
                        help="Show only this entity type.")
    parser.add_argument("--group-by", choices=["type", "status", "tag"],
                        help="Group output by field.")
    parser.add_argument("--sort", choices=["id", "title"], default="id",
                        help="Sort by field.")
    parser.add_argument("--archived", action="store_true",
                        help="Include archived entities.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)
    store = discover_entities(root)

    # Select bucket or all.
    _BUCKETS = {"spec": store.specs, "task": store.tasks, "decision": store.decisions}
    if args.type:
        entities = list(_BUCKETS[args.type])
    else:
        entities = list(store.entities)

    # Filter out archived unless requested.
    if not args.archived:
        entities = [e for e in entities if not e.archived]

    # Sort.
    if args.sort == "title":
        entities.sort(key=lambda e: e.title.lower())
    else:
        entities.sort(key=lambda e: e.id)

    if not entities:
        print("(none)")
        return

    # Group output.
    if args.group_by:
        groups = defaultdict(list)
        for e in entities:
            if args.group_by == "type":
                groups[e.type].append(e)
            elif args.group_by == "status":
                status = e.fields.get("status", "(no status)")
                groups[status].append(e)
            elif args.group_by == "tag":
                if e.tags:
                    for tag in e.tags:
                        groups[tag].append(e)
                else:
                    groups["(untagged)"].append(e)

        first = True
        for heading in sorted(groups):
            if not first:
                print()
            first = False
            print(f"[{heading}]")
            for e in groups[heading]:
                print(f"  {_format_line(e)}")
    else:
        for e in entities:
            print(_format_line(e))


if __name__ == "__main__":
    main()
