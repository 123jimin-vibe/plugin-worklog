+++
id = "s0017"
title = "Testing"
tags = ["quality", "tooling"]
paths = ["tests/**"]
+++

# Testing

Automated tests for plugin scripts and shared libraries. Tests are written before implementation and must pass against the spec, not the code.

## Framework

Python `unittest` standard library. No external test runner dependency.

## Layout

`tests/` mirrors `plugin/skills/worklog/script/`:

```
tests/
├── loader.py
├── helpers.py
├── lib/
│   ├── test_parse.py
│   └── test_discover.py
├── test_validate.py
├── test_next_id.py
├── test_drift.py
├── test_search.py
└── test_list.py
```

- `loader.py` — shared module loading via `importlib.util` (used by lib/ tests).
- `helpers.py` — shared fixture functions: `make_worklog`, `write_entity`, `write_tags`.

## Module Loading

Tests load the module under test via `importlib.util.spec_from_file_location`, resolving paths relative to the test file. When the module does not exist yet (tests written before implementation), the test file remains importable — all test classes are guarded with `@unittest.skipUnless` so they skip instead of failing.

```python
_MODULE_PATH = str(
    pathlib.Path(__file__).resolve().parents[2]
    / "plugin" / "skills" / "worklog" / "script" / "lib" / "parse.py"
)
_spec = importlib.util.spec_from_file_location("lib.parse", _MODULE_PATH)

_module_available = _spec is not None and _spec.loader is not None
_missing_reason = "parse.py not loadable"

if _module_available:
    try:
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
    except BaseException as _exc:
        _module_available = False
        _missing_reason = f"parse.py failed to load: {_exc}"
```

## Boilerplate

Three patterns repeat across every test file.

### Module loading block

Every test file resolves the module path relative to itself, attempts to load it, and exposes a `_module_available` flag. Each test class is decorated with `@unittest.skipUnless(_module_available, _missing_reason)`. The only varying parts are the relative path to the module and the names extracted from it.

```python
import importlib.util
import pathlib
import unittest

_MODULE_PATH = str(
    pathlib.Path(__file__).resolve().parents[N]  # N varies per depth
    / "plugin" / "skills" / "worklog" / "script" / "<module>.py"
)
_spec = importlib.util.spec_from_file_location("<module_name>", _MODULE_PATH)

_module_available = _spec is not None and _spec.loader is not None
_missing_reason = "<module>.py not loadable"

if _module_available:
    try:
        _mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)
    except BaseException as _exc:
        _module_available = False
        _missing_reason = f"<module>.py failed to load: {_exc}"

if _module_available:
    for _fn in ["<expected_function_1>", "<expected_function_2>"]:
        if not hasattr(_mod, _fn):
            _module_available = False
            _missing_reason = f"<module>.py is missing function: {_fn}"
            break

if _module_available:
    expected_function_1 = _mod.expected_function_1
    expected_function_2 = _mod.expected_function_2
```

### Fixture worklog creation

Most test classes need a temporary worklog directory with known structure. The pattern is `tempfile.mkdtemp()` in `setUp`, `shutil.rmtree()` in `tearDown`, and helper methods to populate it.

```python
import shutil
import tempfile

class TestSomething(unittest.TestCase):
    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        # create subdirectories
        for d in ["spec", "task", "decision", "archive/task"]:
            os.makedirs(os.path.join(self.worklog, d), exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)
```

This repeats in test_validate, test_next_id, test_search, test_list, test_discover, and test_drift (6 of 7 test files). Only test_parse tests a single file, not a directory tree.

### Entity file writing

Tests that exercise validate, search, list, and discover all need to write entity files with TOML frontmatter into the fixture worklog. The pattern is a helper that takes an ID, fields dict, and optional body, then writes a properly formatted file to the right subdirectory.

```python
def _write_entity(self, entity_id, fields, body="", subdir=None):
    """Write a worklog entity file into the fixture."""
    prefix = entity_id[0]
    if subdir is None:
        subdir = {"s": "spec", "t": "task", "d": "decision"}[prefix]
    slug = fields.get("title", "untitled").lower().replace(" ", "-")
    filename = f"{entity_id}-{slug}.md"
    path = os.path.join(self.worklog, subdir, filename)
    lines = ["+++"]
    for k, v in fields.items():
        if isinstance(v, list):
            lines.append(f'{k} = {v}')
        elif isinstance(v, str):
            lines.append(f'{k} = "{v}"')
    lines.append("+++")
    if body:
        lines.append("")
        lines.append(body)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path
```

Factored into `tests/helpers.py` as `write_entity()`.

## Fixtures

Tests that need a worklog directory create one in `tempfile.mkdtemp()` during `setUp` and remove it in `tearDown`. No shared fixture directory checked into the repo — each test class builds exactly the state it needs.

For `drift.py` tests, the fixture must be a real git repository (`git init` + commits) since drift detection depends on git history.

## Running

```
python -m unittest discover -s tests -p "test_*.py"
```

## Anticipated Changes

- CI integration when the project gets a pipeline.

## Dangers

- Tests that verify implementation details (function signatures, internal data structures) instead of observable behavior break on every refactor.
- Fixture worklogs that are too simple miss real-world edge cases. Fixture worklogs that are too complex make tests hard to read.
- `skipUnless` masking real failures — a module that fails to load due to a bug looks the same as a module that hasn't been written yet.
