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
import sys

_SCRIPT_ROOT = (
    pathlib.Path(__file__).resolve().parents[1]
    / "plugin" / "skills" / "worklog" / "scripts"
)


def load_module(relative_path, expected=None):
    """Load a module from the plugin script tree.

    Args:
        relative_path: Path relative to plugin/skills/worklog/scripts/,
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
        # Add script root to sys.path so `from lib.x import y` resolves.
        script_root_str = str(_SCRIPT_ROOT)
        if script_root_str not in sys.path:
            sys.path.insert(0, script_root_str)

        mod = importlib.util.module_from_spec(spec)
        # Register before exec so dataclasses and relative imports work.
        sys.modules[module_name] = mod

        # Ensure parent packages exist for relative imports.
        parts = module_name.rsplit(".", 1)
        if len(parts) == 2:
            parent_name = parts[0]
            if parent_name not in sys.modules:
                parent_dir = str(_SCRIPT_ROOT / parent_name.replace(".", "/"))
                parent_spec = importlib.util.spec_from_file_location(
                    parent_name,
                    parent_dir + "/__init__.py",
                    submodule_search_locations=[parent_dir],
                )
                if parent_spec and parent_spec.loader:
                    parent_mod = importlib.util.module_from_spec(parent_spec)
                    sys.modules[parent_name] = parent_mod
                    parent_spec.loader.exec_module(parent_mod)

        # Pre-load sibling modules that aren't yet in sys.modules,
        # so relative imports (e.g. from .parse import ...) resolve.
        if len(parts) == 2:
            parent_dir = _SCRIPT_ROOT / parts[0].replace(".", "/")
            if parent_dir.is_dir():
                for sibling in sorted(parent_dir.glob("*.py")):
                    if sibling.name == "__init__.py":
                        continue
                    sib_name = f"{parts[0]}.{sibling.stem}"
                    if sib_name not in sys.modules:
                        sib_rel = f"{parts[0]}/{sibling.name}"
                        load_module(sib_rel)

        spec.loader.exec_module(mod)
    except BaseException as exc:
        sys.modules.pop(module_name, None)
        return None, False, f"{relative_path} failed to load: {exc}"

    if expected:
        for fn_name in expected:
            if not hasattr(mod, fn_name):
                return None, False, f"{relative_path} is missing: {fn_name}"

    return mod, True, ""
