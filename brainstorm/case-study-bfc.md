# Case Study: BFC

[BFC](https://github.com/123jimin/bfc) is a TypeScript BrainFuck compiler with a high-level assembly language (BSM). It used the previous revision of the worklog system extensively: 11 specs, 13 plans, 9 tasks (6 archived as done, 1 plan abandoned).

## What Worked Well

**Specs as living reference, not frozen requirements.** The 11 specs (s0001-s0011) describe *what currently exists*, not aspirational requirements. They have no `status` field — they're always "current." Tasks modify them via the `modifies` field. No spec was ever archived (`archive/spec/` is empty). This contradicts v1's "immutable spec" principle, and the practice won.

**Task size is small and consistent.** Successful tasks are completable in a single session: t0001 (goto coalescing) is ~15 lines of code, t0003 (scan loop pattern) is recognition only with no AST rewrite, t0006 is 3 macro implementations. The one large task (t0009, 5-phase source location tracking) worked because p0009 was unusually detailed.

**Plan detail scales with proximity to implementation.** p0009 (source location) has 5 phases, TypeScript interfaces, a file impact table — it was about to be built. p0010-p0013 are thin sketches — they're far from implementation. This is natural and the system accommodates it without forcing a uniform level of detail.

**Cross-references create a navigable graph.** `targets`, `implements`, `modifies`, `blocked_by` create forward links; `find-refs.py` provides reverse lookups. You can trace plan -> spec targets -> implementing tasks. This is the most structurally valuable feature.

**Abandoned items with documented reasoning.** p0005 (primitive cell transfers) was abandoned with 4 open questions recorded — syntax, scratch cells, AST level, optimizer interaction. A future agent revisiting this idea doesn't start from zero.

**Investigation tasks are a real pattern.** t0007 (lexer performance) started as an investigation, not a fix. It documented benchmarks, root causes, what was fixed, and what was deferred with rationale. This is exactly the kind of non-obvious cross-session knowledge the worklog should preserve.

## What Didn't Work / Lessons

**Spec/plan overlap is real.** s0010 (optimization spec) and p0002 (optimizer plan) describe the same passes — one as "what exists," the other as "what to build." Once a plan's items are implemented, its content migrates into the spec. The boundary is a continuum, confirming the pitfall already documented.

**Design rationale gets buried in archives.** p0008 (conditional env) is archived as "done." The *why* behind its design choices now lives only in the archive. The spec (s0009) captures *what* was built, not *why* those alternatives were rejected. There's no permanent home for decision rationale.

**Schema inconsistency crept in.** Some tasks use `implements = ["p0002"]`, others use `plan = "p0001"`. The TOML frontmatter isn't validated strictly enough to catch this.

**Validation is manual and therefore skipped.** `validate.py` is whitelisted in `.claude/settings.local.json` but nothing triggers it automatically. This directly confirms the pitfall: "Archive and validate scripts require deliberate invocation — frequently skipped."

**Source code markers (`@worklog sNNNN`) were not adopted.** The v1 design defines them, but the bfc source shows no usage. The friction of maintaining inline markers was too high.

**Stale plans accumulate.** p0003 (VLA), p0004 (high-level language) are blocked/draft plans sitting in the active directory with no clear path forward. p0007 was archived as "active" — the archive boundary is fuzzy.

**Tasks don't track sub-progress.** t0009 implemented 5 phases but is tracked as a single "done." The v1 design had `steps.md` for checklists, but bfc doesn't use them — suggesting the overhead wasn't worth it for small tasks, and large tasks are rare enough to not justify the mechanism.

**"File impact" in plans leaks implementation.** p0009 lists every file that changes. Useful for the implementing agent, but this is the kind of over-specification that couples the plan to the current file layout.

## Key Takeaways

1. Specs work best as **mutable living reference** — "what the design currently is" — not as frozen requirements.
2. The plan/spec boundary is fluid in practice. The system should accommodate overlap rather than enforce rigid separation.
3. **Small tasks** are the success pattern. The plugin should encourage this.
4. **Investigation/research** is a legitimate task type that doesn't implement a plan.
5. **Decision rationale** needs a permanent home that isn't an archived plan.
6. **Automatic validation** via hooks is necessary — manual script invocation doesn't survive contact with reality.
7. **Source code markers** were too high-friction to adopt. Either automate or drop.
8. Cross-references are the most valuable structural feature, but **schema enforcement** is needed to prevent drift.
