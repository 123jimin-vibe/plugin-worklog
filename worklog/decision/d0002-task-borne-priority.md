+++
id = "d0002"
title = "Task-borne priority with a generated backlog view"
relates_to = ["s0016", "s0012", "s0010"]
supersedes = []
+++

# Task-borne priority with a generated backlog view

## Context

s0016 defined a manually maintained `worklog/UNIMPLEMENTED.md`. It was never created, and its own Dangers section predicted drift as the expected failure mode. Meanwhile "what should I work on" spans two kinds of outstanding work — `UNIMPLEMENTED` spec items and open tasks — with no shared priority signal. Candidate stores for triaged priority: (a) a priority field in task frontmatter with triage-by-task-promotion, (b) inline annotations on the markers in spec bodies, (c) a hybrid.

## Choice

(a). Priority lives only in task frontmatter: an optional non-negative integer `priority`, 0 most urgent, absent meaning untriaged. Triaging an `UNIMPLEMENTED` item means covering it with an open task whose `modifies` includes the spec and which carries `priority`; the item inherits the lowest priority among its covering open tasks. A script (`backlog.py`, s0010) computes the unified view on demand; no index file exists.

Marker detection is pinned with the choice: a bare `UNIMPLEMENTED` token marks an item; a backticked occurrence is a mention, not a marker.

## Rationale

- Priority is process state, not behavior. Tasks already carry process state (status); specs are always-current behavior and should stay stable.
- Decisive against (b): every edit to a spec file resets its drift watermark (s0010 Dangers), so inline retriage annotations would blind drift detection each time priorities shift.
- s0012 already anticipated an urgency field on tasks; (a) realizes it.
- A computed view cannot drift; the maintained index demonstrably did not survive contact with practice.

## Consequences

- Triage granularity is spec-level: `modifies` links task to spec, not to an individual marker, so one prioritized task lifts every marker in its spec. Accepted; per-marker linkage can be added if this proves insufficient.
- Retriage is one frontmatter edit on a task — no spec churn, no watermark resets.
- A marker with no covering prioritized open task surfaces explicitly as untriaged, which is the cue that triage is needed.
