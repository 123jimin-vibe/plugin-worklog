# @worklog s0017
"""Tests for plugin/skills/worklog/scripts/archive.py — task archiving."""

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
    / "plugin" / "skills" / "worklog" / "scripts" / "archive.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "archive.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)


def _make_git_worklog(root):
    """Create a worklog inside a fresh git repo; return the worklog path."""
    _git(str(root), "init")
    _git(str(root), "config", "user.email", "test@test.com")
    _git(str(root), "config", "user.name", "Test")
    worklog = pathlib.Path(root) / "worklog"
    make_worklog(worklog)
    return str(worklog)


def _run_archive(worklog_root, task_id, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), task_id, "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


def _task_path(worklog, name):
    return pathlib.Path(worklog) / "task" / name


def _archived_path(worklog, name):
    return pathlib.Path(worklog) / "archive" / "task" / name


# ===================================================================
# Refuses to archive non-terminal tasks
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestArchiveRefusesNonTerminal(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.worklog = _make_git_worklog(self.root)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_pending_refused(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Unfinished", "tags": ["misc"],
            "status": "pending", "modifies": ["s0001"],
        })

        result = _run_archive(self.worklog, "t0001", "--confirm")
        self.assertNotEqual(result.returncode, 0)
        # File stays put.
        self.assertTrue(_task_path(self.worklog, "t0001-unfinished.md").exists())
        self.assertFalse(_archived_path(self.worklog, "t0001-unfinished.md").exists())


# ===================================================================
# Surfaces the governing specs in full
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestArchiveSurfacesSpecs(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.worklog = _make_git_worklog(self.root)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_prints_spec_body_and_does_not_move(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        }, body="GOVERNED-BEHAVIOR-SENTINEL: the rule that must still hold.")
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Done work", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        })

        # No --confirm: report only.
        result = _run_archive(self.worklog, "t0001")
        self.assertEqual(result.returncode, 0,
                         f"stderr: {result.stderr}")
        self.assertIn("GOVERNED-BEHAVIOR-SENTINEL", result.stdout)
        # Not moved.
        self.assertTrue(_task_path(self.worklog, "t0001-done-work.md").exists())
        self.assertFalse(_archived_path(self.worklog, "t0001-done-work.md").exists())


# ===================================================================
# --confirm moves the file
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestArchiveConfirmMoves(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.worklog = _make_git_worklog(self.root)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def _populate(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        }, body="Behavior.")
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Done work", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        })

    def test_tracked_file_moved_with_git(self):
        self._populate()
        _git(self.root, "add", "-A")
        _git(self.root, "commit", "-m", "initial")

        result = _run_archive(self.worklog, "t0001", "--confirm")
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertFalse(_task_path(self.worklog, "t0001-done-work.md").exists())
        self.assertTrue(_archived_path(self.worklog, "t0001-done-work.md").exists())
        # git still tracks it at the new path.
        tracked = _git(self.root, "ls-files").stdout
        self.assertIn("worklog/archive/task/t0001-done-work.md", tracked)

    def test_untracked_file_moved_plainly(self):
        self._populate()
        # Commit only the spec; leave the task untracked.
        _git(self.root, "add", "worklog/spec", "worklog/tags.csv")
        _git(self.root, "commit", "-m", "spec only")

        result = _run_archive(self.worklog, "t0001", "--confirm")
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertFalse(_task_path(self.worklog, "t0001-done-work.md").exists())
        self.assertTrue(_archived_path(self.worklog, "t0001-done-work.md").exists())


# ===================================================================
# Cancelled tasks need an explanation
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestArchiveCancelled(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.worklog = _make_git_worklog(self.root)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_cancelled_empty_body_refused(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Dropped", "tags": ["misc"],
            "status": "cancelled", "modifies": ["s0001"],
        })  # no body

        result = _run_archive(self.worklog, "t0001", "--confirm")
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(_task_path(self.worklog, "t0001-dropped.md").exists())

    def test_cancelled_with_note_archived(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Dropped", "tags": ["misc"],
            "status": "cancelled", "modifies": ["s0001"],
        }, body="Requirement removed upstream.")

        result = _run_archive(self.worklog, "t0001", "--confirm")
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertTrue(_archived_path(self.worklog, "t0001-dropped.md").exists())


# ===================================================================
# Unknown task
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestArchiveUnknownTask(unittest.TestCase):

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.worklog = _make_git_worklog(self.root)

    def tearDown(self):
        shutil.rmtree(self.root, ignore_errors=True)

    def test_missing_id(self):
        write_tags(self.worklog, ["misc"])
        result = _run_archive(self.worklog, "t9999", "--confirm")
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
