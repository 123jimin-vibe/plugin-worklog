+++
id = "t0018"
title = "Exam coverage for the new rule clusters"
tags = ["quality"]
status = "pending"
modifies = ["s0014"]
blocked_by = ["t0007", "t0009", "t0010", "t0011", "t0016"]
+++

# Exam coverage for the new rule clusters

Wording-only rule changes have under- and over-corrected before (skill-revision-comparison: S6). Each new rule cluster needs exam questions before it can be trusted.

## Scope

Questions grading:

- **Write-back** — given a genuinely stale spec, does the produced spec edit contain the new state rather than a consistency claim?
- **Comments** — does the diff reference the spec/decision instead of restating it?
- **Naming** — is the chosen public name readable without the module's context, without the rule collapsing into a naming-scheme mandate?
- **Spec register** — binding items preserved; narration and status sections absent.
- **Script invocation** — correct plugin script path from a fresh context.

Re-run the full suite; update results/skill-revision-comparison.md.

## Status note (deferred)

Deferred per user decision (kept pending). The exam targets above depend on rules from
t0007/t0009/t0010/t0011, which are unwritten — expected answers can't be grounded in spec
citations (s0014) for rules that don't exist yet, and guessing the wording would itself be
the S6 trap. Author these once those rule tasks land; they slot into the reorganized 6-file
suite from t0017 (write-back/spec-register → pitfall-governance or pitfall-spec-authoring;
script-invocation → a happy/governance question).
