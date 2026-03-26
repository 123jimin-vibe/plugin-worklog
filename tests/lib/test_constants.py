# @worklog s0017
"""Tests for plugin/skills/worklog/script/lib/constants.py — parse_id and normalize_id."""

import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from tests.loader import load_module

_mod, _module_available, _missing_reason = load_module(
    "lib/constants.py",
    expected=["parse_id", "normalize_id"],
)

if _module_available:
    parse_id = _mod.parse_id
    normalize_id = _mod.normalize_id


# ===================================================================
# parse_id
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestParseIdValid(unittest.TestCase):
    """Valid IDs return (prefix, number) tuples."""

    def test_standard_four_digit(self):
        self.assertEqual(parse_id("s0001"), ("s", 1))

    def test_task_prefix(self):
        self.assertEqual(parse_id("t0042"), ("t", 42))

    def test_decision_prefix(self):
        self.assertEqual(parse_id("d0100"), ("d", 100))

    def test_single_digit(self):
        self.assertEqual(parse_id("s1"), ("s", 1))

    def test_many_digits(self):
        self.assertEqual(parse_id("t00001"), ("t", 1))

    def test_large_number(self):
        self.assertEqual(parse_id("s9999"), ("s", 9999))


@unittest.skipUnless(_module_available, _missing_reason)
class TestParseIdInvalid(unittest.TestCase):
    """Invalid IDs return None."""

    def test_unknown_prefix(self):
        self.assertIsNone(parse_id("x0001"))

    def test_no_digits(self):
        self.assertIsNone(parse_id("s"))

    def test_non_numeric_suffix(self):
        self.assertIsNone(parse_id("s00a1"))

    def test_empty_string(self):
        self.assertIsNone(parse_id(""))

    def test_bare_number(self):
        self.assertIsNone(parse_id("0001"))


# ===================================================================
# normalize_id
# ===================================================================

@unittest.skipUnless(_module_available, _missing_reason)
class TestNormalizeId(unittest.TestCase):
    """IDs are normalized to canonical 4-digit zero-padded form."""

    def test_short_id(self):
        self.assertEqual(normalize_id("s1"), "s0001")

    def test_already_canonical(self):
        self.assertEqual(normalize_id("t0042"), "t0042")

    def test_over_padded(self):
        self.assertEqual(normalize_id("s00001"), "s0001")

    def test_two_digits(self):
        self.assertEqual(normalize_id("d10"), "d0010")

    def test_non_id_passthrough(self):
        self.assertEqual(normalize_id("banana"), "banana")

    def test_empty_passthrough(self):
        self.assertEqual(normalize_id(""), "")


if __name__ == "__main__":
    unittest.main()
