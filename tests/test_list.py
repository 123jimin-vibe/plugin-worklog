# @worklog s0017
"""Tests for plugin/skills/worklog/scripts/list.py — entity listing."""

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
    / "plugin" / "skills" / "worklog" / "scripts" / "list.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "list.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _run_list(worklog_root, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


def _populate(root):
    """Fixture with entities for list tests."""
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


def _populate_with_archive(root):
    """Fixture including an archived task."""
    _populate(root)
    write_entity(root, "t0004", {
        "id": "t0004", "title": "Old work", "tags": ["auth"],
        "status": "done", "modifies": ["s0001"],
    }, subdir="archive/task")


# ===================================================================
# Default listing
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListDefault(unittest.TestCase):
    """Default: all active entities, one per line, sorted by ID."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_all_active_listed(self):
        result = _run_list(self.worklog)
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        for eid in ["s0001", "s0010", "t0001", "t0002", "t0003", "d0001"]:
            self.assertIn(eid, output)

    def test_sorted_by_id(self):
        result = _run_list(self.worklog)
        output = result.stdout
        lines = [l for l in output.strip().splitlines() if l.strip()]
        # Extract IDs from each line (they should appear as the first
        # recognizable token). Just verify ordering by checking that
        # each ID appears before the next one.
        ids_in_order = []
        for eid in ["d0001", "s0001", "s0010", "t0001", "t0002", "t0003"]:
            pos = output.find(eid)
            if pos >= 0:
                ids_in_order.append((pos, eid))
        ids_in_order.sort()
        sorted_ids = [eid for _, eid in ids_in_order]
        self.assertEqual(sorted_ids, sorted(sorted_ids))


# ===================================================================
# Filter by type
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListFilterByType(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_type_task(self):
        result = _run_list(self.worklog, "--type", "task")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("t0001", output)
        self.assertIn("t0002", output)
        self.assertIn("t0003", output)
        self.assertNotIn("s0001", output)
        self.assertNotIn("d0001", output)


# ===================================================================
# Group by status
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListGroupByStatus(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_tasks_grouped(self):
        result = _run_list(self.worklog, "--type", "task", "--group-by", "status")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        # Output should contain status headings.
        self.assertIn("pending", output.lower())
        self.assertIn("active", output.lower())
        # Tasks should appear under their status.
        self.assertIn("t0001", output)
        self.assertIn("t0002", output)
        self.assertIn("t0003", output)


# ===================================================================
# Group by tag
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListGroupByTag(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_entities_grouped_by_tag(self):
        result = _run_list(self.worklog, "--group-by", "tag")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        # t0003 has both "tooling" and "quality" tags — should appear under both.
        # Check that tag names appear as headings and entities are listed.
        self.assertIn("tooling", output.lower())
        self.assertIn("auth", output.lower())
        self.assertIn("t0003", output)


# ===================================================================
# Group by status with status-less entities
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListGroupByStatusStatusless(unittest.TestCase):
    """Specs and decisions have no status; they group under (no status)."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_statusless_grouped_under_no_status(self):
        result = _run_list(self.worklog, "--group-by", "status")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        self.assertIn("(no status)", output)
        # The spec and decision land in that group; tasks keep their statuses.
        self.assertIn("s0001", output)
        self.assertIn("d0001", output)
        self.assertIn("pending", output.lower())


# ===================================================================
# Sort by title
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListSortByTitle(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_alphabetical_by_title(self):
        result = _run_list(self.worklog, "--sort", "title")
        self.assertEqual(result.returncode, 0)
        output = result.stdout
        # Titles in alphabetical order: Add login, Auth, Scripts, Tests, Tooling, Use JWT
        # Check that "Add login" appears before "Use JWT".
        pos_add = output.find("Add login")
        pos_jwt = output.find("Use JWT")
        self.assertGreater(pos_add, -1)
        self.assertGreater(pos_jwt, -1)
        self.assertLess(pos_add, pos_jwt)


# ===================================================================
# Excludes archive by default
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListExcludesArchive(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate_with_archive(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_archived_absent(self):
        result = _run_list(self.worklog)
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("t0004", result.stdout)


# ===================================================================
# Includes archive when requested
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListIncludesArchive(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        _populate_with_archive(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_archived_present(self):
        result = _run_list(self.worklog, "--archived")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0004", result.stdout)


# ===================================================================
# Empty result
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestListEmptyResult(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)
        # Only create a spec and task, no decisions.
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_no_decisions(self):
        result = _run_list(self.worklog, "--type", "decision")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "(none)")


if __name__ == "__main__":
    unittest.main()
