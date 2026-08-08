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

`tests/` mirrors the plugin's script directory: one module per script, and a `lib/` subdirectory for the shared library modules. Each test module is named after its target.

- `loader.py` — shared module loading for library targets.
- `helpers.py` — shared fixture builders: worklog tree creation, entity file writing, tag index writing.

## Exercising the Target

Two mechanisms, chosen by what the target is.

- **Scripts are exercised as commands.** The test runs the script in a subprocess under the same interpreter as the suite and asserts on exit status, stdout, and stderr. The command line is a script's observable contract — argument handling, exit codes, and which stream a message lands on are all prescribed behavior, and only a subprocess exercises them.
- **Library modules are imported.** The shared loader loads a module from its path, putting the script root on the import path and pre-loading sibling modules so intra-package imports resolve. It reports whether the module loaded and why not, and can assert that the module exposes named attributes.

Either mechanism resolves its target relative to the test file. Neither requires the plugin to be installed.

## Availability Guard

Tests precede implementation, so a target may be absent. Both mechanisms expose an availability flag and a reason; test classes skip on that flag instead of failing at import time, so a test file stays collectable against a missing target.

## Fixtures

Each test class builds exactly the state it needs in a temporary directory and removes it afterwards. No fixture worklog is checked into the repo.

Tests for git-dependent behavior — drift classification, and moving a tracked file on archive — build a real git repository with commits, because the behavior under test reads git history.

## Running

```
python -m unittest discover -s tests -p "test_*.py"
```

## Anticipated Changes

- CI integration when the project gets a pipeline.
- Coverage for the shared git-drift library module, currently exercised only through the scripts that consume it.

## Dangers

- Tests that verify implementation details (function signatures, internal data structures) instead of observable behavior break on every refactor.
- Fixture worklogs that are too simple miss real-world edge cases. Fixture worklogs that are too complex make tests hard to read.
- The availability guard masking real failures — a target that fails to load because of a bug looks the same as one that has not been written yet.
