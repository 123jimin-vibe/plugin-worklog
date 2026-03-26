# @worklog s0017
"""Tests for plugin/skills/worklog/script/lib/parse.py — frontmatter parsing.

Tests verify attributes via duck typing (e.g. result.id, result.type),
not concrete class identity.
"""

import pathlib
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
from tests.loader import load_module

_mod, _module_available, _missing_reason = load_module(
    "lib/parse.py",
    expected=["parse_frontmatter"],
)

if _module_available:
    parse_frontmatter = _mod.parse_frontmatter


# ===================================================================
# Helpers
# ===================================================================

def _write_file(directory, filename, content):
    """Write a file into *directory* and return its path."""
    path = pathlib.Path(directory) / filename
    path.write_text(content, encoding="utf-8")
    return str(path)


# ===================================================================
# parse_frontmatter — valid input
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestParseFrontmatterValid(unittest.TestCase):
    """Valid frontmatter between +++ fences returns an Entity-like object."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_basic_fields(self):
        path = _write_file(self.tmpdir, "s0001-auth.md", (
            '+++\n'
            'id = "s0001"\n'
            'title = "Auth"\n'
            'tags = ["auth"]\n'
            '+++\n'
            '\n'
            '# Auth\n'
            'Body text here.\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(result.id, "s0001")
        self.assertEqual(result.title, "Auth")
        self.assertEqual(result.tags, ["auth"])

    def test_extra_fields_in_fields_dict(self):
        path = _write_file(self.tmpdir, "t0001-work.md", (
            '+++\n'
            'id = "t0001"\n'
            'title = "Work"\n'
            'tags = ["tooling", "quality"]\n'
            'status = "pending"\n'
            'modifies = ["s0001", "s0002"]\n'
            '+++\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(result.tags, ["tooling", "quality"])
        self.assertEqual(result.fields["modifies"], ["s0001", "s0002"])
        self.assertEqual(result.fields["status"], "pending")

    def test_multiline_toml_array(self):
        path = _write_file(self.tmpdir, "s0005-multi.md", (
            '+++\n'
            'id = "s0005"\n'
            'title = "Multi"\n'
            'tags = [\n'
            '    "tooling",\n'
            '    "quality",\n'
            ']\n'
            '+++\n'
        ))
        result = parse_frontmatter(path)
        self.assertIsInstance(result.tags, list)
        self.assertEqual(result.tags, ["tooling", "quality"])

    def test_content_after_frontmatter_ignored(self):
        path = _write_file(self.tmpdir, "s0002-stuff.md", (
            '+++\n'
            'id = "s0002"\n'
            'title = "Stuff"\n'
            'tags = ["misc"]\n'
            '+++\n'
            '\n'
            '# Stuff\n'
            'This body should not affect parsing.\n'
            'id = "WRONG"\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(result.id, "s0002")

    def test_path_stored(self):
        path = _write_file(self.tmpdir, "s0003-paths.md", (
            '+++\n'
            'id = "s0003"\n'
            'title = "Paths"\n'
            'tags = ["misc"]\n'
            '+++\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(str(result.path), path)


# ===================================================================
# parse_frontmatter — invalid input
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestParseFrontmatterInvalid(unittest.TestCase):
    """Malformed or missing frontmatter raises an error."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_missing_closing_fence(self):
        path = _write_file(self.tmpdir, "broken.md", (
            '+++\n'
            'id = "s0001"\n'
            'title = "Broken"\n'
            '# No closing fence\n'
        ))
        with self.assertRaises(Exception):
            parse_frontmatter(path)

    def test_no_frontmatter(self):
        path = _write_file(self.tmpdir, "plain.md", (
            '# Just Markdown\n'
            'No frontmatter here.\n'
        ))
        with self.assertRaises(Exception):
            parse_frontmatter(path)

    def test_empty_frontmatter_raises(self):
        """Empty frontmatter has no id — should raise."""
        path = _write_file(self.tmpdir, "empty.md", '+++\n+++\n')
        with self.assertRaises(Exception):
            parse_frontmatter(path)


# ===================================================================
# Entity type inference from ID prefix
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestEntityTypeInference(unittest.TestCase):
    """Entity type is inferred from the ID prefix."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _parse_with_id(self, entity_id):
        path = _write_file(self.tmpdir, f"{entity_id}-test.md", (
            '+++\n'
            f'id = "{entity_id}"\n'
            'title = "Test"\n'
            'tags = ["test"]\n'
            '+++\n'
        ))
        return parse_frontmatter(path)

    def test_spec_prefix(self):
        result = self._parse_with_id("s0001")
        self.assertEqual(result.type, "spec")

    def test_task_prefix(self):
        result = self._parse_with_id("t0001")
        self.assertEqual(result.type, "task")

    def test_decision_prefix(self):
        result = self._parse_with_id("d0001")
        self.assertEqual(result.type, "decision")

    def test_unknown_prefix(self):
        """Unknown ID prefix raises or returns an indicator."""
        path = _write_file(self.tmpdir, "x0001-test.md", (
            '+++\n'
            'id = "x0001"\n'
            'title = "Unknown"\n'
            'tags = ["test"]\n'
            '+++\n'
        ))
        # Accept either an exception or a sentinel value.
        try:
            result = parse_frontmatter(path)
            self.assertNotIn(result.type, ("spec", "task", "decision"),
                             "Unknown prefix should not resolve to a known type")
        except Exception:
            pass  # raising is also acceptable


# ===================================================================
# Extended IDs (non-4-digit)
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestParseFrontmatterExtendedIds(unittest.TestCase):
    """IDs with non-standard digit counts are parsed correctly."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_short_id_s1(self):
        path = _write_file(self.tmpdir, "s1-short.md", (
            '+++\n'
            'id = "s1"\n'
            'title = "Short"\n'
            'tags = ["misc"]\n'
            '+++\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(result.id, "s1")
        self.assertEqual(result.type, "spec")

    def test_long_id_t00001(self):
        path = _write_file(self.tmpdir, "t00001-long.md", (
            '+++\n'
            'id = "t00001"\n'
            'title = "Long"\n'
            'tags = ["misc"]\n'
            'status = "pending"\n'
            'modifies = ["s0001"]\n'
            '+++\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(result.id, "t00001")
        self.assertEqual(result.type, "task")

    def test_two_digit_id_d42(self):
        path = _write_file(self.tmpdir, "d42-answer.md", (
            '+++\n'
            'id = "d42"\n'
            'title = "Answer"\n'
            'relates_to = ["s0001"]\n'
            '+++\n'
        ))
        result = parse_frontmatter(path)
        self.assertEqual(result.id, "d42")
        self.assertEqual(result.type, "decision")


if __name__ == "__main__":
    unittest.main()
