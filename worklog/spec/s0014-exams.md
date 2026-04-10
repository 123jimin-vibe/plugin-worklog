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

`exams/` — organized by spec under test. Fictional source files and other test data go in `fixtures/` subdirectories alongside the exam TOMLs.

## Format

TOML configs for the prompt-engineer:invoke-llm skill. The system prompt references the spec under test. User prompts are questions that probe the spec's behavioral prescriptions.

## Writing Questions

- Scenario-based, not leading.
- Prefer objective, scorable answers.
- Test edge cases and failure modes, not just happy paths.
- Comment intention and expected answer inline.
- Ground questions in realistic user inputs.

## Evaluation Reference

The testee (the LLM under test) sees SKILL.md as its instructions — that is the artifact being evaluated. The tester (the person or system grading answers) evaluates correctness against this project's worklog specs (`worklog/spec/`), never SKILL.md.

If the testee produces an answer that is wrong per the specs but consistent with SKILL.md, that is a SKILL.md deficiency, not a testee failure. If the testee produces an answer that is wrong per SKILL.md but correct per the specs, that is still a testee failure — the testee should follow SKILL.md as given.

Expected answers in exam comments must be grounded in spec rules with citations. When a spec is internally inconsistent (two sections contradict), the expected answer is not irrefutable — fix the spec before using it as an exam criterion.

## Relationships

| Direction | Relationship         | Target |
|-----------|----------------------|--------|
| Outbound  | system prompt `file` | Spec   |

## Tool Emulation

Some exams need to test agent behavior in realistic environments where the agent reads files, creates entities, and archives tasks. When the underlying runner does not support tool invocation, exams emulate tools via prompt conventions — tool schemas in the system prompt, tool calls as structured text in the response.

**Minimal tool set.** The emulated tools should be the smallest set that covers the entity lifecycle: orienting (reading, listing, searching) and acting (writing, moving). Git operations and other non-entity tooling are excluded unless the exam specifically targets them.

**Single-turn constraint.** Exams are single-turn — the runner sends one prompt and collects one response. Multi-step tool loops cannot be tested. Only the immediate next action (tool call, reasoning, or refusal) is observable. Workarounds: instruct the LLM to include its reasoning alongside tool calls, or encourage parallel tool calls so multiple actions are visible in one response.

**One scenario per file.** A TOML exam file can test multiple scenarios only when the final user message differs between them. All prior turns (system prompt, conversation history, tool results) are shared. This means each file is effectively one setup with a fan-out at the last message.

**Two patterns for injecting tool context:**

- **Pre-baked history:** Prior conversation turns already contain tool calls and results, placing the agent mid-scenario. The exam question tests what the agent does next. Tests entity knowledge — decisions, precedence, lifecycle rules.
- **Dry calls:** No prior tool history. The agent writes tool calls in its response that are never executed. The exam evaluates intent — right tool, right arguments, right order. Tests orientation and discovery — ID allocation, archive checks, reference lookups.

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
