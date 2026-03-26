# @worklog s0017
"""Tests for plugin/skills/worklog/script/next_id.py — next available ID."""

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from tests.helpers import make_worklog, write_entity

_SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "plugin" / "skills" / "worklog" / "script" / "next_id.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "next_id.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _run_next_id(worklog_root, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


# ===================================================================
# Normal sequence
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestNextIdNormalSequence(unittest.TestCase):
    """Next ID is one past the highest existing ID (no gap filling)."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_spec_next_after_highest(self):
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "First", "tags": ["misc"],
        })
        write_entity(self.worklog, "s0003", {
            "id": "s0003", "title": "Third", "tags": ["misc"],
        })
        write_entity(self.worklog, "s0010", {
            "id": "s0010", "title": "Tenth", "tags": ["misc"],
        })

        result = _run_next_id(self.worklog, "spec")
        self.assertEqual(result.returncode, 0)
        self.assertIn("s0011", result.stdout.strip())


# ===================================================================
# Empty type — no existing entities
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestNextIdEmpty(unittest.TestCase):
    """When no entities of a type exist, the first ID is returned."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_first_spec(self):
        result = _run_next_id(self.worklog, "spec")
        self.assertEqual(result.returncode, 0)
        self.assertIn("s0001", result.stdout.strip())

    def test_first_task(self):
        result = _run_next_id(self.worklog, "task")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0001", result.stdout.strip())

    def test_first_decision(self):
        result = _run_next_id(self.worklog, "decision")
        self.assertEqual(result.returncode, 0)
        self.assertIn("d0001", result.stdout.strip())


# ===================================================================
# Archive included
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestNextIdIncludesArchive(unittest.TestCase):
    """Archived entities are considered when computing the next ID."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_archived_task_counted(self):
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Active", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })
        write_entity(self.worklog, "t0004", {
            "id": "t0004", "title": "Archived", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        }, subdir="archive/task")

        result = _run_next_id(self.worklog, "task")
        self.assertEqual(result.returncode, 0)
        # Next ID should be t0005, not t0002.
        self.assertIn("t0005", result.stdout.strip())


# ===================================================================
# Extended IDs (non-4-digit)
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestNextIdExtendedIds(unittest.TestCase):
    """next_id correctly accounts for non-4-digit IDs when computing max."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_short_id_counted(self):
        write_entity(self.worklog, "s1", {
            "id": "s1", "title": "Short", "tags": ["misc"],
        })
        write_entity(self.worklog, "s0003", {
            "id": "s0003", "title": "Normal", "tags": ["misc"],
        })
        result = _run_next_id(self.worklog, "spec")
        self.assertEqual(result.returncode, 0)
        self.assertIn("s0004", result.stdout.strip())

    def test_long_id_counted(self):
        write_entity(self.worklog, "t00001", {
            "id": "t00001", "title": "Long", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })
        write_entity(self.worklog, "t0010", {
            "id": "t0010", "title": "Normal", "tags": ["misc"],
            "status": "active", "modifies": ["s0001"],
        })
        result = _run_next_id(self.worklog, "task")
        self.assertEqual(result.returncode, 0)
        self.assertIn("t0011", result.stdout.strip())


# ===================================================================
# Invalid arguments
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestNextIdInvalidArgs(unittest.TestCase):
    """Invalid or missing arguments produce a non-zero exit."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_invalid_type(self):
        result = _run_next_id(self.worklog, "banana")
        self.assertNotEqual(result.returncode, 0)

    def test_no_type_arg(self):
        result = _run_next_id(self.worklog)
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
