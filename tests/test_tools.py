"""Command workflows and preservation checks derived from tool specifications."""

import csv
import io
import json
import argparse
import os
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
from worklog_lib.entities import read_entity
from worklog_lib.context import Context, find_cycle
from worklog_lib.tag_command import run_tag
from worklog_lib.task_command import run_task
from worklog_lib.editing import edit_fields
from worklog_lib.markers import markers


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.root = self.project / "worklog"
        self.script = SCRIPTS / "worklog.py"
        self.run_tool("init")

    def run_tool(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(self.script), *args],
                                cwd=self.project, capture_output=True, text=True, encoding="utf-8")
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result.stdout + result.stderr

    def entity(self, kind, identity=None, fields=None, body="\nBody stays intact.\n", archived=False):
        fields = {"title": "Example", **(fields or {})}
        if identity:
            fields = {"id": identity, **fields}
        if kind == "task":
            fields.setdefault("status", "pending")
            fields.setdefault("modifies", [])
        path = self.root / ("archive/task" if archived else kind) / (f"{identity}-example.md" if identity else "source.md")
        path.parent.mkdir(parents=True, exist_ok=True)
        text = "+++\n" + "\n".join(f"{key} = {json.dumps(value)}" for key, value in fields.items()) + "\n+++\n" + body
        path.write_text(text, encoding="utf-8", newline="")
        return path

    def files(self):
        return {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_tag_database_and_rename_every_reference(self):
        self.run_tool("tag", "add", " Straße ", "--description", 'comma, "quote"\nline')
        paths = [self.entity("spec", "s0001", {"tags": ["STRASSE"]}),
                 self.entity("task", "t0001", {"tags": ["Straße"]}, archived=True),
                 self.entity("ref", fields={"tags": ["strasse"]}),
                 self.entity("decision", "d0001", {"tags": ["strasse"], "relates_to": ["s0001"]})]
        bodies = [p.read_bytes().split(b"+++", 2)[2] for p in paths]
        report = self.run_tool("tag", "update", "STRASSE", "--name", "new")
        for p, body in zip(paths, bodies):
            self.assertIn(p.name, report)
            self.assertEqual(p.read_bytes().split(b"+++", 2)[2], body)
            self.assertIn('"new"', p.read_text())
        rows = list(csv.reader(io.StringIO((self.root / "tags.csv").read_text())))
        self.assertEqual(rows[1], ["new", 'comma, "quote"\nline'])
        before = self.files()
        report = self.run_tool("tag", "remove", "NEW", ok=False)
        for p in paths:
            self.assertIn(p.name, report)
        self.assertEqual(self.files(), before)

    def test_tag_rename_collision_preflights_every_file(self):
        self.run_tool("tag", "add", "old")
        self.entity("note", "n0001", {"tags": ["old", "unknown"]})
        before = self.files()
        self.run_tool("tag", "update", "old", "--name", "unknown", ok=False)
        self.assertEqual(self.files(), before)
        self.assertIn("unknown", self.run_tool("tag", "list"))

    def test_tag_rename_ignores_unrelated_reference_metadata_defects(self):
        self.run_tool("tag", "add", "old")
        reference = self.root / "ref" / "source.md"
        reference.write_text('+++\nid = ["not", "an", "id"]\ntitle = 7\ntags = ["old"]\n+++\nSource.\n')
        self.run_tool("tag", "update", "old", "--name", "new")
        header, body = reference.read_text().split("+++", 2)[1:]
        self.assertEqual(tomllib.loads(header), {"id": ["not", "an", "id"], "title": 7, "tags": ["new"]})
        self.assertEqual(body, "\nSource.\n")

    def test_tag_list_retains_database_rows_when_usage_is_incomplete(self):
        self.run_tool("tag", "add", "known", "--description", "Preserved description")
        reference = self.root / "ref" / "broken.md"
        reference.write_text("Unreadable metadata")
        before = self.files()
        report = self.run_tool("tag", "list", ok=False)
        self.assertIn("known", report)
        self.assertIn("Preserved description", report)
        self.assertIn(reference.name, report)
        self.assertNotIn("unused", report.lower())
        self.assertEqual(self.files(), before)

    def test_create_rejects_forward_relationship_to_its_new_identity(self):
        self.entity("note", "n0001", {"parent": "n2"})
        before = self.files()
        self.run_tool("create", "note", "Cycle", "--parent", "n1", ok=False)
        self.assertEqual(self.files(), before)

    def test_tag_requires_database_and_update_argument(self):
        self.run_tool("tag", "add", "unused")
        self.assertIn("unused", self.run_tool("tag", "list"))
        self.run_tool("tag", "update", "unused", ok=False)
        self.run_tool("tag", "remove", "unused")
        (self.root / "tags.csv").unlink()
        self.run_tool("tag", "list", ok=False)

    def test_create_uses_archive_ids_minimal_fields_and_independent_results(self):
        self.entity("task", "t0009", {"status": "done"}, archived=True)
        report = self.run_tool("create", "task", "First", "Second", "--tag", " New ")
        self.assertIn("t0010", report)
        self.assertIn("t0011", report)
        created = list((self.root / "task").glob("*.md"))
        self.assertEqual(len(created), 2)
        for path in created:
            entity = read_entity(path, "task")
            self.assertEqual(entity.fields["status"], "pending")
            self.assertEqual(entity.fields["tags"], ["new"])
            self.assertIn("NEEDS APPROVAL", entity.body)
        report = self.run_tool("create", "note", "", "Valid", ok=False)
        self.assertIn("Valid", report)
        self.assertEqual(len(list((self.root / "note").glob("*.md"))), 1)
        before = self.files()
        self.run_tool("create", "note", "Invalid", "--modifies", "s01", ok=False)
        self.assertEqual(before, self.files())

    def test_field_preserves_comments_body_and_nested_metadata(self):
        path = self.entity("note", "n0001")
        path.write_bytes(b'+++\r\nid = "n0001"\r\ntitle = "Example" # keep\r\n"tags" = [\r\n "old", # why\r\n]\r\n[custom]\r\nvalue = "keep"\r\n+++\r\n  Body\r\n')
        self.run_tool("field", "set", "n1", "--field", "title", "--value", "Changed")
        self.run_tool("field", "add", "n01", "--field", "tags", "--value", " NEW ")
        self.run_tool("field", "set", "n01", "--field", "parent", "--value", "n01", ok=False)
        text = path.read_bytes()
        self.assertIn(b'# keep', text)
        self.assertIn(b'# why', text)
        self.assertIn(b'[custom]\r\nvalue = "keep"', text)
        self.assertTrue(text.endswith(b'  Body\r\n'))
        self.assertEqual(read_entity(path, "note").fields["tags"], ["old", "new"])

    def test_field_protected_fields_and_independent_results(self):
        path = self.entity("note", "n0001")
        for name in ("id", "status", "agent_mode"):
            before = self.files()
            self.run_tool("field", "set", "n01", "--field", name, "--value", "x", ok=False)
            self.assertEqual(before, self.files())
        report = self.run_tool("field", "set", "n999", "n01", "--field", "title", "--value", "Changed", ok=False)
        self.assertIn("n0001", report)
        self.assertEqual(read_entity(path, "note").fields["title"], "Changed")

    def test_hierarchy_and_dependencies_are_separate_and_include_archives(self):
        parent = self.entity("task", "t0001", {"status": "done"}, archived=True)
        child = self.entity("task", "t0002", {"parent": "t1"})
        self.run_tool("task", "start", "t02")
        self.assertEqual(read_entity(child, "task").fields["status"], "active")
        self.entity("task", "t0003", {"blocked_by": ["t2"]})
        before = self.files()
        self.run_tool("field", "add", "t02", "--field", "blocked_by", "--value", "t03", ok=False)
        self.assertEqual(before, self.files())
        self.assertTrue(parent.exists())

    def test_status_is_read_only_and_reports_modes_markers_and_actionability(self):
        self.entity("spec", "s0001", {"paths": ["src/**"]}, body="# Behavior\n\n## Later (UNIMPLEMENTED)\nPending.\n")
        self.entity("task", "t0001", {"modifies": ["s1"], "tags": ["unknown"]})
        self.entity("task", "t0002", {"blocked_by": ["t1"], "parent": "t1", "agent_mode": "read_only"})
        before = self.files()
        report = self.run_tool("status")
        for value in ("s0001", "t0002", "read_only", "UNIMPLEMENTED", "unknown", "start"):
            self.assertIn(value, report)
        self.assertEqual(before, self.files())
        report = self.run_tool("status", "--path", "src/module.py")
        self.assertIn("s0001", report)
        self.assertIn("t0001", report)
        self.run_tool("status", "s999", ok=False)

    def test_task_lifecycle_reason_checks_and_atomic_closure(self):
        path = self.entity("task", "t0001")
        self.run_tool("task", "start", "t1")
        self.run_tool("task", "block", "t1", "--reason", "Service down")
        self.assertIn("Service down", path.read_text())
        self.run_tool("task", "resume", "t1", "--checked", "Service restored")
        self.assertIn("Service restored", path.read_text())
        self.run_tool("task", "finish", "t1")
        self.assertFalse(path.exists())
        archived = self.root / "archive/task" / path.name
        self.assertEqual(read_entity(archived, "task").fields["status"], "done")
        before = self.files()
        self.run_tool("task", "finish", "t1")
        self.assertEqual(before, self.files())
        self.run_tool("task", "start", "t1", ok=False)

    def test_task_review_gates_and_independent_failure(self):
        self.entity("spec", "s0001", body="# Behavior (NEEDS APPROVAL)\nDraft.\n")
        first = self.entity("task", "t0001", {"status": "active", "modifies": ["s01"]})
        second = self.entity("task", "t0002", {"status": "active"})
        self.run_tool("task", "finish", "t1", "t2", ok=False)
        self.assertTrue(first.exists())
        self.assertFalse(second.exists())
        self.run_tool("task", "cancel", "t1", "--reason", "Stopped", ok=False)

    def test_cancel_reason_and_already_resolved_unarchived(self):
        first = self.entity("task", "t0001")
        self.run_tool("task", "cancel", "t1", ok=False)
        self.run_tool("task", "cancel", "t1", "--reason", "No longer needed")
        self.assertFalse(first.exists())
        second = self.entity("task", "t0002", {"status": "cancelled"}, body="Already cancelled.\n")
        self.run_tool("task", "cancel", "t2")
        self.assertFalse(second.exists())

    def test_tag_write_failure_restores_all_files_and_metadata(self):
        self.run_tool("tag", "add", "old")
        self.entity("spec", "s0001", {"tags": ["old"]})
        self.entity("note", "n0001", {"tags": ["old"]})
        before = self.files()
        times = {p: (self.root / p).stat().st_mtime_ns for p in before}
        actual_replace = os.replace
        calls = 0

        def fail_second(source, destination):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected replacement failure")
            return actual_replace(source, destination)

        args = argparse.Namespace(action="update", tag="old", name="new", description=None)
        with patch("worklog_lib.transactions.os.replace", fail_second), self.assertRaises(OSError):
            run_tag(Context(self.project), args)
        self.assertEqual(self.files(), before)
        self.assertEqual({p: (self.root / p).stat().st_mtime_ns for p in before}, times)
        self.assertFalse(list(self.root.rglob(".worklog-*")))

    def test_failed_archive_removal_restores_source_and_removes_destination(self):
        source = self.entity("task", "t0001", {"status": "active"})
        before = self.files()
        actual_unlink = Path.unlink

        def fail_source(path, *args, **kwargs):
            if path == source:
                raise OSError("injected source removal failure")
            return actual_unlink(path, *args, **kwargs)

        args = argparse.Namespace(action="finish", entities=["t1"])
        with patch.object(Path, "unlink", fail_source):
            _, errors = run_task(Context(self.project), args)
        self.assertTrue(errors)
        self.assertEqual(self.files(), before)
        self.assertFalse(list(self.root.rglob(".worklog-*")))

    def test_existing_archive_destination_is_never_overwritten(self):
        source = self.entity("task", "t0001", {"status": "active"})
        context = Context(self.project)
        destination = self.root / "archive/task" / source.name
        context.resolve("t1")
        destination.write_text("appeared after discovery")
        before = self.files()
        _, errors = run_task(context, argparse.Namespace(action="finish", entities=["t1"]))
        self.assertTrue(errors)
        self.assertEqual(self.files(), before)

    def test_mode_precedence_and_missing_optional_tag_database(self):
        (self.root / "project.toml").write_text('[note]\nagent_mode = "autonomous"\n')
        (self.root / "tags.csv").unlink()
        report = self.run_tool("create", "note", "Example", "--tag", " X ")
        self.assertIn("agent_mode=autonomous", report)
        path = next((self.root / "note").glob("*.md"))
        self.assertNotIn("NEEDS APPROVAL", read_entity(path, "note").body)
        self.assertFalse((self.root / "tags.csv").exists())
        self.entity("note", "n0002", {"agent_mode": "read_only"})
        report = self.run_tool("status", "n2")
        self.assertIn("agent_mode=read_only", report)

    def test_field_unset_and_list_remove_preserve_other_fields(self):
        parent = self.entity("note", "n0001")
        child = self.entity("note", "n0002", {"parent": "n1", "tags": ["a", "b"]})
        self.run_tool("field", "remove", "n2", "--field", "tags", "--value", "A")
        self.run_tool("field", "unset", "n2", "--field", "parent")
        fields = read_entity(child, "note").fields
        self.assertNotIn("parent", fields)
        self.assertEqual(fields["tags"], ["b"])
        self.run_tool("field", "unset", "n2", "--field", "title", ok=False)
        self.run_tool("field", "add", "n2", "--field", "title", "--value", "x", ok=False)
        self.assertTrue(parent.exists())

    def test_modes_are_validated_before_a_field_write(self):
        self.entity("note", "n0001", {"agent_mode": "invalid"})
        before = self.files()
        self.run_tool("field", "set", "n1", "--field", "title", "--value", "Changed", ok=False)
        self.assertEqual(before, self.files())

    def test_task_dependencies_gate_start_resume_and_finish(self):
        self.entity("task", "t0001")
        self.entity("task", "t0002", {"blocked_by": ["t1"]})
        self.run_tool("task", "start", "t2", ok=False)
        self.run_tool("task", "block", "t2", "--reason", "Dependency still open")
        self.run_tool("task", "resume", "t2", "--checked", "Checked", ok=False)
        self.run_tool("task", "cancel", "t1", "--reason", "Superseded")
        self.run_tool("task", "resume", "t2", "--checked", "Dependency resolved")
        self.run_tool("task", "finish", "t2")

    def test_markers_ignore_code_examples_but_recognize_review_headings(self):
        body = '# Rules\n\nThe marker `NEEDS APPROVAL` has meaning.\n\n```md\n# NEEDS APPROVAL\n```\n\n## Child (NEEDS REVIEW)\nDraft.\n'
        self.assertEqual([value[0] for value in markers(body)], ["NEEDS REVIEW"])

    def test_graph_cycles_and_deep_acyclic_hierarchy(self):
        edges = {str(i): [str(i + 1)] for i in range(3000)}
        self.assertEqual(find_cycle(edges), [])
        edges["3000"] = ["2998"]
        self.assertEqual(set(find_cycle(edges)), {"2998", "2999", "3000"})

    def test_editing_literal_strings_multiline_values_and_table_insertion(self):
        raw = b"+++\nid = 'n0001'\ntitle = '''Hello\n+++\nWorld'''\n[custom]\nvalue = 'unchanged'\n+++\nBody\n"
        updated = edit_fields(raw, {"title": "Changed", "tags": ["x"]})
        self.assertIn(b"tags = [\"x\"]\n[custom]", updated)
        self.assertIn(b"[custom]\nvalue = 'unchanged'", updated)
        self.assertTrue(updated.endswith(b"+++\nBody\n"))

    def test_complete_workflow_from_an_isolated_plugin_copy(self):
        shipped = self.project / "shipped-scripts"
        shutil.copytree(SCRIPTS, shipped, ignore=shutil.ignore_patterns("__pycache__"))
        self.script = shipped / "worklog.py"
        self.project = self.project / "independent-project"
        self.project.mkdir()
        self.root = self.project / "worklog"
        self.run_tool("init")
        (self.root / "project.toml").write_text('[spec]\nagent_mode = "autonomous"\n')
        self.run_tool("tag", "add", "work")
        self.run_tool("create", "spec", "Behavior", "--paths", "src/**")
        self.run_tool("create", "task", "Build", "--modifies", "s1", "--tag", "work")
        self.run_tool("field", "set", "t1", "--field", "title", "--value", "Build behavior")
        self.run_tool("tag", "update", "work", "--name", "implementation")
        self.assertIn("t0001", self.run_tool("status", "--path", "src/app.py"))
        self.run_tool("task", "start", "t1")
        self.run_tool("task", "block", "t1", "--reason", "Awaiting service")
        self.run_tool("task", "resume", "t1", "--checked", "Service available")
        self.run_tool("task", "finish", "t1")
        self.assertFalse(list((self.root / "task").glob("*.md")))
        self.assertEqual(len(list((self.root / "archive/task").glob("*.md"))), 1)

    def test_malformed_target_does_not_block_other_field_or_task_targets(self):
        broken = self.entity("task", "t0001", {"status": "active"})
        broken.write_text("malformed entity")
        valid = self.entity("task", "t0002", {"status": "active"})
        self.run_tool("field", "set", "t1", "t2", "--field", "title", "--value", "Changed", ok=False)
        self.assertEqual(read_entity(valid, "task").fields["title"], "Changed")
        self.run_tool("task", "finish", "t1", "t2", ok=False)
        self.assertEqual(broken.read_text(), "malformed entity")
        self.assertFalse(valid.exists())

    def test_field_cycle_failure_does_not_block_independent_repairs(self):
        parent = self.entity("note", "n0001")
        repaired = self.entity("note", "n0002", {"parent": "n404"})
        valid = self.entity("note", "n0003")
        self.entity("note", "n0008", {"parent": "n9"})
        self.entity("note", "n0009", {"parent": "n8"})
        before_parent = parent.read_bytes()
        report = self.run_tool("field", "set", "n1", "n2", "n3",
                               "--field", "parent", "--value", "n1", ok=False)
        self.assertEqual(parent.read_bytes(), before_parent)
        self.assertEqual(read_entity(repaired, "note").fields["parent"], "n0001")
        self.assertEqual(read_entity(valid, "note").fields["parent"], "n0001")
        self.assertNotIn("n0008", report)
        self.assertNotIn("n0009", report)
        self.assertNotIn("n404", report)

    def test_field_removal_does_not_resolve_discarded_relationships(self):
        self.entity("task", "t0002", {"status": "done"}, archived=True)
        self.entity("spec", "s0001")
        task = self.entity("task", "t0001", {
            "blocked_by": ["t404", "t2"], "modifies": ["s404", "s1"], "parent": "t404"})
        self.run_tool("field", "remove", "t1", "--field", "blocked_by", "--value", "t404")
        self.run_tool("field", "remove", "t1", "--field", "modifies", "--value", "s404")
        self.run_tool("field", "unset", "t1", "--field", "parent")
        fields = read_entity(task, "task").fields
        self.assertEqual(fields["blocked_by"], ["t0002"])
        self.assertEqual(fields["modifies"], ["s0001"])
        self.assertNotIn("parent", fields)

    def test_task_batch_observes_dependency_archived_by_previous_target(self):
        first = self.entity("task", "t0001", {"status": "active"})
        second = self.entity("task", "t0002", {"status": "active", "blocked_by": ["t1"]})
        self.run_tool("task", "finish", "t1", "t2")
        for source in (first, second):
            self.assertFalse(source.exists())
            archived = self.root / "archive/task" / source.name
            self.assertEqual(read_entity(archived, "task", archived=True).fields["status"], "done")

    def test_noop_field_tag_and_archived_task_preserve_metadata(self):
        note = self.entity("note", "n0001")
        archived = self.entity("task", "t0001", {"status": "done"}, archived=True)
        self.run_tool("tag", "add", "registered", "--description", "Current description")
        paths = (note, archived, self.root / "tags.csv")
        for path in paths:
            os.utime(path, ns=(1_500_000_000_000_000_000, 1_500_000_000_000_000_000))
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths}
        self.run_tool("field", "set", "n1", "--field", "title", "--value", "Example")
        self.run_tool("field", "unset", "n1", "--field", "parent")
        self.run_tool("tag", "update", "registered", "--description", "Current description")
        self.run_tool("task", "finish", "t1")
        self.assertEqual({path: (path.read_bytes(), path.stat().st_mtime_ns) for path in paths}, before)


if __name__ == "__main__":
    unittest.main()
