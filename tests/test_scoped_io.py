"""Action-scope regressions: unrelated records must not become I/O or diagnostic dependencies."""

import io
import json
import sys
import tempfile
import unittest
from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "plugin/skills/worklog/scripts"
sys.path.insert(0, str(SCRIPTS))
from worklog import main
from worklog_lib.initialization import initialize


class ScopedIOTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.project = Path(temporary.name)
        self.root = self.project / "worklog"
        initialize(self.project)

    def entity(self, kind, identity, fields=None, archived=False):
        fields = {"id": identity, "title": "Example", **(fields or {})}
        if kind == "task":
            fields.setdefault("status", "pending")
            fields.setdefault("modifies", [])
        path = self.root / ("archive/task" if archived else kind) / f"{identity}-example.md"
        path.write_text("+++\n" + "\n".join(f"{key} = {json.dumps(value)}" for key, value in fields.items()) + "\n+++\nBody\n", encoding="utf-8")
        return path

    def invoke(self, *args, readable=None):
        output, errors, reads = io.StringIO(), io.StringIO(), Counter()
        original_open = Path.open

        def guarded_open(path, mode="r", *rest, **kwargs):
            if "r" in mode or "+" in mode:
                reads[path] += 1
                if readable is not None and path not in readable:
                    raise AssertionError(f"Unnecessary read: {path}")
            return original_open(path, mode, *rest, **kwargs)

        with patch.object(Path, "open", guarded_open), redirect_stdout(output), redirect_stderr(errors):
            code = main([*args, "--project", str(self.project)])
        return code, output.getvalue(), errors.getvalue(), reads

    def test_create_reserves_existing_ids_without_reading_their_bodies(self):
        self.entity("task", "t0040").write_text("unreadable metadata")
        self.entity("task", "t0050", archived=True).write_text("unreadable metadata")
        (self.root / "ref/broken.md").write_text("not an entity")
        (self.root / "tags.csv").write_text("broken database")
        code, output, errors, _ = self.invoke("create", "task", "Next", readable={self.root / "project.toml"})
        self.assertEqual((code, errors), (0, ""))
        self.assertIn("t0051", output)
        self.assertTrue((self.root / "task/t0051-next.md").exists())
        self.assertNotIn("database", output.lower())
        self.assertNotIn("broken", output)

    def test_scalar_noop_reads_only_target_and_policy_once(self):
        target = self.entity("note", "n0001", {"tags": ["old"]})
        (self.root / "tags.csv").write_text("broken database")
        (self.root / "ref/broken.md").write_text("not an entity")
        before = target.stat().st_mtime_ns
        code, output, errors, reads = self.invoke("field", "set", "n1", "--field", "title", "--value", "Example",
                                                   readable={target, self.root / "project.toml"})
        self.assertEqual((code, errors), (0, ""))
        self.assertEqual(reads[target], 1)
        self.assertEqual(target.stat().st_mtime_ns, before)
        self.assertNotIn("database", output.lower())

    def test_finish_reads_only_target_blocker_and_governing_spec(self):
        spec = self.entity("spec", "s0001")
        blocker = self.entity("task", "t0002", {"status": "done"}, archived=True)
        target = self.entity("task", "t0001", {"status": "active", "modifies": ["s0001"], "blocked_by": ["t0002"]})
        self.entity("task", "t0003").write_text("broken unrelated task")
        (self.root / "ref/broken.md").write_text("broken reference")
        code, _, errors, reads = self.invoke("task", "finish", "t1", readable={spec, blocker, target, self.root / "project.toml"})
        self.assertEqual((code, errors), (0, ""))
        self.assertFalse(target.exists())
        self.assertTrue((self.root / "archive/task" / target.name).exists())
        self.assertLessEqual(reads[target], 2)  # Initial read and optimistic write preflight.
        self.assertEqual(reads[spec], 1)
        self.assertEqual(reads[blocker], 1)

    def test_selected_status_omits_unrelated_diagnostics_and_reference_reads(self):
        selected_spec = self.entity("spec", "s0001")
        selected_task = self.entity("task", "t0001", {"modifies": ["s0001"]})
        unrelated = self.entity("spec", "s0002", {"parent": "missing", "paths": 7})
        broken = self.entity("note", "n0001")
        broken.write_text("malformed unrelated note")
        (self.root / "ref/broken.md").write_text("malformed unrelated reference")
        (self.root / "tags.csv").write_text("broken database")
        allowed = {selected_spec, selected_task, unrelated, broken, self.root / "project.toml"}
        code, output, errors, reads = self.invoke("status", "t1", readable=allowed)
        self.assertEqual((code, errors), (0, ""))
        self.assertIn("s0001", output)
        self.assertIn("t0001", output)
        self.assertNotIn("s0002", output)
        self.assertNotIn("n0001", output)
        self.assertNotIn("database", output.lower())
        self.assertTrue(all(count == 1 for count in reads.values()))

    def test_explicit_reference_scope_reports_its_own_failure_only(self):
        reference = self.root / "ref/broken.md"
        reference.write_text("not a fenced reference")
        self.entity("task", "t0001").write_text("unrelated task error")
        code, _, errors, _ = self.invoke("status", "--path", "worklog/ref/broken.md", readable={reference})
        self.assertEqual(code, 1)
        self.assertIn("broken.md", errors)
        self.assertNotIn("t0001", errors)

    def test_selected_reference_reports_forbidden_hierarchy(self):
        reference = self.root / "ref/source.md"
        reference.write_text('+++\ntitle = "Source"\nparent = "n0001"\n+++\nCopied text\n')
        code, _, errors, _ = self.invoke("status", "--path", "worklog/ref/source.md", readable={reference})
        self.assertEqual(code, 1)
        self.assertIn("parent", errors)

    def test_explicit_entity_modes_do_not_read_project_policy(self):
        (self.root / "project.toml").write_text("broken inherited policy")
        for kind, identity, args in (
            ("note", "n0001", ("field", "set", "n1", "--field", "title", "--value", "Changed")),
            ("task", "t0001", ("task", "start", "t1")),
        ):
            with self.subTest(kind=kind):
                target = self.entity(kind, identity, {"agent_mode": "autonomous"})
                code, _, errors, _ = self.invoke(*args, readable={target})
                self.assertEqual((code, errors), (0, ""))
                expected = '"Changed"' if kind == "note" else '"active"'
                self.assertIn(expected, target.read_text())

    def test_invalid_policy_section_fails_only_its_dependent_target(self):
        inherited = self.entity("note", "n0001")
        valid = self.entity("task", "t0001")
        (self.root / "project.toml").write_text('note = "invalid policy table"\n[task]\nagent_mode = "draft"\n')
        code, _, _, _ = self.invoke("field", "set", "n1", "t1", "--field", "title", "--value", "Changed")
        self.assertEqual(code, 1)
        self.assertIn('"Example"', inherited.read_text())
        self.assertIn('"Changed"', valid.read_text())

    def test_database_only_tag_actions_do_not_read_entities_or_configuration(self):
        database = self.root / "tags.csv"
        (self.root / "project.toml").write_text("malformed policy")
        (self.root / "ref/broken.md").write_text("malformed reference")
        code, _, errors, reads = self.invoke("tag", "add", "work", readable={database})
        self.assertEqual((code, errors), (0, ""))
        self.assertLessEqual(reads[database], 2)
        code, _, errors, reads = self.invoke("tag", "update", "work", "--description", "Updated", readable={database})
        self.assertEqual((code, errors), (0, ""))
        self.assertLessEqual(reads[database], 2)
        self.assertIn("work,Updated", database.read_text())

    def test_complete_init_does_not_read_entity_files(self):
        (self.root / "ref/broken.md").write_text("malformed reference")
        self.entity("task", "t0001").write_text("malformed task")
        original_open = Path.open
        allowed = {self.root / "project.toml", self.root / "tags.csv"}

        def guarded_open(path, mode="r", *rest, **kwargs):
            self.assertIn(path, allowed)
            self.assertIn("r", mode)
            return original_open(path, mode, *rest, **kwargs)

        with patch.object(Path, "open", guarded_open):
            result = initialize(self.project)
        self.assertEqual(result.created, [])


if __name__ == "__main__":
    unittest.main()
