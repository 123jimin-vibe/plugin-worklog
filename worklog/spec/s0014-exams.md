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

## Writing Adversarial Questions

Adversarial questions push the LLM toward a wrong answer. Two requirements: the question must be misleading, and the correct answer must be irrefutable.

**Irrefutability constraint.** The correct answer must follow from an explicit rule with no exception. If a reasonable person could argue the other side, the question fails as a test. Structural rules (decisions are immutable, specs cannot contain implementation details, tests before implementation) are safer targets than approval-gated rules (spec behavioral changes require user approval) — because in a user-message format, any user statement about the topic can be construed as the approval that satisfies the gate.

**Pressure source.** The misleading pressure should come from context — chat history, momentum, trivialization, social signals, the agent's own prior commitments — not from the user's exam question itself. When the user's message directly instructs the wrong action, the LLM can reasonably interpret it as authorization, making the expected answer refutable.

**Harm test.** The wrong action should cause real damage (lost audit trail, ungoverned code, false authority, untested behavior), not just violate a structural convention. If the wrong action is harmless, the question tests rule-following rather than judgment.

**Multi-turn dilution.** Prior conversation turns where the agent already agreed to the wrong action create strong pressure to follow through. The agent must course-correct mid-conversation, which is harder than rejecting a fresh request.

## Dangers

- Leading questions that embed the expected answer bias results toward passing.
- Happy-path-only questions miss the failure modes that matter.
- Testing your interpretation of the spec rather than realistic user inputs.
- Exams not updated after spec changes — stale questions validate outdated behavior.
- Adversarial questions that use direct user instructions as the trap — the LLM can treat the instruction as authorization, making the expected answer refutable.
