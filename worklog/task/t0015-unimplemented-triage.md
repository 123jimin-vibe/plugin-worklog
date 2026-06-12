+++
id = "t0015"
title = "Generated UNIMPLEMENTED view with triaged priority"
tags = ["entity", "tooling"]
status = "done"
modifies = ["s0016", "s0012", "s0010", "s0018"]
+++

# Generated UNIMPLEMENTED view with triaged priority

s0016's manually maintained `worklog/UNIMPLEMENTED.md` predicts its own drift and was never created. Meanwhile "what should I work on" has no priority signal spanning the two kinds of outstanding work: `UNIMPLEMENTED` spec items and open tasks.

## Scope

- Replace the maintained index with a generated view: a script collects `UNIMPLEMENTED` markers live, so there is no file to drift.
- Design where triaged priority is stored so the view ranks markers and open tasks together; untriaged items surface as untriaged. Candidates: a priority field in task frontmatter with triage-by-task-promotion; an inline marker annotation; a combination. s0012 already anticipates an urgency field.
- The mechanism choice needs a decision record before implementation.
- Rewrite s0016 to the chosen mechanism; update s0012 (field), s0010 (script), SKILL.md.

## Outcome

- d0002 records the mechanism: task-borne `priority` (optional non-negative int, 0 most urgent) + triage-by-task-promotion; markers inherit the lowest priority among covering open tasks; decisive argument against inline annotations was the drift-watermark reset on every spec edit.
- `backlog.py` implements the view (tests first: tests/test_backlog.py, 10 tests); validate.py gained priority checks (3 fail-first tests). Marker convention pinned: bare `UNIMPLEMENTED` = marker, backticked = mention.
- s0016 renamed to Backlog View and rewritten; s0012 gained the `priority` field row (urgency anticipated-change resolved); s0010 + SKILL.md updated.
- Dogfooding caught phantom entries from unbackticked meta-prose in s0016/s0018/s0019 — backticked, view now clean.
