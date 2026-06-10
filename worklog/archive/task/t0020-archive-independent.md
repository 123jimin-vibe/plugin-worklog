+++
id = "t0020"
title = "archive.py: handle each task independently, not atomically"
tags = ["tooling"]
status = "done"
modifies = ["s0010", "s0018"]
+++

# archive.py: handle each task independently, not atomically

t0019 made batch archiving atomic — one failing task aborts the whole batch.
That is too strict: archiving a sprint's tasks, one stale task shouldn't block
the ready ones. Process each task independently.

## Scope

- Archive each valid task; a task that fails its gate (non-terminal, cancelled
  without explanation, unknown, not a task) is reported and left in place while
  the others proceed.
- Exit non-zero if any task could not be archived, so partial failure is still
  signalled — but the successful archives stand.
- Already-archived IDs remain a skip, not a failure. Deduped spec surfacing and
  duplicate-ID collapsing are unchanged.

## Constraints

- Tests before implementation (s0017); rewrite the t0019 atomic-batch test to the
  independent contract.
- Update the archive.py description in s0010 and the SKILL.md scripts table — both
  currently say "atomic."

## Outcome

Gate errors no longer abort the batch: invalid tasks are reported on stderr and left
in place while the valid ones archive. The command exits non-zero when any task failed
its gate or move, so partial failure is still signalled (report-only mode included).
Already-archived IDs remain a non-fatal skip; dedup and duplicate-collapse unchanged.
s0010 and the SKILL.md scripts table corrected from "atomic" to independent. The t0019
atomic-batch test was rewritten to assert partial success (the ready task archives, the
unready one stays put, exit non-zero); full suite 128 green.

The "atomic" behavior this reverses was speculative detail I added in t0019 without it
being asked for — s0019 pitfall S6 — caught and corrected here.
