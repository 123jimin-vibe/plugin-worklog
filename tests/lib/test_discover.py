# @worklog s0017
"""Tests for plugin/skills/worklog/script/lib/discover.py — entity discovery.

Tests verify attributes via duck typing (e.g. store.entities, tag.name),
not concrete class identity.
"""

import pathlib
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
# discover_entities — returns EntityStore-like object
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
        store = discover_entities(self.worklog)
        ids = {e.id for e in store.entities}
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

        store = discover_entities(self.worklog)
        ids = {e.id for e in store.entities}
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

        store = discover_entities(self.worklog)
        ids = {e.id for e in store.entities}
        self.assertIn("t0004", ids)


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverEmptyWorklog(unittest.TestCase):
    """Empty worklog returns an empty entities list."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_empty(self):
        store = discover_entities(self.worklog)
        self.assertEqual(list(store.entities), [])


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverSkipsNonEntities(unittest.TestCase):
    """Non-entity files (no valid frontmatter) are skipped."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_readme_skipped(self):
        readme = pathlib.Path(self.worklog) / "spec" / "README.md"
        readme.write_text("# Specs\nThis is not an entity.\n", encoding="utf-8")

        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Real spec", "tags": ["misc"],
        })

        store = discover_entities(self.worklog)
        ids = {e.id for e in store.entities}
        self.assertEqual(ids, {"s0001"})


@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverMixedValidInvalid(unittest.TestCase):
    """Valid entities in store.entities, broken files in store.errors."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_valid_returned_broken_in_errors(self):
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Good spec", "tags": ["misc"],
        })
        # Write a broken file (no closing fence).
        broken = pathlib.Path(self.worklog) / "spec" / "s0002-broken.md"
        broken.write_text('+++\nid = "s0002"\ntitle = "Broken"\n# no closing fence\n', encoding="utf-8")

        store = discover_entities(self.worklog)
        ids = {e.id for e in store.entities}
        self.assertIn("s0001", ids)
        self.assertGreater(len(store.errors), 0)


# ===================================================================
# Separate buckets — store.specs, store.tasks, store.decisions
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverSeparateBuckets(unittest.TestCase):
    """Entities are sorted into specs, tasks, and decisions lists."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_specs_bucket(self):
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Auth", "tags": ["auth"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Add login", "tags": ["auth"],
            "status": "pending", "modifies": ["s0001"],
        })
        store = discover_entities(self.worklog)
        spec_ids = {e.id for e in store.specs}
        task_ids = {e.id for e in store.tasks}
        self.assertEqual(spec_ids, {"s0001"})
        self.assertEqual(task_ids, {"t0001"})
        self.assertEqual(list(store.decisions), [])

    def test_decisions_bucket(self):
        write_entity(self.worklog, "d0001", {
            "id": "d0001", "title": "Use JWT", "relates_to": ["s0001"],
        })
        store = discover_entities(self.worklog)
        decision_ids = {e.id for e in store.decisions}
        self.assertEqual(decision_ids, {"d0001"})
        self.assertEqual(list(store.specs), [])
        self.assertEqual(list(store.tasks), [])


# ===================================================================
# Archived flag — entity.archived
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverArchivedFlag(unittest.TestCase):
    """Entities from archive dirs have archived=True, others False."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_active_entity_not_archived(self):
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Active", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })
        store = discover_entities(self.worklog)
        task = next(e for e in store.tasks if e.id == "t0001")
        self.assertFalse(task.archived)

    def test_archived_entity_flagged(self):
        write_entity(self.worklog, "t0004", {
            "id": "t0004", "title": "Done", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        }, subdir="archive/task")
        store = discover_entities(self.worklog)
        task = next(e for e in store.tasks if e.id == "t0004")
        self.assertTrue(task.archived)


# ===================================================================
# Extended IDs (non-4-digit)
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestDiscoverExtendedIds(unittest.TestCase):
    """Entities with non-4-digit IDs are discovered normally."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_mixed_id_lengths_discovered(self):
        write_entity(self.worklog, "s1", {
            "id": "s1", "title": "Short spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "s0002", {
            "id": "s0002", "title": "Normal spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t00001", {
            "id": "t00001", "title": "Long task", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })
        store = discover_entities(self.worklog)
        ids = {e.id for e in store.entities}
        self.assertEqual(ids, {"s1", "s0002", "t00001"})

    def test_extended_id_in_correct_bucket(self):
        write_entity(self.worklog, "d42", {
            "id": "d42", "title": "Answer",
            "relates_to": ["s0001"],
        })
        store = discover_entities(self.worklog)
        decision_ids = {e.id for e in store.decisions}
        self.assertIn("d42", decision_ids)


# ===================================================================
# load_tags — returns Tag-like objects
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsHappyPath(unittest.TestCase):
    """Standard tags.csv is parsed into Tag objects with names and descriptions."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_returns_tags_with_names(self):
        write_tags(self.worklog, ["auth", "tooling", "quality"])
        result = load_tags(self.worklog)
        names = {t.name for t in result}
        self.assertEqual(names, {"auth", "tooling", "quality"})


@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsDescription(unittest.TestCase):
    """Tag descriptions are captured from tags.csv."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_description_present(self):
        # Write tags.csv with explicit descriptions.
        path = pathlib.Path(self.worklog) / "tags.csv"
        path.write_text(
            "tag,description\n"
            'auth,"Authentication and authorization."\n'
            'tooling,"Automation scripts and tools."\n',
            encoding="utf-8",
        )
        result = load_tags(self.worklog)
        by_name = {t.name: t for t in result}
        self.assertIn("auth", by_name)
        self.assertIn("Authentication", by_name["auth"].description)


@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsEmpty(unittest.TestCase):
    """tags.csv with no data rows returns an empty list."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_empty_table(self):
        path = pathlib.Path(self.worklog) / "tags.csv"
        path.write_text("tag,description\n", encoding="utf-8")
        result = load_tags(self.worklog)
        self.assertEqual(len(result), 0)


@unittest.skipUnless(_module_available, _missing_reason)
class TestLoadTagsMissing(unittest.TestCase):
    """Missing tags.csv raises or returns empty list."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_missing_file(self):
        try:
            result = load_tags(self.worklog)
            self.assertEqual(len(result), 0)
        except (FileNotFoundError, OSError):
            pass  # raising is also acceptable


if __name__ == "__main__":
    unittest.main()
