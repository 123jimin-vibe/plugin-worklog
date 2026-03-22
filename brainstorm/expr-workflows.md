# Workflows

Catalog of workflows that occur in a software project, analyzed for worklog entity design.

## Cross-Cutting Rules

**Project scale:** small and large projects require different methodology. Workflows below describe the full-ceremony version. For small projects, steps can be compressed (e.g. spec + single task, lighter decision records, dangers/anticipated changes omitted when the project scope makes them obvious). The rules below still apply — but the *artifacts* can be lighter.

**Tests before implementation:** tests are written before implementation, derived from the spec (not the code). Applies to all workflows that produce code.

**Test sub-agent:** a dedicated agent writes tests from the spec. It receives detailed instructions derived from pitfalls (test bias, implementation coupling, missing edge cases, etc.) to counteract known AI testing failures. The implementing agent never writes its own tests — separation prevents implementation from leaking into test design.

**Specs describe intent, not implementation:** specs capture observable behavior (*what/why*), not API signatures or code layout (*how*). Over-specified specs create sync burden on every minor change; under-specified specs allow silent divergence.

**Survey before building:** before implementing, check for existing code (in-repo and in dependencies) that already solves the problem. Reimplementing existing functionality is forbidden.

**Surface implicit requirements:** when a spec implicitly requires generality across a dimension (N items, concurrency, security, reliability, etc.), the agent must ask the user to clarify scope before implementing. Do not assume the degenerate case; do not assume the maximal case.

**Escalate when stuck:** when a task is harder than expected, the agent must surface this to the user rather than spiraling into rewrites or bailing silently. No effort-vs-value judgment without user input.

**Record decisions:** when a non-trivial choice is made (approach A over B, abandoning a direction, adopting a workaround), record the reasoning. For small projects this can be inline in the task or spec; for large projects, a dedicated decision record.

**Precedence when artifacts conflict:**
1. Spec over source code (code diverging from spec is a bug).
2. Spec over tests (tests derived from spec).
3. If agent suspects the spec is wrong, ask the user — do not silently override.

**Security and performance:** implementation must not introduce known antipatterns (injection, unbounded allocations, N+1 queries, bare catch, insecure defaults). These are not optional — satisfying the immediate task does not override defensive concerns.

**Session boundaries:** when resuming work across sessions, the agent must re-orient from the worklog state (specs, task status, decision records) rather than assuming continuity from a previous session's context.

> TODO: Should tests be written before task creation (as a pre-task gate derived from the spec), or as the first step within a task? The former enforces the spec→test→code ordering more strictly; the latter is more practical for tasks where the test shape isn't clear until work begins.

> TODO: When should detailed design (code layout, module boundaries, internal interfaces) be determined? It must happen after spec but before tests — tests need to know *what* to import and call. But locking detailed design too early over-constrains implementation. Tension between test-writability and implementation flexibility.

## 1. Greenfield Feature

New capability designed and built from scratch.

**Happy Path:**
1. Requirement surfaces.
2. Spec written (observable behavior, constraints, anticipated changes, dangers).
3. Tasks created from spec.
4. Tests written from spec (before implementation).
5. Implementation until tests pass.
6. Spec updated as implementation reveals adjustments. Decision recorded if a non-trivial choice was made.
7. Merge.

**Common Incidents:**
- Spec is incomplete at write time — details discovered during implementation. Spec updated mid-flight.
- Task reveals a design flaw. Spec revised, downstream tasks re-scoped. Decision recorded.
- Feature depends on another unfinished feature. Task blocked.
- Existing code partially solves the problem. Reused and extended rather than reimplemented.

**Rare but Allowed:**
- Spec abandoned mid-implementation because the requirement changed. Tasks cancelled; spec marked obsolete or rewritten. Decision recorded.
- Feature is small enough that spec + single task is sufficient (no decomposition needed).
- Implementation reveals the feature is unnecessary. Work stopped, decision record written.
- Task is harder than expected. Agent escalates to user for re-scoping.

**Forbidden:**
- Implementation without a spec (even a minimal one).
- Implementation before tests.
- Spec modified without user approval when the change alters observable behavior.
- Tests written to match implementation rather than spec.
- Reimplementing functionality that already exists in the codebase or dependencies.

## 2. Bug Fix

Something doesn't work as specified, or as reasonably expected when no spec exists.

**Happy Path:**
1. Bug reported (user, CI, monitoring).
2. Triage: severity, affected component, spec violation vs. spec gap.
3. Reproduce and root-cause.
4. Regression test written (captures the bug; fails before fix).
5. Fix until test passes.
6. Spec updated if a gap was revealed.

**Common Incidents:**
- Root cause is in a different component than the symptom. Fix touches unexpected files.
- Bug reveals a spec gap — the spec didn't cover this case. Spec amended.
- Fix is straightforward but the test setup is complex.

**Rare but Allowed:**
- Bug is a known limitation, not worth fixing now. Documented and deferred.
- Fix requires a design change significant enough to warrant a new spec or spec revision.
- Bug is in a dependency. Workaround implemented with a tracking note.

**Forbidden:**
- Routing around the bug instead of fixing it (distorting implementation to avoid triggering the defect).
- Closing the bug because a workaround exists without documenting the underlying issue.
- Fixing the specific failing case without evaluating whether the bug is a symptom of a general problem.
- Writing the regression test after the fix (test must fail before the fix to prove it captures the bug).

## 3. Refactoring

Restructuring code without changing external behavior.

**Happy Path:**
1. Motivation identified (coupling, duplication, maintainability).
2. Scope defined: what moves, what invariants hold.
3. Incremental restructuring with existing tests as safety net.
4. All tests pass, no behavioral change.

**Common Incidents:**
- Tests are coupled to implementation details and break despite no behavioral change. Tests updated.
- Refactoring reveals a latent bug (previously unreachable code path now reachable). Bug filed separately.
- Scope creeps — "while I'm here" adjacent changes. Must be resisted or split into separate tasks.

**Rare but Allowed:**
- Refactoring requires updating a spec because component boundaries changed (structural, not behavioral).
- Refactoring abandoned because the cost exceeds the benefit. Decision recorded.

**Forbidden:**
- Behavioral changes smuggled in as "refactoring."
- Refactoring without test coverage to verify behavioral preservation.

## 4. Investigation

Exploring a question without a predetermined outcome. Output is knowledge, not code.

**Happy Path:**
1. Question or hypothesis stated.
2. Experimentation: benchmarks, prototypes, reading.
3. Findings documented in task body.
4. Outcome: leads to a new task, a spec, a decision record, or nothing.

**Common Incidents:**
- Investigation reveals the question was wrong — the real problem is elsewhere. Scope pivots.
- Findings are inconclusive. Documented as-is; may be revisited.

**Rare but Allowed:**
- Investigation produces a prototype worth keeping. Promoted to a proper feature with a spec.
- Investigation reveals a critical issue requiring immediate action (escalates to hotfix).

**Forbidden:**
- Investigation that produces code merged without a spec or proper task lifecycle.
- Findings not documented (knowledge lost at session end).

## 5. Chore

Maintenance work: dependency updates, CI changes, tooling, documentation.

**Happy Path:**
1. Trigger: security advisory, deprecation, tooling need.
2. Assessment: breaking changes, migration effort.
3. Execute change.
4. Verify: CI green, no regressions.

**Common Incidents:**
- Dependency update introduces breaking changes. Migration is larger than expected.
- Chore reveals an outdated spec (e.g., doc references removed API). Spec updated.

**Rare but Allowed:**
- Chore escalates into a feature (e.g., major version migration requires architectural changes). New spec created.
- Chore is blocked by an upstream issue outside the project's control.

**Forbidden:**
- Behavioral changes introduced as part of a chore without going through the spec/task lifecycle.

## 6. Hotfix

Production is broken, immediate fix needed. Process is compressed.

**Happy Path:**
1. Incident detected.
2. Minimal triage, rapid fix.
3. Fix deployed.
4. Post-mortem: root cause, what went wrong, follow-up tasks created.

**Common Incidents:**
- First fix doesn't resolve the issue. Multiple iterations under time pressure.
- Hotfix introduces a regression. Caught in post-deploy verification; rolled back or patched.

**Rare but Allowed:**
- Hotfix knowingly introduces tech debt for speed. Follow-up task created to clean up.
- Hotfix bypasses normal review process due to severity.

**Forbidden:**
- Hotfix without a post-mortem. The shortcut is acceptable; skipping the retrospective is not.
- Hotfix used as precedent to bypass process for non-emergencies.
