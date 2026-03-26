# @worklog s0017
"""Tests for plugin/skills/worklog/script/lib/discover.py — entity discovery."""

import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from tests.loader import load_module
from tests.helpers import make_worklog, write_entity, write_tags

_mod, _module_available, _missing_reason = load_module(
    "lib/discover.py",
    expected=["discover_entities", "load_tags"],
)

if _module_available:
    discover_entities = _mod.discover_entities
    load_tags = _mod.load_tags




# ===================================================================
# discover_entities
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverStandardLayout(unittest.TestCase):
    """Entities in spec/, task/, decision/ are all discovered."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_finds_all_entity_types(self):
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Auth", "tags": ["auth"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Add login", "tags": ["auth"],
            "status": "pending", "modifies": ["s0001"],
        })
        write_entity(self.worklog, "d0001", {
            "id": "d0001", "title": "Use JWT", "relates_to": ["s0001"],
        })
        result = discover_entities(self.worklog)
        ids = {e["id"] for e in result}
        self.assertEqual(ids, {"s0001", "t0001", "d0001"})


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverRecursiveSpecDirs(unittest.TestCase):
    """Specs in subdirectories like spec/entity/ are found."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_finds_specs_in_subdirectories(self):
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Top level", "tags": ["misc"],
        })
        write_entity(self.worklog, "s0011", {
            "id": "s0011", "title": "Entity spec", "tags": ["entity"],
        }, subdir="spec/entity")
        write_entity(self.worklog, "s0004", {
            "id": "s0004", "title": "Greenfield", "tags": ["workflow"],
        }, subdir="spec/workflow")

        result = discover_entities(self.worklog)
        ids = {e["id"] for e in result}
        self.assertIn("s0001", ids)
        self.assertIn("s0011", ids)
        self.assertIn("s0004", ids)


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverArchive(unittest.TestCase):
    """Entities in archive/task/ are included."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_archived_task_found(self):
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Active task", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })
        write_entity(self.worklog, "t0004", {
            "id": "t0004", "title": "Done task", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        }, subdir="archive/task")

        result = discover_entities(self.worklog)
        ids = {e["id"] for e in result}
        self.assertIn("t0004", ids)


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverEmptyWorklog(unittest.TestCase):
    """Empty worklog returns an empty list."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_empty(self):
        result = discover_entities(self.worklog)
        self.assertEqual(result, [])


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverSkipsNonEntities(unittest.TestCase):
    """Non-entity files (no valid frontmatter) are skipped."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_readme_skipped(self):
        readme = os.path.join(self.worklog, "spec", "README.md")
        with open(readme, "w", encoding="utf-8") as f:
            f.write("# Specs\nThis is not an entity.\n")

        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Real spec", "tags": ["misc"],
        })

        result = discover_entities(self.worklog)
        ids = {e["id"] for e in result}
        self.assertEqual(ids, {"s0001"})


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverMixedValidInvalid(unittest.TestCase):
    """Valid entities are returned even when broken files exist."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_valid_returned_broken_skipped(self):
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Good spec", "tags": ["misc"],
        })
        # Write a broken file (no closing fence).
        broken = os.path.join(self.worklog, "spec", "s0002-broken.md")
        with open(broken, "w", encoding="utf-8") as f:
            f.write('+++\nid = "s0002"\ntitle = "Broken"\n# no closing fence\n')

        result = discover_entities(self.worklog)
        ids = {e["id"] for e in result}
        self.assertIn("s0001", ids)


# ===================================================================
# load_tags
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsHappyPath(unittest.TestCase):
    """Standard tags.md is parsed into a set of tag strings."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_returns_tag_set(self):
        write_tags(self.worklog, ["auth", "tooling", "quality"])
        result = load_tags(self.worklog)
        self.assertEqual(result, {"auth", "tooling", "quality"})


@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsEmpty(unittest.TestCase):
    """tags.md with no data rows returns an empty set."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_empty_table(self):
        # Write tags.md with header but no rows.
        path = os.path.join(self.worklog, "tags.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Tags\n\n| Tag | Description |\n|-----|-------------|\n")
        result = load_tags(self.worklog)
        self.assertEqual(result, set())


@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsMissing(unittest.TestCase):
    """Missing tags.md raises or returns empty set."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_missing_file(self):
        # Accept either an exception or an empty set.
        try:
            result = load_tags(self.worklog)
            self.assertEqual(result, set())
        except (FileNotFoundError, OSError):
            pass  # raising is also acceptable


if __name__ == "__main__":
    unittest.main()
