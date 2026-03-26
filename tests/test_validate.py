# @worklog s0017
"""Tests for plugin/skills/worklog/script/validate.py — worklog validation."""

import os
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
    / "plugin" / "skills" / "worklog" / "script" / "validate.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "validate.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _run_validate(worklog_root, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


def _populate_clean_worklog(root):
    """Write a minimal valid worklog with one spec, task, decision, and tags."""
    write_tags(root, ["auth", "tooling"])
    write_entity(root, "s0001", {
        "id": "s0001", "title": "Auth", "tags": ["auth"],
    })
    write_entity(root, "t0001", {
        "id": "t0001", "title": "Add login", "tags": ["auth"],
        "status": "pending", "modifies": ["s0001"],
    })
    write_entity(root, "d0001", {
        "id": "d0001", "title": "Use JWT",
        "relates_to": ["s0001"],
    })


# ===================================================================
# Clean worklog
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateClean(unittest.TestCase):
    """A valid worklog passes with exit 0 and no error output."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_clean(self):
        _populate_clean_worklog(self.worklog)
        result = _run_validate(self.worklog)
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0, got {result.returncode}.\n"
                         f"stdout: {result.stdout}\nstderr: {result.stderr}")


# ===================================================================
# Malformed TOML
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateMalformedToml(unittest.TestCase):
    """Missing closing +++ fence is reported."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_missing_closing_fence(self):
        _populate_clean_worklog(self.worklog)
        broken = os.path.join(self.worklog, "spec", "s0099-broken.md")
        with open(broken, "w", encoding="utf-8") as f:
            f.write('+++\nid = "s0099"\ntitle = "Broken"\n')

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("s0099", output)


# ===================================================================
# Missing required field
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateMissingField(unittest.TestCase):
    """A task without 'status' is reported with field name and file."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_task_missing_status(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "No status", "tags": ["misc"],
            "modifies": ["s0001"],
            # status intentionally omitted
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("status", output)
        self.assertIn("t0001", output)


# ===================================================================
# Bad ID format
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateBadIdFormat(unittest.TestCase):
    """An ID like s00a1 is reported as a format violation."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_non_numeric_id(self):
        write_tags(self.worklog, ["misc"])
        path = os.path.join(self.worklog, "spec", "s00a1-bad.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write('+++\nid = "s00a1"\ntitle = "Bad"\ntags = ["misc"]\n+++\n')

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("s00a1", output)


# ===================================================================
# Filename/ID mismatch
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateFilenameMismatch(unittest.TestCase):
    """Filename starting with wrong ID is reported."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_id_filename_mismatch(self):
        write_tags(self.worklog, ["misc"])
        # File named t0002-foo.md but ID says t0003.
        path = os.path.join(self.worklog, "task", "t0002-foo.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                '+++\n'
                'id = "t0003"\n'
                'title = "Foo"\n'
                'tags = ["misc"]\n'
                'status = "pending"\n'
                'modifies = ["s0001"]\n'
                '+++\n'
            )
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        # Should mention the mismatch (either ID or filename).
        self.assertTrue("t0003" in output or "t0002" in output,
                        f"Expected mismatch reported, got:\n{output}")


# ===================================================================
# Invalid status
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateInvalidStatus(unittest.TestCase):
    """A status value not in the allowed set is reported."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_status_wip(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Bad status", "tags": ["misc"],
            "status": "wip", "modifies": ["s0001"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("wip", output)


# ===================================================================
# Dangling references
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateDanglingModifies(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_modifies_nonexistent_spec(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Dangling", "tags": ["misc"],
            "status": "pending", "modifies": ["s9999"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("s9999", output)


@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateDanglingBlockedBy(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_blocked_by_nonexistent_task(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Blocked", "tags": ["misc"],
            "status": "blocked", "modifies": ["s0001"],
            "blocked_by": ["t9999"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("t9999", output)


@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateDanglingRelatesTo(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_relates_to_nonexistent_spec(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "d0001", {
            "id": "d0001", "title": "Decision",
            "relates_to": ["s9999"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("s9999", output)


@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateDanglingSupersedes(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_supersedes_nonexistent_decision(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "d0002", {
            "id": "d0002", "title": "Superseder",
            "relates_to": ["s0001"],
            "supersedes": ["d9999"],
        })
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("d9999", output)


# ===================================================================
# Unknown tag
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateUnknownTag(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_tag_not_in_tags_md(self):
        write_tags(self.worklog, ["auth"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["nonexistent"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("nonexistent", output)


# ===================================================================
# Duplicate IDs
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateDuplicateIds(unittest.TestCase):

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_two_files_same_id(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "First", "tags": ["misc"],
        })
        # Second file with same ID but different filename.
        path = os.path.join(self.worklog, "spec", "s0001-duplicate.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                '+++\n'
                'id = "s0001"\n'
                'title = "Duplicate"\n'
                'tags = ["misc"]\n'
                '+++\n'
            )

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        self.assertIn("s0001", output)


# ===================================================================
# Archived entity refs are valid
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateArchivedRefValid(unittest.TestCase):
    """blocked_by pointing to an archived task is not an error."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_blocked_by_archived_task(self):
        write_tags(self.worklog, ["misc"])
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })
        write_entity(self.worklog, "t0004", {
            "id": "t0004", "title": "Done task", "tags": ["misc"],
            "status": "done", "modifies": ["s0001"],
        }, subdir="archive/task")
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Active", "tags": ["misc"],
            "status": "blocked", "modifies": ["s0001"],
            "blocked_by": ["t0004"],
        })

        result = _run_validate(self.worklog)
        self.assertEqual(result.returncode, 0,
                         f"Expected exit 0, got {result.returncode}.\n"
                         f"stdout: {result.stdout}\nstderr: {result.stderr}")


# ===================================================================
# Multiple errors — all reported
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestValidateMultipleErrors(unittest.TestCase):
    """Multiple errors in different files are all reported, not just the first."""

    def setUp(self):
        self.worklog = tempfile.mkdtemp()
        make_worklog(self.worklog)

    def tearDown(self):
        shutil.rmtree(self.worklog, ignore_errors=True)

    def test_reports_all_errors(self):
        write_tags(self.worklog, ["misc"])
        # Error 1: dangling modifies.
        write_entity(self.worklog, "t0001", {
            "id": "t0001", "title": "Dangling mod", "tags": ["misc"],
            "status": "pending", "modifies": ["s9999"],
        })
        # Error 2: invalid status.
        write_entity(self.worklog, "t0002", {
            "id": "t0002", "title": "Bad status", "tags": ["misc"],
            "status": "wip", "modifies": ["s0001"],
        })
        write_entity(self.worklog, "s0001", {
            "id": "s0001", "title": "Spec", "tags": ["misc"],
        })

        result = _run_validate(self.worklog)
        self.assertNotEqual(result.returncode, 0)
        output = result.stdout + result.stderr
        # Both errors should be present.
        self.assertIn("s9999", output)
        self.assertIn("wip", output)


if __name__ == "__main__":
    unittest.main()
