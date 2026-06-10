+++
id = "t0015"
title = "Generated UNIMPLEMENTED view with triaged priority"
tags = ["entity", "tooling"]
status = "pending"
modifies = ["s0016", "s0012", "s0010", "s0018"]
+++

# Generated UNIMPLEMENTED view with triaged priority

s0016's manually maintained `worklog/UNIMPLEMENTED.md` predicts its own drift and was never created. Meanwhile "what should I work on" has no priority signal spanning the two kinds of outstanding work: `UNIMPLEMENTED` spec items and open tasks.

## Scope

- Replace the maintained index with a generated view: a script collects `UNIMPLEMENTED` markers live, so there is no file to drift.
- Design where triaged priority is stored so the view ranks markers and open tasks together; untriaged items surface as untriaged. Candidates: a priority field in task frontmatter with triage-by-task-promotion; an inline marker annotation; a combination. s0012 already anticipates an urgency field.
- The mechanism choice needs a decision record before implementation.
- Rewrite s0016 to the chosen mechanism; update s0012 (field), s0010 (script), SKILL.md.
