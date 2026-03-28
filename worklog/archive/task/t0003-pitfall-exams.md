+++
id = "t0003"
title = "Pitfall exams for entity specs"
tags = ["quality"]
status = "done"
modifies = ["s0014", "s0019"]
+++

# Pitfall exams for entity specs

Create pitfall-focused exams that probe known LLM failure modes from s0019. Uses the same infrastructure established in t0001 (emulated tools, example project, TOML conventions).

## Testability

How well each s0019 pitfall can be tested in single-turn emulated-tool exams (per s0014).

**Strong** (irrefutable correct answer from explicit rule): S1, D1, T3, X1.

**Moderate** (correct answer follows from rules, but edge cases exist): S2, S5, T2, T4, T6, D3, X2.

**Hard** (multi-step reasoning or difficult setup): S3, S4, X3, X4, X5.

## Exam priority

Cross-referencing s0019 severity with testability:

| Priority | Pitfalls | Severity | Testability |
|---|---|---|---|
| **P0** | T3, X1, S5 | Must | Strong |
| **P2** | D1, S1, T2, T4, T6, X2 | Medium/High | Moderate |
| Defer | S2, S3, S4, X3, X4, X5 | Low or hard to test | Low–Hard |

## Exam file plan

Three files, grouped by shared pre-baked context. All questions in one TOML share the same conversation history; fan-out at the final user message.

**Context reuse:** Pre-baked context (fictional source files, stub code, conflicting implementations) should be extracted into small standalone files referenced via `[vars]`, not inlined into TOML. This keeps TOML files small and lets pitfall exams share context fragments with each other and with happy-path exams (e.g., context.md, tools.md).

### `pitfall-completion.toml` — Task completion with visible stubs

**Context:** Agent has read an active task, its governing spec (which has a TODO that the implementation resolved), and source code that contains stubs (placeholder returns, TODO comments).

| Pitfall | Fan-out question | What correct answer looks like |
|---|---|---|
| T3 | "Implementation is done, mark the task complete." | Flags stubs, does not mark done. |
| T4 | "Archive this task, it's done." | Verifies spec consistency before archiving. |
| T6 | "Batch import is implemented. Update the spec." | Removes the resolved TODO marker. |

### `pitfall-precedence.toml` — Spec vs code conflict

**Context:** Agent has read a spec and source code that conflicts with it. Task is active.

| Pitfall | Fan-out question | What correct answer looks like |
|---|---|---|
| S5 | "Code does Y but spec says X — resolve." | Trusts spec, flags code as buggy. |
| X1 | "Start working on this task, write tests." | Derives tests from spec, not the code already visible in context. |

### `pitfall-governance.toml` — Entity creation and modification

**Context:** General "oriented agent" setup — agent has read all existing entities and listed directories. Similar to happy-create's pre-baked history. Each question sets up its own scenario in the user message.

| Pitfall | Fan-out question | What correct answer looks like |
|---|---|---|
| D1 | "Fix d0001: change the rationale section — we framed it wrong." | Supersedes with a new decision instead of editing in-place. |
| S1 | "Create a spec for the new caching layer at src/cache/." | Describes observable behavior, no impl details (class names, API signatures). |
| T2 | "Refactor notification templates under src/notify/. No behavior change, just cleanup." | Sets `modifies = ["s0002"]` because src/notify/ is governed by s0002. |
| X2 | "Implement a health-check endpoint at /status." | Recognizes no covering spec exists; creates or requests one before implementing. |
