+++
id = "s0014"
title = "Exams"
tags = ["quality"]
paths = ["exams/**"]
+++

# Exams

LLM Q&A evaluation files. Each exam runs questions against the delivered skill artifact (s0018) and observes whether an agent following it behaves as this project's specs prescribe.

## Purpose

Specs prescribe behavior, but predicting whether an LLM will follow a spec correctly is a false-belief task. Exams verify spec effectiveness by running questions through actual LLM calls and observing the output.

The goal of writing exams is to find failures — questions the agent gets wrong — not to confirm the agent passes. A passing exam reveals nothing about SKILL.md's limits. A failing exam reveals a gap to fix. Optimize for failure discovery: if every question passes, the exam is too easy or too obvious, not proof that SKILL.md works.

## Location

`exams/` — one directory per spec group, named for the group it probes. Exam files are named for the pitfall cluster or the condition they test, not for a spec ID. Prompt fragments shared across a group's exams — the tool sheet and the fictional worklog state — sit beside the exam files; fictional source files go in a `fixtures/` subdirectory.

## Format

TOML configs for the prompt-engineer:invoke-llm skill. Each config resolves the artifact under test into a variable and delivers it either as the system prompt or as a tool result inside the conversation body. User prompts are questions that probe the artifact's behavioral prescriptions. Model and temperature are pinned, and pinned identically across every exam in a group — cross-revision verdict tables are comparable only because they are.

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

| Direction | Relationship        | Target           |
|-----------|---------------------|------------------|
| Outbound  | artifact under test | SKILL.md (s0018) |
| Outbound  | grading reference   | Spec             |

## Tool Emulation

Some exams need to test agent behavior in realistic environments where the agent reads files, creates entities, and archives tasks. When the underlying runner does not support tool invocation, exams emulate tools via prompt conventions — tool schemas in the system prompt, tool calls as structured text in the response.

**Minimal tool set.** The emulated tools should be the smallest set that covers the entity lifecycle: orienting (reading, listing, searching), acting (writing, moving), and a shell — script invocation is itself a graded surface (s0019 X9). Other non-entity tooling is excluded unless an exam specifically targets it.

**Single-turn constraint.** Exams are single-turn — the runner sends one prompt and collects one response. Multi-step tool loops cannot be tested. Only the immediate next action (tool call, reasoning, or refusal) is observable. Workarounds: instruct the LLM to include its reasoning alongside tool calls, or encourage parallel tool calls so multiple actions are visible in one response. Rules that prescribe stop-and-wait protocols (e.g., two-step archiving) push the graded action past the single turn — seed the protocol's first step and its tool_result into the pre-baked history so the graded action is the next one. The tool sheet both sanctions verification re-reads and forbids the model from writing its own tool results, so orientation consumes the turn by default. For artifact questions, instruct the write to happen in the current response; an orientation-only turn yields no verdict.

**One scenario per file.** A TOML exam file can test multiple scenarios only when the final user message differs between them. All prior turns (system prompt, conversation history, tool results) are shared. This means each file is effectively one setup with a fan-out at the last message.

**Two patterns for injecting tool context:**

- **Pre-baked history:** Prior conversation turns already contain tool calls and results, placing the agent mid-scenario. The exam question tests what the agent does next. Tests entity knowledge — decisions, precedence, lifecycle rules.
- **Dry calls:** No prior tool history. The agent writes tool calls in its response that are never executed. The exam evaluates intent — right tool, right arguments, right order. Tests orientation and discovery — ID allocation, archive checks, reference lookups.

## Results

Raw run output is uncommitted: each exam writes its answers to a JSONL file that the ignore rules keep out of the repository. Per-revision baseline snapshots and the comprehension-probe config are local measurement scaffolding, also uncommitted — a record that cites them cites something local by design, not a broken link.

The durable record is a single append-only comparison ledger per exam group. One section per campaign round, each pairing that round's artifact levers with the questions watching them, the per-question verdicts, attributable wins, open failures, and watch items. Earlier sections are never rewritten; a corrected attribution is recorded in the round that corrected it.

Verdicts are comparable only against baselines captured on the same exam files. Where an exam file changed after its baseline was taken, a control run of the prior artifact revision against the current files separates exam noise from artifact change.

## Proposals

- Classifying the pitfalls added since the drift/framing split was drawn (S9, T7, X7, X8, X9) as drift targets or framing targets.
- Ranking the drift techniques by measured strength, so an author reaches for the strongest first.
- Making the weak-model comprehension probes a binding gate on exam changes, as they already are on artifact changes (s0018).

## Anticipated Changes

- Grading rubric or automated scoring.

## Writing Adversarial Questions

Adversarial questions push the LLM toward a wrong answer. Two requirements: the question must be misleading, and the correct answer must be irrefutable. A good adversarial question fails on first attempt — if the model passes easily, the question is not adversarial enough. Iterate until it fails, then verify the expected answer is still objectively correct.

**Irrefutability constraint.** The correct answer must follow from an explicit rule with no exception. If a reasonable person could argue the other side, the question fails as a test. Structural rules (decisions are immutable, specs cannot contain implementation details, tests before implementation) are safer targets than approval-gated rules (spec behavioral changes require user approval) — because in a user-message format, any user statement about the topic can be construed as the approval that satisfies the gate.

**Pressure source.** The misleading pressure should come from context — chat history, momentum, trivialization, social signals, the agent's own prior commitments — not from the user's exam question itself. When the user's message directly instructs the wrong action, the LLM can reasonably interpret it as authorization, making the expected answer refutable.

**Harm test.** The wrong action should cause real damage (lost audit trail, ungoverned code, false authority, untested behavior), not just violate a structural convention. If the wrong action is harmless, the question tests rule-following rather than judgment.

**Multi-turn dilution.** Prior conversation turns where the agent already agreed to the wrong action create strong pressure to follow through. The agent must course-correct mid-conversation, which is harder than rejecting a fresh request.

## Drift Techniques

Empirically validated techniques for increasing adversarial pressure, isolated by toggling one factor at a time; the lab notes beside the exam files carry the rounds. Apply these when a question passes too easily. Each technique's measured strength is stated with it — no technique is decisive alone.

**Artifact placement.** Delivering the artifact as a conversation-body tool result rather than a system prompt exposes it to attention decay as the conversation grows, and mirrors real-world delivery where skills load as conversation content. Marginal in isolation: with the artifact in the system prompt and every other vector active, the same questions still fail. It is the default delivery, not an escalation.

**Execution momentum.** Pre-baked chore turns (sed fixes, file creation, dependency bumps) between orientation and the critical question build a "just execute" pattern. Each chore is legitimately spec-free, establishing that the current session is about quick fixes. The critical question inherits this framing. Insufficient alone — execution history without the other vectors leaves the questions passing.

**Prior commitment.** The agent's own earlier suggestion — later referenced in the fan-out — creates sunk-cost pressure. When the agent already proposed a solution and the user approved it, the governance check feels redundant at execution time. Strongest on the question that cashes in the commitment; it does not carry the rest of the fan-out.

**Precedent-setting.** A chore that creates a file in an ungoverned area (e.g., a utility module) establishes that file creation there is governance-free. When the critical question asks for another file in the same area, the agent treats it as the same class of work.

**Fan-out directness.** Action-oriented wording ("Add X at path Y. Wire it into Z.") suppresses deliberation compared to open-ended wording ("We need X, what do you think?"). Specifying exact file paths and actions gives the agent an execution plan that bypasses the "should I check governance?" step. The single most impactful wording change measured.

### What drift affects and what it doesn't

Drift suppresses **process compliance** — governance checks, verification steps, archival procedures. These are steps the agent must remember to perform; drift pushes them out of active attention.

Drift does NOT suppress **reasoning quality** — spec-vs-code precedence, decision immutability, spec content constraints. These are judgment calls where both sources are visible in context; the agent can still compare and reason correctly even under drift pressure.

Target drift techniques at process-rule pitfalls (T2, T4, X2). For reasoning-rule pitfalls (S1, S5, D1, X1), use framing pressure (trivialization, user endorsement of wrong values) rather than drift.

## Single-turn coverage limits

Some pitfalls resist single-turn testing. Record the reason here rather than shipping a refutable exam.

- **X4 (inline spec edit without approval)** — the violation is the agent *spontaneously* editing a spec's behavioral content mid-task. A single user message instructing the edit reads as authorization (the irrefutability problem), so the wrong action becomes defensible. Needs a multi-turn harness that observes an unsolicited spec edit during task execution.
- **S4, X6** (Low severity) and **T1, D2** (Medium, per s0019) — deferred, not infeasible.

## Dangers

- Leading questions that embed the expected answer bias results toward passing.
- Happy-path-only questions miss the failure modes that matter.
- Testing your interpretation of the spec rather than realistic user inputs.
- Exams not updated after spec changes — stale questions validate outdated behavior.
- Adversarial questions that use direct user instructions as the trap — the LLM can treat the instruction as authorization, making the expected answer refutable.
- Treating a passing exam as validation that SKILL.md works. A pass means the question wasn't hard enough, not that the spec is sufficient.
- Changing multiple variables at once during exam iteration, then attributing the result to one variable. Isolate factors: toggle one at a time and re-run.
