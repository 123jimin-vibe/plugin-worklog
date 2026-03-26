# @worklog s0017
"""Shared module loader for tests.

Loads a module from the plugin script tree via importlib. Returns a tuple of
(module_or_none, available_bool, reason_string) so test files can guard classes
with @unittest.skipUnless.

Usage:

    from tests.loader import load_module

    _mod, _module_available, _missing_reason = load_module(
        "lib/parse.py",
        expected=["parse_frontmatter"],
    )

    if _module_available:
        parse_frontmatter = _mod.parse_frontmatter
"""

import importlib.util
import pathlib

_SCRIPT_ROOT = (
    pathlib.Path(__file__).resolve().parents[1]
    / "plugin" / "skills" / "worklog" / "script"
)


def load_module(relative_path, expected=None):
    """Load a module from the plugin script tree.

    Args:
        relative_path: Path relative to plugin/skills/worklog/script/,
            e.g. "lib/parse.py" or "validate.py".
        expected: Optional list of attribute names the module must expose.

    Returns:
        (module, True, "") on success.
        (None, False, reason) on failure.
    """
    module_path = str(_SCRIPT_ROOT / relative_path)
    module_name = relative_path.replace("/", ".").removesuffix(".py")

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        return None, False, f"{relative_path} not loadable"

    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except BaseException as exc:
        return None, False, f"{relative_path} failed to load: {exc}"

    if expected:
        for fn_name in expected:
            if not hasattr(mod, fn_name):
                return None, False, f"{relative_path} is missing: {fn_name}"

    return mod, True, ""
