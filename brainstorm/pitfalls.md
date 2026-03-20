# Pitfalls for AI Agents

This file documents pitfalls for AI agents:

- Known common limitations.
- Known limitations for using some forms of "test-driven" or "spec-driven" methodology.
- Problems encountered while using the [previous version of the plugin](./resource/worklog-skill-v1.md)

## Common Limitations

### Context and Memory

- Lack of **Theory of Mind**
- Unable to **Learn from Previous Failures**
- No **Self Consistency** across Sessions

### Strategic Judgment

- **No Abort/Continue Calibration**
  - Spirals into "easy-to-do" rewrites instead of revising architectures.
  - Bails prematurely when a task is more complex than expected.
- **Append-Only Bias**
  - Does not try to reuse existing code, nor to factor out common occurrences.
  - Does not remove dead code or consolidate duplicates.
- **Blindness to Tech Debt**
  - Optimizes for **"works now" over "easy to change later"**.

## Limitations on using TDD/DDD

**Expectation**: DDD/TDD is hard to adhere for humans because writing documentations and tests are cumbersome. AI Agents would automate this process.

**Reality**: TDD/DDD are commonly used for AI agent-based programming, but it has several severe issues.

- **Test Biased Towards "Good-Path"**
  - AI agents treat test-writing as a goal to *pass*, not a tool to *find failures*.
  - They *do* write "bad-path" tests, but only basic ones.
  - They do not attempt to think about pathological cases.
  - They even miss "common and realistic" bad-path cases.
- **Test Biased Towards Implementation**
  - Even if implementation clearly does not match intended behavior, agents write tests that pass the existing implementation.
- **No Test Decomposition**
  - Tests become hundreds or thousands of lines, even when separation by domain is possible.
- **Hierarchy Confusion**
  - When code, tests, and documentation conflict, agents have no consistent rule for which source of truth wins.
- **Sync Drift**
  - Stale docs are worse than no docs.
- **Confusion on State**
  - No distinction between TO-DO / Ongoing / Completed.

## Limitations of Worklog v1

Worklog v1 was an attempt to mitigate some of the issues above. However, it had several issues.

- **Unclear Tier Boundaries**
  - The spec (*what*) / plan (*how*) boundary is a continuum: interface design is simultaneously a behavioral contract and an implementation decision.
  - Plans are written as ordered task lists; the plan/task distinction collapses in use.
- **Docs/Specs Incompatibility**
  - Docs are not suitable as specs; specs are equally not suitable as docs.
  - Maintaining both creates duplication; collapsing them sacrifices either precision or readability.
- **Specs Over-Specify**
  - Agents define API signatures and field names, not observable behavior.
  - Over-specified specs require re-sync on every minor implementation change.
  - Under-adhering leads to silent divergence; the spec describes intent, not reality.
- **Lifecycle Bypassed**
  - Agents modify specs inline while working, bypassing the task lifecycle.
  - Code written before spec is updated; inter-spec dependency goes unnoticed.
  - Archive and validate scripts require deliberate invocation — frequently skipped.
- **Three-Tier Ceremony**
  - Spec/plan/task classification required at the moment requirements are least clear.
  - "Skip plan for reactive work" escape hatch applied inconsistently; boundaries erode.
