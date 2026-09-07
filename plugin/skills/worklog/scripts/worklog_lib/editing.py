"""Surgical edits to top-level TOML fields; preserve unrelated text and bodies."""

import json
import tomllib

from .entities import _closing_fence


def encode_value(value):
    return json.dumps(value, ensure_ascii=False)


def _tokens(text):
    pos = 0
    while pos < len(text):
        start = pos
        char = text[pos]
        if char in " \t\r":
            pos += 1
            continue
        if char == "#":
            pos = text.find("\n", pos)
            if pos < 0:
                pos = len(text)
        elif char in "\"'":
            quote = char * 3 if text.startswith(char * 3, pos) else char
            pos += len(quote)
            while pos < len(text):
                if char == '"' and text[pos] == "\\":
                    pos += 2
                elif text.startswith(quote, pos):
                    pos += len(quote)
                    if len(quote) == 3:
                        while pos < len(text) and text[pos] == char:
                            pos += 1
                    break
                else:
                    pos += 1
        elif char in "\n=[]{}.,":
            pos += 1
        else:
            while pos < len(text) and text[pos] not in " \t\r\n=[]{}.,#\"'":
                pos += 1
        yield text[start:pos], start, pos


def edit_fields(raw: bytes, changes: dict, append: str = "") -> bytes:
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    text = raw.decode("utf-8-sig")
    lines = text.splitlines(keepends=True)
    end = _closing_fence(lines)
    if end is None:
        raise ValueError("Missing closing frontmatter fence")
    header = "".join(lines[1:end])
    data = tomllib.loads(header)
    newline = "\r\n" if "\r\n" in header else "\n"
    tokens = list(_tokens(header))
    spans, insertion = {}, len(header)
    index = 0
    while index < len(tokens):
        token, start, stop = tokens[index]
        if token == "\n" or token.startswith("#"):
            index += 1
            continue
        if token == "[":
            insertion = start
            break
        key_start = start
        eq = index
        while eq < len(tokens) and tokens[eq][0] != "=":
            eq += 1
        if eq == len(tokens):
            raise ValueError("Cannot locate TOML assignment")
        key_text = header[key_start:tokens[eq][1]].strip()
        parsed_key = tomllib.loads(key_text + " = 0")
        key = next(iter(parsed_key)) if list(parsed_key.values()) == [0] else None
        value_start = tokens[eq + 1][1]
        value_end, depth, comments = value_start, 0, []
        index = eq + 1
        while index < len(tokens):
            token, start, stop = tokens[index]
            if token == "\n" and depth == 0:
                break
            if token.startswith("#"):
                if depth:
                    comments.append(token.rstrip("\r"))
            elif token != "\n":
                depth += (token in ("[", "{")) - (token in ("]", "}"))
                value_end = stop
            index += 1
        if key is not None:
            spans[key] = (key_start, value_start, value_end, comments)
    edits, additions = [], []
    expected = dict(data)
    for key, value in changes.items():
        if value is None:
            expected.pop(key, None)
        else:
            expected[key] = value
        if key in spans:
            start, value_start, stop, comments = spans[key]
            if value is None:
                replacement = (newline.join(comments) + newline) if comments else ""
                edits.append((start, stop, replacement))
            else:
                edits.append((value_start, stop, encode_value(value)))
                if comments:
                    edits.append((start, start, newline.join(comments) + newline))
        elif value is not None:
            if key in data:
                raise ValueError(f"{key}: unsupported field layout; no files changed")
            additions.append(f"{key} = {encode_value(value)}{newline}")
    if additions:
        edits.append((insertion, insertion, "".join(additions)))
    # Rebuild once instead of copying the entire document for every replacement.
    parts, offset = [], 0
    for start, stop, replacement in sorted(edits, key=lambda edit: (edit[0], edit[1])):
        parts.extend((header[offset:start], replacement))
        offset = stop
    parts.append(header[offset:])
    header = "".join(parts)
    if tomllib.loads(header) != expected:
        raise ValueError("Edited frontmatter did not preserve unrelated metadata")
    body = "".join(lines[end + 1:])
    if append:
        body += ("" if body.endswith("\n") else newline) + newline + append.replace("\n", newline) + newline
    return bom + (lines[0] + header + lines[end] + body).encode("utf-8")
