# @worklog s0010
"""Print the next available ID for a given entity type."""

import argparse
import pathlib
import re

from lib.constants import ID_PREFIX_TO_TYPE
from lib.discover import discover_entities

_TYPE_TO_PREFIX = {v: k for k, v in ID_PREFIX_TO_TYPE.items()}
_TYPE_TO_BUCKET = {"spec": "specs", "task": "tasks", "decision": "decisions"}
_ID_PATTERN = re.compile(r"^[std](\d{4})$")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Next available worklog entity ID.")
    parser.add_argument("-w", default="./worklog", help="Worklog root directory.")
    parser.add_argument("type", choices=list(_TYPE_TO_PREFIX), help="Entity type.")
    args = parser.parse_args(argv)

    root = pathlib.Path(args.w)
    prefix = _TYPE_TO_PREFIX[args.type]

    store = discover_entities(root)
    bucket = getattr(store, _TYPE_TO_BUCKET[args.type])
    max_num = 0
    for entity in bucket:
        m = _ID_PATTERN.match(entity.id)
        if m:
            max_num = max(max_num, int(m.group(1)))

    next_id = f"{prefix}{max_num + 1:04d}"
    print(next_id)


if __name__ == "__main__":
    main()
