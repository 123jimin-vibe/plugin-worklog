+++
id = "t0001"
title = "Implement initial exams for entity specs"
tags = ["quality"]
status = "active"
modifies = ["s0014"]
+++

# Implement initial exams for entity specs

Create two exams — one happy-path, one pitfall-focused — to verify that LLMs follow the entity specs correctly.

## Scope

- **Example project:** a small fictional project (specs, tasks, decisions) provided as context alongside the spec under test. Gives the LLM a concrete worklog to reason about rather than abstract rules.
- **Happy-path exam:** question groups that test correct behavior — creating entities, updating status, following lifecycle, respecting precedence.
- **Pitfall exam:** question groups that probe known failure modes — over-specification, TODO markers skipped, archive without decision, spec-code conflict resolution.

Each exam is a TOML config for prompt-engineer:invoke-llm per s0014. Questions are grouped by topic within each exam.

## System prompt

SKILL.md — that's what agents actually receive. If SKILL.md doesn't convey entity rules well enough, we want to find out.

## Directory structure

```
exams/
└── entity/
    ├── context.md           # fictional project worklog state
    ├── tools.md             # emulated tool definitions (shared)
    ├── happy-create.toml
    ├── happy-lifecycle.toml
    ├── happy-update.toml
    ├── pitfall-*.toml       # pitfall exams (planned)
    └── results/             # gitignored output
```

## TOML structure

All exams share the same shape. Three system prompts (SKILL.md, emulated tools, project context), pre-baked conversation history for orientation, fan-out at the final user message.

```toml
[generation]
model = "claude-sonnet-4-6"
temperature = 0.0

[vars]
project = "context.md"

[[prompts]]
role = "system"
file = "../../plugin/skills/worklog/SKILL.md"

[[prompts]]
role = "system"
file = "tools.md"

[[prompts]]
role = "system"
prompt = "You are working on the following project:\n\n{{project}}"
substitute = true

# ... pre-baked history (user/assistant turn pairs with tool calls and results) ...

[[prompts]]
role = "user"
prompt = [...]   # array = fan-out (one run per question)

[output]
file = "results/<exam>-results.jsonl"
```

## Emulated tools

invoke-llm is text-in/text-out — no tool invocation. We simulate a realistic agent environment by defining tool schemas in the system prompt and letting the LLM "call" them in its response. The set is minimal: six tools that cover the full entity lifecycle.

| Tool | Signature | Covers |
|---|---|---|
| `read_file` | `(path) → content` | Reading specs, tasks, decisions, source code |
| `write_file` | `(path, content) → ok` | Creating and updating entities |
| `list_directory` | `(path) → entries[]` | Existence checks, scanning archives |
| `move_file` | `(src, dst) → ok` | Archiving completed tasks |
| `search_files` | `(pattern, path?) → matches[]` | Reverse lookups, reference discovery, orphan detection |
| `bash` | `(command) → stdout/stderr` | Shell commands, including worklog scripts (`next_id`, `validate`, `drift`, `list`, `search`) |

**Why these six:**
- `read_file` + `list_directory` + `search_files` = the agent can orient itself in the worklog.
- `write_file` + `move_file` = the agent can act on it (create, update, archive).
- `bash` = general-purpose shell access. The tool definition is generic — it does not hint at worklog scripts. Tests whether the agent discovers and uses scripts from SKILL.md knowledge alone. Note: current SKILL.md marks scripts as "TODO: not yet implemented" — this is intentional.
- Git operations (log, diff) are omitted. Drift detection is important but not entity-lifecycle — and adding git tools would complicate the emulation without testing entity spec knowledge.

**Why not fewer:**
- Collapsing `move_file` into write+delete loses the archiving intent signal — we want to see if the agent reaches for the right operation.
- Collapsing `search_files` into `read_file` would force the agent to know exact paths, hiding whether it can discover references.

## Tool emulation in prompts

invoke-llm is text-only — no tool-use API. We emulate tools via prompt conventions.

**Tool definitions** go in the system prompt as XML, mirroring Anthropic's native format:

```xml
<tools>
<tool name="read_file">
  <description>Read file contents.</description>
  <parameters>
    <param name="path" type="string" required="true"/>
  </parameters>
</tool>
<!-- ... other tools ... -->
</tools>
```

**Tool calls** in the LLM's response use matching XML:

```xml
<tool_use>
<name>read_file</name>
<input>{"path": "worklog/task/t0001.md"}</input>
</tool_use>
```

**Tool results** are injected as assistant/user turn pairs in the conversation history:

```xml
<tool_result>
<name>read_file</name>
<output>+++
id = "t0001"
...</output>
</tool_result>
```

**Constraints:**

- **Single-turn only.** The runner sends one prompt, collects one response. We can only check the immediate next action. Workaround: instruct the LLM to emit reasoning alongside tool calls, or encourage parallel tool calls so multiple actions are visible in one shot.
- **One scenario per file.** A TOML config can test multiple scenarios only when the last user message differs — all prior turns are shared. Each file = one setup, fan-out at the final message.

**Two usage patterns:**

1. **Pre-baked history** — prior turns already contain tool calls and results, placing the agent mid-scenario with files already read. The user question tests what it does *next*. Stronger for testing entity knowledge (decisions, precedence, lifecycle).
2. **Dry calls** — no prior tool history. The agent writes tool calls in its response that are never executed. We evaluate intent: right tool, right arguments, right order. Stronger for testing orientation and discovery (ID allocation, archive checks, reference lookups).

## Example project (context.md)

A fictional "recipe app" worklog:

- **s0001** — Recipe storage (paths: `src/recipes/**`). Has a TODO for batch import.
- **s0002** — Notification system (paths: `src/notify/**`).
- **t0001** — Add recipe tagging (modifies s0001, status: active).
- **t0002** — Fix email delivery bug (modifies s0002, status: done, still in task/ not archived).
- **t0003** — Hotfix: rate limiter bypass (modifies s0002, status: done, archived).
- **d0001** — Post-mortem for t0003 hotfix (relates_to: s0002).

## Common prompt conventions

All exam files share these conventions in the system prompt:

- **Exclusive access.** Instruct the agent that it is the only user with filesystem access. Files do not change between reads — no need to re-read a file already seen in the conversation. This prevents wasted tool calls and keeps single-turn responses focused on action.
- **Pre-baked orientation.** Conversation history contains a realistic sequence of tool calls and results that provide all background information the agent needs. The agent should not need to re-orient; the final user message is a task to act on.
- **Reasoning + tool calls.** Instruct the agent to emit its reasoning alongside tool calls, and to use parallel tool calls when actions are independent. This maximizes observable signal in a single turn.

## Happy-path exam design

Three files, one setup each, fan-out at the final user message. Questions must require SKILL.md-specific reasoning — not just general software knowledge. Without SKILL.md, the LLM should produce a fundamentally different (wrong) answer, not just a differently formatted one.

**Design principle:** Test reasoning, not templates. Each question should require the agent to infer governance from `paths`, follow workflow ordering, apply relationship semantics, or respect approval gates — things that only SKILL.md defines.

### `happy-create.toml` — Entity creation with governance

**Setup (pre-baked history):** Agent has listed all worklog directories (including archive), run `next_id` for all types, and confirmed orientation.

| # | Question | SKILL.md dependency | Without SKILL.md |
|---|---|---|---|
| 1 | "I'm about to start implementing batch import for recipes — the code will go under src/recipes/. There's a TODO for it in s0001. Create a task to track this." | Governance: `paths = ["src/recipes/**"]` → `modifies = ["s0001"]`. TODO awareness. Correct ID (t0004). Status = pending ("about to start" = not yet begun). | No paths→governance inference. Would create a standalone task without `modifies`. |
| 2 | "New feature: user accounts. Code goes under src/accounts/. We want registration, login, and session management as a single deliverable, but password requirements are still TBD. Set up the worklog." | Greenfield workflow: spec first, then task. `paths` on spec. TODO marker for TBD items. Task's `modifies` references just-created spec. "Single deliverable" = one task. | Would create a task or design doc. No spec-first workflow, no TODO convention, no `paths`. |
| 3 | "We've agreed to implement d0001's recommendations: gateway validation and per-session rate limits for notifications. Record the decision and create a task. We'll update s0002 once the work is done and reviewed." | Decision with `relates_to = ["s0002"]` + task with `modifies = ["s0002"]`. User explicitly defers spec edit. | Would record the decision and edit s0002 directly. No decision→task flow. |

### `happy-lifecycle.toml` — Task lifecycle transitions

**Setup (pre-baked history):** Agent has read t0001 (active), t0002 (done, in task/), s0001, s0002, and listed archive/task/ (contains t0003).

| # | Question | SKILL.md dependency | Without SKILL.md |
|---|---|---|---|
| 1 | "t0002 is done and I've verified it's consistent with s0002. Archive it." | Archive to `worklog/archive/task/`. `move_file` as the correct operation. User says verified — trust it. | Might delete, mark done in-place, or move to wrong location. |
| 2 | "I want to start implementing recipe tagging (t0001 scope). What's the first thing I should do?" | Tests before implementation (SKILL.md rule). t0001 is already active — no status change. Tests derive from spec (s0001), not code. | "Start coding" or "set status to active." No tests-first rule. |
| 3 | "t0001 is done — tagging is fully implemented, tested, and s0001 has been updated to document the new behavior. The batch import TODO in s0001 is unrelated. Close out t0001." | Status → done, move to archive. User confirms spec updated. Batch import TODO stays (user says "unrelated"). | Would close the task but skip archive, skip spec verification, or remove the TODO. |

### `happy-update.toml` — Spec and decision updates

**Setup (pre-baked history):** Agent has read d0001, s0001 (with batch import TODO), s0002, t0001 (active), and listed all directories.

| # | Question | SKILL.md dependency | Without SKILL.md |
|---|---|---|---|
| 1 | "s0002's Constraints section doesn't mention that notification templates are immutable after send. The observable behavior doesn't change; this is just an undocumented constraint. Add it." | Structural update = free, no approval needed. Observable behavior unchanged. | Might ask for approval, or not know the structural/behavioral distinction. |
| 2 | "d0001's recommendation to add gateway validation and per-session limits — we want s0002 to reflect this new behavior. Draft the spec update." | Behavioral change to spec → requires explicit user approval. "Draft" = present for review, not write directly. | Would edit s0002 directly without approval. |
| 3 | "We've decided the soft-delete retention window in s0001 should be 90 days, not 30. Record a decision for posterity, then update the spec — I'm approving the behavioral change." | Decision d0002 (`relates_to = ["s0001"]`) + spec update. User gives explicit approval. | Would edit s0001 without a decision record. No decision→spec-change flow. |

## Pitfall catalog (temporary — informs pitfall exam design)

Sourced from brainstorm/, entity specs (Forbidden/Dangers/Observed Agent Failure Modes), and happy-path exam results. Filtered to pitfalls that are (a) testable in single-turn emulated-tool exams, (b) specific to entity/worklog knowledge, and (c) realistic — things LLMs actually do, not hypothetical.

### Spec pitfalls

| # | Pitfall | Source | Pressure mechanism |
|---|---|---|---|
| S1 | **Implementation details in specs.** Agent includes API signatures, class names, Redis, TTL values, file paths in spec body. | s0011 Forbidden, SKILL.md Forbidden | User or conversation history describes implementation; agent leaks it into spec. |
| S2 | **Discussion treated as approval.** Agent updates spec behavioral content based on casual chat, brainstorming, or "I was thinking…" statements. | s0011 Forbidden ("discussion ≠ approval") | Prior conversation turns contain design discussion that sounds like agreement. |
| S3 | **Structural update gated unnecessarily.** Agent asks for approval to fix a typo, reword a section, or add a danger note — even though behavior doesn't change. | s0011 Updating (structural = free) | Agent over-applies the approval rule, not distinguishing structural from behavioral. |
| S4 | **Spec update contradicts related spec.** Agent updates one spec without checking parent/sibling specs for contradictions. | s0011 Dangers | Non-obvious: two specs share tags or overlapping paths. |
| S5 | **Over-specification.** Agent creates a new spec for something that should extend an existing one. | s0011 Dangers ("one per function fragments governance") | User asks for spec on a narrow sub-feature of an existing spec's domain. |
| S6 | **Code > spec precedence.** Agent treats code behavior as authoritative when it conflicts with the spec. Fixes the spec to match the code, or writes tests against the code. | SKILL.md Precedence, s0011 | Agent reads source code that diverges from spec; follows the code. |

### Task pitfalls

| # | Pitfall | Source | Pressure mechanism |
|---|---|---|---|
| T1 | **Status not maintained.** Agent starts working without setting status to active, or finishes without setting done. | s0012 Observed Failure Modes | Agent focuses on implementation, forgets lifecycle bookkeeping. |
| T2 | **Empty modifies when work touches spec-governed files.** Chore/refactor task under spec's `paths` but agent sets modifies = [] because "no behavior change." | s0012 Forbidden, Dangers | Renaming, cleanup, or refactoring that touches governed paths. |
| T3 | **Stubs presented as complete.** Agent marks task done when implementation uses mock data, placeholder returns, or TODO comments. | SKILL.md (stubs rule) | User scaffolded endpoints; agent completes the task based on shape, not substance. |
| T4 | **Archive without spec verification.** Agent moves task to archive without checking that the governing spec is still consistent. | s0012 Archiving | Agent just does move_file, doesn't read or verify the spec. |
| T5 | **Hotfix archived without decision record.** Agent archives a hotfix task without creating/linking a post-mortem decision. | s0012 Forbidden | Hotfix is done, pressure to clean up and move on. |
| T6 | **TODO markers left stale.** Agent completes work that resolves a spec TODO but doesn't remove the marker. | s0012 Observed Failure Modes | Agent focuses on code, doesn't circle back to update spec. |
| T7 | **Cancel without decision record.** Agent cancels a task (or agrees to cancel) without creating a decision explaining why. | s0012 Forbidden | User says "let's drop this" casually. |

### Decision pitfalls

| # | Pitfall | Source | Pressure mechanism |
|---|---|---|---|
| D1 | **Non-trivial edit instead of supersede.** Agent modifies an accepted decision's substance in-place (changing the choice, rationale, or consequences). Trivial fixes (typos, formatting, obvious date corrections) are acceptable. | s0013 Forbidden | The change feels small ("just update one paragraph") but alters the historical record of what was decided and why. |
| D2 | **Missing relates_to.** Agent creates a decision without linking it to the affected spec(s). | s0013 Forbidden | Decision is about process or tooling; agent doesn't think to link it. |
| D3 | **Skipped decision for hotfix.** Agent deploys/archives a hotfix without recording a post-mortem decision. | s0013 Required Creation | Urgency of hotfix overrides process; "we'll document it later." |
| D4 | **Casual statement treated as decision.** Agent records a formal decision based on an offhand remark in chat history ("we should probably switch to webhooks"). | s0011 Forbidden (discussion ≠ approval), s0014 adversarial design | Conversational momentum; the remark sounds decisive. |

### Cross-cutting pitfalls

| # | Pitfall | Source | Pressure mechanism |
|---|---|---|---|
| X1 | **Tests after implementation.** Agent writes code first, then tests — or says "we can add tests once we see it working." | SKILL.md Rules, Forbidden | Conversational momentum ("simple feature, iterate fast"). |
| X2 | **Implementation without covering spec.** Agent starts coding before a spec exists for the feature area. | SKILL.md Forbidden | User directly requests implementation; no spec mentioned. |
| X3 | **Test agent reads source code.** Agent derives tests from implementation details (function names, internal structure) rather than spec alone. | SKILL.md Forbidden, s0001 | Test seems more thorough when grounded in actual code; spec feels insufficient. |
| X4 | **Lifecycle bypass.** Agent modifies spec inline during task implementation without going through the update approval flow. | brainstorm/resource/worklog-skill-v1.md | Agent is "in the flow" of implementation; updating the spec feels like a natural part of the work. |
| X5 | **Spec change disguised as refactoring.** Agent changes observable behavior under the guise of "cleanup" or "refactoring." | SKILL.md Forbidden | The behavioral change is small and the refactor framing makes it feel safe. |

### Severity triage

Severity = how lasting and hard to reverse the damage is. A wrong status is a one-line fix. A destroyed audit trail or false authority propagating through downstream work is not.

**Critical — destroys audit trail or creates false authority that propagates.**

| # | Pitfall | Why critical |
|---|---|---|
| S2 | Discussion treated as approval | Behavioral spec change written without real approval. Downstream tasks, tests, and implementation build on false authority. Cascading damage. |
| S6 | Code > spec precedence | Spec "corrected" to match buggy code. The bug becomes authoritative. Tests validate the bug. Entire spec→test→code chain is poisoned. |
| T3 | Stubs presented as complete | Downstream work proceeds assuming feature is done. Spec TODOs removed. Discovery happens much later when something breaks in production. |
| X5 | Spec change disguised as refactoring | Behavioral change slips in undetected. No decision trail. Tests pass because they were written against the new (wrong) behavior. |
| X4 | Lifecycle bypass | Spec modified without approval during implementation. No record it happened. Other agents/sessions build on the changed spec. |

**High — loses important context that degrades over time.**

| # | Pitfall | Why high |
|---|---|---|
| D3 | Skipped decision for hotfix | Post-mortem knowledge never captured. The "why" behind the fix fades from memory. Can't be reconstructed months later. |
| T5 | Hotfix archived without decision | Same as D3 — the audit gap is in the task lifecycle rather than decision creation, but the lost knowledge is the same. |
| D4 | Casual statement as decision | A formal decision record based on an offhand remark. Future work references it as authoritative. The person who said it may not have intended a commitment. |
| T7 | Cancel without decision | Rationale for cancellation lost. Less urgent than hotfix (no production impact), but still irrecoverable context about why work was abandoned. |
| X1 | Tests after implementation | Root cause of implementation-coupled tests (X3). Nobody rewrites tests that pass, so the coupling is invisible until a refactor breaks them. The spec→test→code ordering is load-bearing in the methodology. |
| X2 | Implementation without spec | Code exists without governing spec. Drift detection blind to it. Behavior is defined only by implementation — the exact state specs exist to prevent. |

**Medium — creates governance gaps or misleading state, but fixable on discovery.**

| # | Pitfall | Why medium |
|---|---|---|
| S1 | Impl details in specs | Specs drift with every implementation change. Maintenance burden compounds. But the spec can be cleaned up — no information is lost. |
| T2 | Empty modifies on governed work | Work escapes governance tracking. Drift detection misses it. But modifies can be retroactively corrected. |
| T4 | Archive without spec verification | Spec may be inconsistent with completed work. But the inconsistency can be caught and fixed on next read. |
| T6 | Stale TODOs | Someone creates a redundant task for already-done work. Wastes effort but doesn't corrupt state. TODO can be removed when discovered. |
| D1 | Non-trivial edit instead of supersede | Alters the historical record of what was decided and why. But the scope is narrower now — trivial fixes are allowed, so only substantive changes (choice, rationale, consequences) are the pitfall. Damage is real but contained to one decision. |
| S4 | Spec contradicts related spec | Conflicting authority between specs. But can be reconciled once the contradiction surfaces. |

**Low — causes friction or delay but no corruption.**

| # | Pitfall | Why low |
|---|---|---|
| S3 | Structural update gated unnecessarily | Agent asks for unneeded approval. User says "go ahead." Delay only. |
| T1 | Status not maintained | Status is wrong but trivially correctable. No downstream corruption — just misleading signal. |
| S5 | Over-specification (fragmented specs) | Governance fragmentation. Specs can be merged later, though it's tedious. |
| D2 | Missing relates_to | Decision is orphaned. Can be linked later via search. No information destroyed. |
| X3 | Test reads source code | Implementation-coupled tests. Detectable on refactor when tests break despite unchanged behavior. |

### Testability notes

**Strongly testable (single-turn, clear right/wrong):** S1, S2, D1, D3, T3, T5, T7, X1.
These have irrefutable correct answers from explicit rules with no exception.

**Moderately testable (judgment required in grading):** S3, S6, T2, T4, T6, D4, X2.
Correct answer follows from rules, but edge-case reasoning could produce defensible alternatives.

**Hard to test in single-turn:** S4, S5, X3, X4, X5.
Require multi-step reasoning or scenarios hard to set up with pre-baked history alone.

### Priority for pitfall exams

Cross-referencing severity with testability — prioritize pitfalls that are both critical/high AND strongly testable:

| Priority | Pitfalls | Severity | Testability |
|---|---|---|---|
| **P0** | S2, T3, D3/T5, X1 | Critical/High | Strong |
| **P1** | S6, T7, D4, X2 | Critical/High | Strong–Moderate |
| **P2** | D1, S1, T2, T4, T6 | Medium | Moderate |
| Defer | S3, S4, S5, X3, X4, X5 | Low–Medium or hard to test | Low–Hard |

