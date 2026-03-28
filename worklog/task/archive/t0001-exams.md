+++
id = "t0001"
title = "Initial exam setup and happy-path exams"
tags = ["quality"]
status = "done"
modifies = ["s0014"]
+++

# Initial exam setup and happy-path exams

Exam infrastructure (emulated tools, example project, TOML conventions) and three happy-path exams verifying correct entity lifecycle behavior.

## Scope

- **Example project:** a small fictional project (specs, tasks, decisions) provided as context alongside the spec under test. Gives the LLM a concrete worklog to reason about rather than abstract rules.
- **Happy-path exam:** question groups that test correct behavior — creating entities, updating status, following lifecycle, respecting precedence.

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

