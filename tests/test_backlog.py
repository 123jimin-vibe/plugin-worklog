# @worklog s0017
"""Tests for plugin/skills/worklog/scripts/backlog.py — unified priority view."""

import pathlib
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from tests.helpers import make_worklog, write_entity

_SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "plugin" / "skills" / "worklog" / "scripts" / "backlog.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "backlog.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _run_backlog(worklog_root, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


def _populate(root):
    """Fixture mixing triaged/untriaged tasks and covered/uncovered markers."""
    write_entity(root, "s0001", {
        "id": "s0001", "title": "Recipes", "tags": ["entity"],
    }, body=(
        "Recipe storage.\n\n"
        "- UNIMPLEMENTED Batch import — accept a list of recipes.\n"
        "- UNIMPLEMENTED Export to CSV.\n"
    ))
    write_entity(root, "s0002", {
        "id": "s0002", "title": "Notify", "tags": ["entity"],
    }, body=(
        "Notification delivery.\n\n"
        "Approved items without implementation are marked `UNIMPLEMENTED`.\n"
    ))
    write_entity(root, "s0003", {
        "id": "s0003", "title": "Sharing", "tags": ["entity"],
    }, body=(
        "Sharing.\n\n"
        "- UNIMPLEMENTED Public share links.\n"
    ))
    # Prioritized active task covering s0001's markers.
    write_entity(root, "t0001", {
        "id": "t0001", "title": "Batch work", "tags": ["entity"],
        "status": "active", "modifies": ["s0001"], "priority": 0,
    })
    # Unprioritized open task covering s0003 — marker stays untriaged.
    write_entity(root, "t0002", {
        "id": "t0002", "title": "Sharing groundwork", "tags": ["entity"],
        "status": "pending", "modifies": ["s0003"],
    })
    # Done task with priority — terminal, must not appear or lift markers.
    write_entity(root, "t0003", {
        "id": "t0003", "title": "Old sharing push", "tags": ["entity"],
        "status": "done", "modifies": ["s0003"], "priority": 1,
    })
    # Prioritized pending task touching no markers.
    write_entity(root, "t0004", {
        "id": "t0004", "title": "Chore sweep", "tags": ["entity"],
        "status": "pending", "modifies": [], "priority": 2,
    })
    # Archived task with priority — must never appear.
    write_entity(root, "t0005", {
        "id": "t0005", "title": "Ancient work", "tags": ["entity"],
        "status": "done", "modifies": ["s0001"], "priority": 0,
    }, subdir="archive/task")


# ===================================================================
# Tests
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestBacklogView(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        make_worklog(self.root)
        _populate(self.root)

    def tearDown(self):
        self._tmp.cleanup()

    def test_exits_zero(self):
        result = _run_backlog(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_triaged_ranked_ascending_by_priority(self):
        out = _run_backlog(self.root).stdout
        self.assertIn("Triaged:", out)
        p0 = out.index("t0001")
        p2 = out.index("t0004")
        self.assertLess(p0, p2)

    def test_marker_inherits_lowest_covering_priority(self):
        out = _run_backlog(self.root).stdout
        triaged = out.split("Untriaged:")[0]
        self.assertIn("Batch import", triaged)
        batch_line = next(l for l in triaged.splitlines() if "Batch import" in l)
        self.assertIn("p0", batch_line)
        self.assertIn("s0001", batch_line)
        self.assertIn("t0001", batch_line)

    def test_every_marker_of_covered_spec_is_lifted(self):
        out = _run_backlog(self.root).stdout
        triaged = out.split("Untriaged:")[0]
        self.assertIn("Export to CSV", triaged)

    def test_backticked_token_is_mention_not_marker(self):
        out = _run_backlog(self.root).stdout
        self.assertNotIn("s0002", out)

    def test_uncovered_or_unprioritized_marker_is_untriaged(self):
        out = _run_backlog(self.root).stdout
        untriaged = out.split("Untriaged:")[1]
        self.assertIn("Public share links", untriaged)
        # Covering unprioritized task listed for context.
        share_line = next(l for l in untriaged.splitlines() if "Public share links" in l)
        self.assertIn("t0002", share_line)

    def test_unprioritized_open_task_is_untriaged(self):
        out = _run_backlog(self.root).stdout
        untriaged = out.split("Untriaged:")[1]
        self.assertIn("t0002", untriaged)

    def test_terminal_and_archived_tasks_excluded(self):
        out = _run_backlog(self.root).stdout
        self.assertNotIn("t0003", out)
        self.assertNotIn("t0005", out)
        # t0003's priority must not lift s0003's marker.
        triaged = out.split("Untriaged:")[0]
        self.assertNotIn("Public share links", triaged)

    def test_marker_excerpt_strips_token_and_list_markup(self):
        out = _run_backlog(self.root).stdout
        line = next(l for l in out.splitlines() if "Batch import" in l)
        self.assertNotIn("UNIMPLEMENTED", line)
        self.assertNotIn("- ", line.split("Batch import")[0])


@unittest.skipUnless(_script_available, _missing_reason)
class TestBacklogEmpty(unittest.TestCase):
    def test_empty_worklog_prints_none(self):
        with tempfile.TemporaryDirectory() as root:
            make_worklog(root)
            result = _run_backlog(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("(none)", result.stdout)


if __name__ == "__main__":
    unittest.main()
