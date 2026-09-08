"""Project policy configuration used during initialization."""

import tomllib
from pathlib import Path

DEFAULT_MODES = {"spec": "propose", "task": "draft", "note": "draft"}
MODES = {"read_only", "propose", "draft", "autonomous"}


def read_configuration(path: Path, *, kinds=DEFAULT_MODES) -> dict:
    with path.open("rb") as stream:
        data = tomllib.load(stream)
    for kind in kinds:
        table = data.get(kind, {})
        if not isinstance(table, dict):
            raise ValueError(f"{path}: {kind} must be a policy table")
        mode = table.get("agent_mode")
        if "agent_mode" in table and (not isinstance(mode, str) or mode not in MODES):
            raise ValueError(f"{path}: invalid {kind}.agent_mode: {mode!r}")
    return data


def default_configuration() -> bytes:
    lines = [
        "# worklog project configuration.",
        "# Agents MUST treat this file as read-only and SHOULD NOT prepare changes unless asked.",
        "# Omitted policies default to propose for specs and draft for tasks and notes.",
    ]
    guidance = {
        "propose": "Before applying a change, agents MUST obtain human approval of its content or permission scoped to the edit.",
        "draft": "Unapproved agent-authored content MUST be marked NEEDS APPROVAL.",
    }
    for kind, mode in DEFAULT_MODES.items():
        lines.extend(["", f"[{kind}]", f"# {guidance[mode]}", f'agent_mode = "{mode}"'])
    return ("\n".join(lines) + "\n").encode("utf-8")
