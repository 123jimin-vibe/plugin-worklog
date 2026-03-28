+++
id = "t0003"
title = "Pitfall exams for entity specs"
tags = ["quality"]
status = "pending"
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
