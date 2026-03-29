# @worklog s0017
"""Tests for plugin/skills/worklog/scripts/search.py — entity querying."""

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from tests.helpers import make_worklog, write_entity, write_tags

_SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "plugin" / "skills" / "worklog" / "scripts" / "search.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "search.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _run_search(worklog_root, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


def _populate(root):
    """Create a fixture worklog with mixed entities for search tests."""
    write_tags(root, ["auth", "tooling", "quality"])
    write_entity(root, "s0001", {
        "id": "s0001", "title": "Auth", "tags": ["auth"],
    })
    write_entity(root, "s0010", {
        "id": "s0010", "title": "Tooling", "tags": ["tooling"],
    })
    write_entity(root, "t0001", {
        "id": "t0001", "title": "Add login", "tags": ["auth"],
        "status": "pending", "modifies": ["s0001"],
    })
    write_entity(root, "t0002", {
        "id": "t0002", "title": "Scripts", "tags": ["tooling"],
        "status": "active", "modifies": ["s0010"],
    })
    write_entity(root, "t0003", {
        "id": "t0003", "title": "Tests", "tags": ["tooling", "quality"],
        "status": "pending", "modifies": ["s0010"],
    })
    write_entity(root, "d0001", {
        "id": "d0001", "title": "Use JWT",
        "relates_to": ["s0001"],
    })
    write_entity(root, "d0002", {
        "id": "d0002", "title": "Python only",
        "relates_to": ["s0010"],
    })


# ===================================================================
# Filter by tag
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchByTag(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_tag_tooling(self):
        result = _run_search(self.worklog, "--tag", "tooling")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("s0010", output)
        self.assertIn("t0002", output)
        self.assertIn("t0003", output)
        # Auth entities should not appear.
        self.assertNotIn("s0001", output)
        self.assertNotIn("t0001", output)


# ===================================================================
# Filter by status
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchByStatus(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_status_pending(self):
        result = _run_search(self.worklog, "--status", "pending")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("t0001", output)
        self.assertIn("t0003", output)
        self.assertNotIn("t0002", output)


# ===================================================================
# Filter by modifies
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchByModifies(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_modifies_s0001(self):
        result = _run_search(self.worklog, "--modifies", "s0001")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("t0001", output)
        self.assertNotIn("t0002", output)
        self.assertNotIn("t0003", output)


# ===================================================================
# Filter by type
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchByType(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_type_spec(self):
        result = _run_search(self.worklog, "--type", "spec")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("s0001", output)
        self.assertIn("s0010", output)
        # Tasks and decisions should not appear.
        self.assertNotIn("t0001", output)
        self.assertNotIn("d0001", output)


# ===================================================================
# Filter by relates-to
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchByRelatesTo(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_relates_to_s0010(self):
        result = _run_search(self.worklog, "--relates-to", "s0010")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("d0002", output)
        self.assertNotIn("d0001", output)


# ===================================================================
# Extended ID normalization
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchModifiesExtendedId(unittest.TestCase):
    """--modifies with a short ID normalizes to match canonical form."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Auth", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Login", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_modifies_short_id_s1(self):
        result = _run_search(self.worklog, "--modifies", "s1")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0001", result.stdout)

    def test_relates_to_short_id(self):
        write_entity(self.worklog, "d0001", {
            "id": "d0001", "title": "Use JWT",
            "relates_to": ["s0001"],
        })
        result = _run_search(self.worklog, "--relates-to", "s1")
        self.assertEqual(result.returncode, 0)
        self.assertIn("d0001", result.stdout)


# ===================================================================
# Archived entities in search
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchIncludesArchived(unittest.TestCase):
    """Archived entities appear in search results."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Active task", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })
        write_entity(self.worklog, "t0004", {
            "id": "t0004", "title": "Archived task", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        }, subdir="archive/task")

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_archived_task_in_tag_search(self):
        result = _run_search(self.worklog, "--tag", "misc")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0004", result.stdout)
        self.assertIn("t0001", result.stdout)

    def test_archived_task_in_status_search(self):
        result = _run_search(self.worklog, "--status", "done")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0004", result.stdout)

    def test_archived_task_in_modifies_search(self):
        result = _run_search(self.worklog, "--modifies", "s0001")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0004", result.stdout)


# ===================================================================
# Combined filters (AND logic)
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchCombinedFilters(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_tag_and_status(self):
        result = _run_search(self.worklog, "--tag", "tooling", "--status", "pending")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        # Only t0003 is both tooling-tagged and pending.
        self.assertIn("t0003", output)
        self.assertNotIn("t0002", output)  # tooling but active
        self.assertNotIn("t0001", output)  # pending but auth-tagged


# ===================================================================
# No matches
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchNoMatches(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_nonexistent_tag(self):
        result = _run_search(self.worklog, "--tag", "nonexistent")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "(none)")


# ===================================================================
# No filters
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestSearchNoFilters(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_no_filters(self):
        """No filters: either returns all entities or exits with usage error."""
        result = _run_search(self.worklog)
        if result.returncode == 0:
            # Returned all entities.
            output = result.stdout
            for eid in ["s0001", "s0010", "t0001", "t0002", "t0003", "d0001", "d0002"]:
                self.assertIn(eid, output)
        else:
            # Usage error is also acceptable.
            output = result.stdout + result.stderr
            self.assertTrue(len(output.strip()) > 0,
                            "Non-zero exit should produce a message")


if __name__ == "__main__":
    unittest.main()
