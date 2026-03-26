# @worklog s0010
"""Print the next available ID for a given entity type."""

import argparse
import pathlib

from lib.constants import TYPE_TO_BUCKET, TYPE_TO_PREFIX, parse_id
from lib.discover import discover_entities


def main(argv=None):
    parser = argparse.ArgumentParser(description="Next available worklog entity ID.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    parser.add_argument("type", choices=list(TYPE_TO_PREFIX), help="Entity type.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)
    prefix = TYPE_TO_PREFIX[args.type]

    store = discover_entities(root)
    bucket = getattr(store, TYPE_TO_BUCKET[args.type])
    max_num = 0
    for entity in bucket:
        parsed = parse_id(entity.id)
        if parsed and parsed[0] == prefix:
            max_num = max(max_num, parsed[1])

    next_id = f"{prefix}{max_num + 1:04d}"
    print(next_id)


if __name__ == "__main__":
    main()
