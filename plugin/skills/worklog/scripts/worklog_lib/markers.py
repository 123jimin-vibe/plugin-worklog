"""Recognize workflow markers in Markdown prose, excluding code examples."""

import re

MARKER = re.compile(r"\b(?:NEEDS APPROVAL|NEEDS REVIEW|UNIMPLEMENTED)\b")


def markers(body):
    found, fence = [], None
    for number, line in enumerate(body.splitlines(), 1):
        match = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if match:
            token = match[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence or line.startswith(("    ", "\t")):
            continue
        prose = re.sub(r"(`+).*?\1", "", line)
        heading = re.match(r"^\s{0,3}#{1,6}\s", prose)
        for match in MARKER.finditer(prose):
            if heading or not prose[:match.start()].strip(" -*_(") or prose[match.start() - 1:match.start()] == "(":
                found.append((match[0], number, line.strip()))
    return found
