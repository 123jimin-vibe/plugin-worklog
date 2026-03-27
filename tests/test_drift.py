# @worklog s0017
"""Tests for plugin/skills/worklog/script/drift.py — spec-code drift detection."""

import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

_SCRIPT_PATH = (
    pathlib.Path(__file__).resolve().parents[1]
    / "plugin" / "skills" / "worklog" / "script" / "drift.py"
)
_script_available = _SCRIPT_PATH.is_file()
_missing_reason = "drift.py not found"


# ===================================================================
# Helpers
# ===================================================================

def _git(cwd, *args):
    """Run a git command in *cwd* and return CompletedProcess."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd, capture_output=True, text=True,
    )


def _make_git_worklog(root):
    """Create a worklog inside a fresh git repo with an initial commit."""
    root = pathlib.Path(root)
    _git(str(root), "init")
    _git(str(root), "config", "user.email", "test@test.com")
    _git(str(root), "config", "user.name", "Test")

    worklog = root / "worklog"
    for d in ["spec", "task", "decision", "archive/task"]:
        (worklog / d).mkdir(parents=True, exist_ok=True)
    return str(worklog)


def _write_spec_with_paths(worklog, spec_id, title, paths, tags=None):
    """Write a spec entity with a paths field and return its file path."""
    if tags is None:
        tags = ["misc"]
    filename = f"{spec_id}-{title.lower().replace(' ', '-')}.md"
    filepath = pathlib.Path(worklog) / "spec" / filename
    lines = [
        "+++",
        f'id = "{spec_id}"',
        f'title = "{title}"',
        f"tags = {tags}",
        f"paths = {paths}",
        "+++",
    ]
    filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(filepath)


def _write_spec_without_paths(worklog, spec_id, title, tags=None):
    """Write a spec entity without a paths field."""
    if tags is None:
        tags = ["misc"]
    filename = f"{spec_id}-{title.lower().replace(' ', '-')}.md"
    filepath = pathlib.Path(worklog) / "spec" / filename
    lines = [
        "+++",
        f'id = "{spec_id}"',
        f'title = "{title}"',
        f"tags = {tags}",
        "+++",
    ]
    filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return str(filepath)


def _run_drift(worklog_root, *extra_args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT_PATH), "-w", worklog_root, *extra_args],
        capture_output=True, text=True,
    )


# ===================================================================
# No drift
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestDriftNone(unittest.TestCase):
    """When spec paths have not changed since the spec commit, no drift."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_clean(self):
        worklog = _make_git_worklog(self.tmpdir)
        root = self.tmpdir

        # Create a source file and a spec that governs it.
        src_dir = pathlib.Path(root) / "src" / "auth"
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / "login.py").write_text("# login\n")

        _write_spec_with_paths(worklog, "s0001", "Auth", '["src/auth/**"]')

        # Commit everything together.
        _git(root, "add", "-A")
        _git(root, "commit", "-m", "initial")

        result = _run_drift(worklog)
        self.assertEqual(result.returncode, 0)
        # Output should not mention s0001 as drifted.
        self.assertNotIn("drift", result.stdout.lower())


# ===================================================================
# Drift present
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestDriftPresent(unittest.TestCase):
    """Source file changed after spec commit — drift is reported."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_source_changed_after_spec(self):
        worklog = _make_git_worklog(self.tmpdir)
        root = self.tmpdir

        src_dir = pathlib.Path(root) / "src" / "auth"
        src_dir.mkdir(parents=True, exist_ok=True)
        src_file = src_dir / "login.py"
        src_file.write_text("# login v1\n")

        _write_spec_with_paths(worklog, "s0001", "Auth", '["src/auth/**"]')

        _git(root, "add", "-A")
        _git(root, "commit", "-m", "initial")

        # Now change the source file without touching the spec.
        src_file.write_text("# login v2 - changed\n")
        _git(root, "add", "-A")
        _git(root, "commit", "-m", "change source")

        result = _run_drift(worklog)
        output = result.stdout + result.stderr
        self.assertIn("s0001", output)


# ===================================================================
# No paths field — skipped
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestDriftNoPathsField(unittest.TestCase):
    """Specs without a paths field are silently skipped."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_skipped(self):
        worklog = _make_git_worklog(self.tmpdir)
        root = self.tmpdir

        _write_spec_without_paths(worklog, "s0001", "Conceptual")

        _git(root, "add", "-A")
        _git(root, "commit", "-m", "initial")

        result = _run_drift(worklog)
        self.assertEqual(result.returncode, 0)
        # s0001 should not appear in drift output.
        self.assertNotIn("s0001", result.stdout)


# ===================================================================
# Spec never committed
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestDriftSpecNeverCommitted(unittest.TestCase):
    """A spec file not yet in git history is handled gracefully."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_uncommitted_spec(self):
        worklog = _make_git_worklog(self.tmpdir)
        root = self.tmpdir

        # Initial commit with nothing.
        placeholder = pathlib.Path(root) / ".gitkeep"
        placeholder.write_text("")
        _git(root, "add", "-A")
        _git(root, "commit", "-m", "initial")

        # Add spec but don't commit.
        _write_spec_with_paths(worklog, "s0001", "New", '["src/**"]')

        result = _run_drift(worklog)
        # Should not crash.
        self.assertIn(result.returncode, (0, 1),
                       f"Unexpected exit code {result.returncode}.\n"
                       f"stderr: {result.stderr}")


# ===================================================================
# Glob patterns with **
# ===================================================================

@unittest.skipUnless(_script_available, _missing_reason)
class TestDriftGlobPatterns(unittest.TestCase):
    """Paths with ** wildcards are expanded correctly by git diff."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_recursive_glob(self):
        worklog = _make_git_worklog(self.tmpdir)
        root = self.tmpdir

        # Create nested source files.
        deep_dir = pathlib.Path(root) / "src" / "auth" / "providers"
        deep_dir.mkdir(parents=True, exist_ok=True)
        deep_file = deep_dir / "oauth.py"
        deep_file.write_text("# oauth v1\n")

        _write_spec_with_paths(worklog, "s0001", "Auth", '["src/auth/**"]')

        _git(root, "add", "-A")
        _git(root, "commit", "-m", "initial")

        # Change deeply nested file.
        deep_file.write_text("# oauth v2\n")
        _git(root, "add", "-A")
        _git(root, "commit", "-m", "change deep file")

        result = _run_drift(worklog)
        output = result.stdout + result.stderr
        self.assertIn("s0001", output)


if __name__ == "__main__":
    unittest.main()
