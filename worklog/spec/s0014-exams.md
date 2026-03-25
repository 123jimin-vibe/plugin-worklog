+++
id = "s0014"
title = "Exams"
tags = ["quality"]
paths = ["exams/**"]
+++

# Exams

LLM Q&A evaluation files. Each exam tests a worklog spec by feeding it as a system prompt and running questions against it.

## Purpose

Specs prescribe behavior, but predicting whether an LLM will follow a spec correctly is a false-belief task. Exams verify spec effectiveness by running questions through actual LLM calls and observing the output.

## Location

`exams/` — organized by spec under test.

## Format

TOML configs for the prompt-engineer:invoke-llm skill. The system prompt references the spec under test. User prompts are questions that probe the spec's behavioral prescriptions.

## Writing Questions

- Scenario-based, not leading.
- Prefer objective, scorable answers.
- Test edge cases and failure modes, not just happy paths.
- Comment intention and expected answer inline.
- Ground questions in realistic user inputs.

## Relationships

| Direction | Relationship         | Target |
|-----------|----------------------|--------|
| Outbound  | system prompt `file` | Spec   |

## Anticipated Changes

- Grading rubric or automated scoring.
- Convention for exam file naming relative to spec ID.
- Result archiving strategy.

## Dangers

- Leading questions that embed the expected answer bias results toward passing.
- Happy-path-only questions miss the failure modes that matter.
- Testing your interpretation of the spec rather than realistic user inputs.
- Exams not updated after spec changes — stale questions validate outdated behavior.
