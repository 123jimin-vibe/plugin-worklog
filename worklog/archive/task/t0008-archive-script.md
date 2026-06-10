+++
id = "t0008"
title = "archive.py: archiving with forced spec read"
tags = ["tooling"]
status = "done"
modifies = ["s0010", "s0012", "s0018"]
+++

# archive.py: archiving with forced spec read

The archive-time spec check is skippable because nothing routes the spec text through the agent's context. A script makes the read unskippable.

## Scope

- `archive.py <task-id>`: verify status is `done` (or `cancelled` with an explanation in the body); print each spec in `modifies` in full; run drift for those specs' `paths`. Default run only reports — `--confirm` performs the move, so the spec text is in context before the move happens.
- Move uses `git mv` for tracked files, plain `mv` otherwise.
- Tests before implementation (s0017). Add to the SKILL.md scripts table and the archiving flow from t0007.

## Outcome

archive.py refuses non-terminal tasks (and cancelled tasks lacking an explanation), prints each spec in `modifies` in full with its drift classification — the forced consistency read — and moves the file into `archive/task/` only on `--confirm`: `git mv` when tracked, plain `mv` otherwise (honoring the tracked/untracked rule). Reuses `lib/gitdrift.py`. Added to the SKILL.md scripts table; the s0012 and SKILL.md archiving lines now point to it. Tests cover refusal, spec surfacing without moving, tracked and untracked moves, the cancelled-needs-explanation gate, and unknown IDs.

Completed independently of t0007: `blocked_by` was a wording-first sequencing preference, not a code dependency, so it is dropped. t0007's archiving reframe will enrich the surrounding prose (it also modifies s0012/s0018); the script and its current wiring stand on their own.
