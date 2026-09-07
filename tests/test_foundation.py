"""Behavioral coverage for shared entity reading and identity."""

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "plugin/skills/worklog/scripts"
sys.path.insert(0, str(SCRIPTS))

from worklog_lib.entities import discover_entities, read_entity
from worklog_lib.identity import normalize_id


class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def entity(self, relative, frontmatter, body="\nBody +++ remains intact.\n"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(("+++\n" + frontmatter + "\n+++\n" + body).encode())
        return path

    def test_id_aliases_and_unbounded_digits(self):
        for value in ("s1", "s01", "s001", "s0001", "s00001"):
            self.assertEqual(normalize_id(value), "s0001")
        self.assertEqual(normalize_id("t000"), "t0000")
        self.assertEqual(normalize_id("n12345"), "n12345")
        self.assertEqual(normalize_id("d" + "9" * 5000), "d" + "9" * 5000)
        for value in ("", "s", "s-1", "s1x", "r01", "s1\n", 1):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_id(value)

    def test_read_preserves_body_and_unknown_legacy_fields(self):
        body = "\r\n  Text +++\r\n\r\n"
        path = self.entity("decision/d0001-old.md", 'id = "d0001"\n'
                           'title = "Value +++ inside TOML"\nrelates_to = ["s0001"]', body)
        before = path.read_bytes()
        entity = read_entity(path, "decision")
        self.assertEqual(entity.body, body)
        self.assertEqual(entity.fields["relates_to"], ["s0001"])
        self.assertEqual(entity.tags, ())
        self.assertEqual(path.read_bytes(), before)

    def test_discovery_includes_nested_types_and_flat_archived_tasks(self):
        for kind, prefix in (("spec", "s"), ("task", "t"), ("note", "n"), ("decision", "d")):
            self.entity(f"{kind}/nested/{prefix}0001-title.md",
                        f'id = "{prefix}0001"\ntitle = "Title"')
        self.entity("ref/source/excerpt.md", 'title = "Source"\nsource = "https://example.org"')
        self.entity("archive/task/t0002-old.md", 'id = "t0002"\ntitle = "Old"')
        store = discover_entities(self.root)
        self.assertEqual(store.errors, [])
        self.assertEqual(len(store.entities), 6)
        self.assertTrue(store.by_id["t0002"].archived)
        self.assertIsNone(next(e for e in store.entities if e.type == "ref").id)

    def test_discovery_reports_errors_without_losing_valid_entries(self):
        self.entity("spec/s0001-good.md", 'id = "s0001"\ntitle = "Good"')
        self.entity("note/n0001-bad.md", 'id = "n0001"\ntitle = [')
        self.entity("task/t0001-bad.md", 'id = "t0001"\ntitle = "Bad"\ntags = "oops"')
        store = discover_entities(self.root)
        self.assertEqual(len(store.errors), 2)
        self.assertIn("s0001", store.by_id)

    def test_duplicate_identity_in_archive_is_ambiguous(self):
        self.entity("task/t0001-current.md", 'id = "t0001"\ntitle = "Current"')
        self.entity("archive/task/t0001-old.md", 'id = "t0001"\ntitle = "Old"')
        store = discover_entities(self.root)
        self.assertTrue(any("duplicate" in error.lower() for error in store.errors))
        self.assertNotIn("t0001", store.by_id)

    def test_invalid_frontmatter_and_identity_are_reported(self):
        cases = [
            ('title = "No ID"', "spec/s0001-title.md"),
            ('id = "s0001"\ntitle = 3', "spec/s0001-title.md"),
            ('id = "s0001"\ntitle = "Wrong type"', "task/t0001-title.md"),
            ('id = "s0001"\ntitle = "Wrong filename"', "spec/s00010-title.md"),
        ]
        for fields, relative in cases:
            with self.subTest(fields=fields):
                path = self.entity(relative, fields)
                with self.assertRaises(ValueError):
                    read_entity(path, relative.split("/")[0])

    def test_frontmatter_fences_inside_multiline_toml_are_data(self):
        for quote in ('"""', "'''"):
            with self.subTest(quote=quote):
                path = self.entity("note/n0001-note.md", 'id = "n0001"\ntitle = "Note"\n'
                                   f'custom = {quote}\n+++\n# not a comment\ntext{quote}\ntags = ["tag"]')
                entity = read_entity(path, "note")
                self.assertEqual(entity.fields["custom"], "+++\n# not a comment\ntext")
                self.assertEqual(entity.tags, ("tag",))


if __name__ == "__main__":
    unittest.main()
