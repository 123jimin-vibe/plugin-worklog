"""Initialization workflows through the shipped entry point."""

import csv
import io
import shutil
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "plugin/skills/worklog/scripts"
sys.path.insert(0, str(SCRIPTS))

from worklog_lib.initialization import initialize


def snapshot(root):
    return {str(p.relative_to(root)): (p.read_bytes(), p.stat().st_mtime_ns) if p.is_file() else None
            for p in root.rglob("*")}


class InitTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "project with spaces"
        self.project.mkdir()
        self.root = self.project / "worklog"

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
        return path

    def run_cli(self, *args, cwd=None, script=None):
        return subprocess.run([sys.executable, str(script or SCRIPTS / "worklog.py"), *args],
                              cwd=cwd or self.project, capture_output=True, text=True, encoding="utf-8")

    def test_new_project_and_idempotence(self):
        result = self.run_cli("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Worklog initialized.", result.stdout)
        self.assertIn(str(self.project), result.stdout)
        for directory in ("spec", "task", "note", "ref", "decision", "archive/task"):
            self.assertTrue((self.root / directory).is_dir())
        config_text = (self.root / "project.toml").read_text()
        config = tomllib.loads(config_text)
        self.assertEqual(config, {"spec": {"agent_mode": "propose"},
                                  "task": {"agent_mode": "draft"}, "note": {"agent_mode": "draft"}})
        self.assertIn("read-only", config_text)
        self.assertIn("NEEDS APPROVAL", config_text)
        self.assertIn("approval", config_text)
        self.assertEqual(list(csv.reader(io.StringIO((self.root / "tags.csv").read_text()))),
                         [["tag", "description"]])
        self.assertFalse(list(self.root.rglob("*.md")))
        self.assertFalse((self.project / ".git").exists())
        before = snapshot(self.project)
        again = self.run_cli("init", str(self.project))
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("Worklog already initialized.", again.stdout)
        self.assertIn("Existing:", again.stdout)
        self.assertEqual(snapshot(self.project), before)

    def test_partial_worklog_seeds_all_entity_types_and_preserves_files(self):
        for kind, identity in (("spec", "s0001"), ("task", "t0001"), ("note", "n0001"),
                               ("decision", "d0001"), ("archive/task", "t0002")):
            subdir = "" if kind == "archive/task" else "nested/"
            self.write(f"{kind}/{subdir}{identity}-entity.md",
                       f'+++\nid = "{identity}"\ntitle = "Title"\ntags = [" {kind.upper()} ", "Straße"]\n+++\nBody\n')
        self.write("ref/source/excerpt.md", '+++\ntitle = "Reference"\ntags = ["REF"]\n+++\nCopied body\n')
        self.write("project.toml", '# User configuration\n[spec]\nagent_mode = "autonomous"\n')
        before = snapshot(self.project)
        result = self.run_cli("init", str(self.project))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Worklog structure completed.", result.stdout)
        for name, value in before.items():
            self.assertEqual(snapshot(self.project)[name], value)
        rows = list(csv.reader(io.StringIO((self.root / "tags.csv").read_text())))
        expected = sorted(["spec", "task", "note", "decision", "archive/task", "strasse", "ref"])
        self.assertEqual(rows, [["tag", "description"]] + [[tag, ""] for tag in expected])

    def test_valid_database_quoted_descriptions_and_advisory_tags_are_preserved(self):
        self.write("tags.csv", 'tag,description\r\nUnused,"comma, quote "" and\nline"\r\n')
        self.write("note/n0001-note.md", '+++\nid = "n0001"\ntitle = "Note"\ntags = ["unknown"]\n+++\n')
        before = snapshot(self.project)
        result = self.run_cli("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        after = snapshot(self.project)
        for name, value in before.items():
            self.assertEqual(after[name], value)

    def test_structural_conflicts_are_all_reported_before_writes(self):
        self.write("spec", "occupied")
        self.write("archive", "occupied")
        (self.root / "project.toml").mkdir()
        (self.root / "tags.csv").mkdir()
        before = snapshot(self.project)
        result = self.run_cli("init")
        self.assertNotEqual(result.returncode, 0)
        for name in ("spec", "archive", "project.toml", "tags.csv"):
            self.assertIn(str(self.root / name), result.stderr)
        self.assertEqual(snapshot(self.project), before)

    def test_worklog_file_conflict_and_nonexistent_project(self):
        self.root.write_text("occupied")
        before = snapshot(self.project)
        self.assertNotEqual(self.run_cli("init").returncode, 0)
        self.assertEqual(snapshot(self.project), before)
        missing = self.project / "missing"
        self.assertNotEqual(self.run_cli("init", str(missing)).returncode, 0)
        self.assertFalse(missing.exists())

    def test_invalid_databases_fail_without_partial_changes(self):
        for text in ("", "description,tag\n", "tag,description,extra\n", "tag,description\na\n",
                     "tag,description\na,b,c\n", 'tag,description\na,"unclosed\n',
                     "tag,description\n ,empty\n", "tag,description\nStraße,a\nSTRASSE,b\n"):
            with self.subTest(text=text):
                self.write("tags.csv", text)
                before = snapshot(self.project)
                result = self.run_cli("init")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(snapshot(self.project), before)

    def test_duplicate_entity_tags_prevent_seeding_a_missing_database(self):
        self.write("task/t0001-task.md", '+++\nid = "t0001"\ntitle = "Task"\ntags = [" X ", "x"]\n+++\n')
        before = snapshot(self.project)
        result = self.run_cli("init")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)

    def test_invalid_entity_cannot_be_silently_omitted_from_seed(self):
        self.write("note/n0001-note.md", '+++\nid = "n0001"\ntitle = "Note"\ntags = [" "]\n+++\n')
        before = snapshot(self.project)
        result = self.run_cli("init")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)

    def test_failure_during_second_file_creation_rolls_back_only_new_paths(self):
        self.write("note/n0001-note.md", '+++\nid = "n0001"\ntitle = "Note"\n+++\nBody\n')
        before = snapshot(self.project)
        real_open = Path.open

        def fail_tags(path, mode="r", *args, **kwargs):
            if path.name == "tags.csv" and "x" in mode:
                raise OSError("injected write failure")
            return real_open(path, mode, *args, **kwargs)

        with patch.object(Path, "open", fail_tags), self.assertRaises(OSError):
            initialize(self.project)
        self.assertEqual(snapshot(self.project), before)

    def test_shipped_plugin_runs_without_repository_and_only_adds_bytecode(self):
        isolated = Path(self.temp.name) / "plugin copy"
        shutil.copytree(SCRIPTS, isolated, ignore=shutil.ignore_patterns("__pycache__"))
        before = snapshot(isolated)
        result = self.run_cli("init", script=isolated / "worklog.py")
        self.assertEqual(result.returncode, 0, result.stderr)
        after = snapshot(isolated)
        for name, value in before.items():
            self.assertEqual(after[name], value)
        for name in after.keys() - before.keys():
            path = Path(name)
            self.assertIn("__pycache__", path.parts)
            if after[name] is not None:
                self.assertEqual(path.suffix, ".pyc")

    def test_help_and_unknown_commands_do_not_change_project(self):
        for args in (("--help",), ("init", "--help"), ("tag",)):
            with self.subTest(args=args):
                self.run_cli(*args)
                self.assertEqual(snapshot(self.project), {})

    def test_partial_file_write_failure_removes_new_worklog(self):
        real_open = Path.open

        class FailedWrite:
            def __init__(self, stream):
                self.stream = stream

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.stream.close()

            def write(self, content):
                self.stream.write(content[:12])
                raise OSError("injected failure after partial write")

        def fail_write(path, mode="r", *args, **kwargs):
            stream = real_open(path, mode, *args, **kwargs)
            return FailedWrite(stream) if mode == "xb" else stream

        with patch.object(Path, "open", fail_write), self.assertRaises(OSError):
            initialize(self.project)
        self.assertEqual(snapshot(self.project), {})

    def test_invalid_configuration_is_preserved_on_failure(self):
        for content in ('[spec]\nagent_mode = "invalid"\n', 'spec = 2\n', '[spec\n'):
            with self.subTest(content=content):
                self.write("project.toml", content)
                before = snapshot(self.project)
                result = self.run_cli("init")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(snapshot(self.project), before)

    def test_nested_directory_link_cannot_silently_hide_entity_tags(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "n0001-note.md").write_text('+++\nid = "n0001"\ntitle = "Note"\ntags = ["linked"]\n+++\n')
        (self.root / "note").mkdir(parents=True)
        try:
            (self.root / "note/linked").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Directory symlinks unavailable: {exc}")
        before = snapshot(self.project)
        result = self.run_cli("init")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)
        self.assertFalse((self.root / "tags.csv").exists())


if __name__ == "__main__":
    unittest.main()
