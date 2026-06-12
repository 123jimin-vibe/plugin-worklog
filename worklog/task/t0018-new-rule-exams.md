+++
id = "t0018"
title = "Exam coverage for the new rule clusters"
tags = ["quality"]
status = "done"
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

## Status note

Was deferred per user decision while the rule tasks were unwritten; t0007/t0009/t0010/t0011/t0016
landed their rules (same session), unblocking this. Slotting per the t0017 plan: write-back →
completion-drift; spec-register → pitfall-spec-authoring; comments/naming → pitfall-precedence
(its pre-baked source fixtures fit); script-invocation → happy + archive-flow comments.

## Outcome

- Write-back: completion-drift restructured with a seeded archive.py dry-run turn (the two-step
  protocol pushed the graded action past the single turn) and a true-premise fixture
  (`batch_import` added); the laundering failure is now observable in-turn.
- Comments/naming: precedence gained X7/X8 questions with a seeded current-file read-back and
  in-turn forcing; first valid run shows both traps firing (spec rules restated into comments;
  generic-name dodge plus "refactor needs no spec" reasoning).
- Spec register: spec-authoring Q6 (S9) — register held on first run, marker-removal-on-claim
  fired; question retained as the S9/verification probe.
- Script invocation: covered by observation across archive-flow questions (X9 cured in r3+;
  paths graded in comments) plus happy's corrected pre-baked history; no dedicated question.
- Q4 in-turn forcing fixed the no-artifact gap; stale expectations (happy Q6, drift Q3)
  modernized; tools.md sanctions verification re-reads and bans fabricated tool_results.
- Full suite re-run and the iteration table recorded in results/skill-revision-comparison.md
  (2026-06-12 section), including per-revision provenance, open failures, and next levers.
