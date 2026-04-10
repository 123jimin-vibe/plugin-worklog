"""PreToolUse hook — auto-allow Bash calls that invoke plugin skill scripts.

Pessimistic: every check that fails exits 0 with no output (no opinion,
does *not* auto-allow).  Only an exact match of python + skill
script at the expected depth produces an "allow" decision.
"""

import json
import shlex
import sys
from pathlib import Path


def parse_hook_input() -> tuple[str, ...] | None:
    """Read hook JSON from stdin and return the parsed command tokens."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return None

    if not isinstance(hook_input, dict):
        return None

    command = hook_input.get("tool_input", {}).get("command", "")
    try:
        parts = shlex.split(command)
    except ValueError:
        return None

    return tuple(parts) if len(parts) >= 2 else None


def is_skill_script(script_path: str, plugin_root: str) -> bool:
    """Return True if *script_path* is a .py file at skills/<name>/scripts/<file>.py."""
    try:
        script = Path(script_path).resolve(strict=True)
        skills = (Path(plugin_root) / "skills").resolve(strict=True)
    except (OSError, ValueError):
        return False

    if not script.is_relative_to(skills):
        return False

    relative = script.relative_to(skills)
    if len(relative.parts) != 3:
        return False
    if relative.parts[1] != "scripts":
        return False
    if script.suffix != ".py":
        return False
    return True


def emit_allow() -> None:
    """Write an 'allow' decision to stdout."""
    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "permissionDecisionReason": "Plugin skill script invocation",
            }
        },
        sys.stdout,
    )


def main() -> None:
    parts = parse_hook_input()
    if parts is None:
        return

    import os

    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if not plugin_root:
        return

    # Accept "python" as the executable (no venv check — worklog has no venv deps)
    exe = parts[0]
    if not Path(exe).stem.startswith("python"):
        return

    if not is_skill_script(parts[1], plugin_root):
        return

    emit_allow()


if __name__ == "__main__":
    main()
