+++
id = "t0003"
title = "Implement plugin scripts"
tags = ["tooling"]
status = "pending"
modifies = ["s0010"]
+++

# Implement plugin scripts

Implement the scripts listed in s0010 Anticipated Changes: next-id, validate, drift, search. Python, bundled at `plugin/skills/worklog/script/`, accepting `-w PATH` for worklog root.

Priority order per methodology needs:

1. **validate** — dangling refs, invalid statuses, missing required fields. Most impactful: prevents silent integrity erosion.
2. **next-id** — next available ID for a given entity type. Low complexity, high convenience.
3. **drift** — spec-code drift report for specs with `paths`.
4. **search** — query entities by tag, status, or relationship.
