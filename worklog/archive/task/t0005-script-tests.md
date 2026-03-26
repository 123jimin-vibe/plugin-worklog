+++
id = "t0005"
title = "Write tests for plugin scripts"
tags = ["quality", "tooling"]
status = "done"
modifies = ["s0017"]
blocked_by = []
+++

# Write tests for plugin scripts

Write the test files defined in s0017 for the scripts specified in t0003. Tests are written before implementation per the methodology — all test classes use `@unittest.skipUnless` so they skip cleanly until the modules exist.

## Scope

- `tests/lib/test_parse.py` — test cases from t0003's lib/parse.py table.
- `tests/lib/test_discover.py` — test cases from t0003's lib/discover.py table.
- `tests/test_validate.py` — test cases from t0003's validate.py table.
- `tests/test_next_id.py` — test cases from t0003's next_id.py table.
- `tests/test_drift.py` — test cases from t0003's drift.py table. Fixture must `git init` a temporary repo.
- `tests/test_search.py` — test cases from t0003's search.py table.
- `tests/test_list.py` — test cases from t0003's list.py table.

Each test file follows the loading and fixture patterns from s0017. Test cases derive from the spec (t0003's tables), not from reading the implementation.
