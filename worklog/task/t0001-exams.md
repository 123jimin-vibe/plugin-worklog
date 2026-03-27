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
    ├── happy-path.toml
    ├── pitfalls.toml
    └── results/             # gitignored output
```

## TOML structure

Both exams share the same shape. SKILL.md as system prompt, project context injected via `[vars]`, questions as a user prompt array.

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
prompt = "You are working on the following project:\n\n{{project}}"
substitute = true

[[prompts]]
role = "user"
prompt = [...]

[output]
file = "results/<exam>-results.jsonl"
```

## Emulated tools

invoke-llm is text-in/text-out — no tool invocation. We simulate a realistic agent environment by defining tool schemas in the system prompt and letting the LLM "call" them in its response. The set is minimal: five tools that cover the full entity lifecycle.

| Tool | Signature | Covers |
|---|---|---|
| `read_file` | `(path) → content` | Reading specs, tasks, decisions, source code |
| `write_file` | `(path, content) → ok` | Creating and updating entities |
| `list_directory` | `(path) → entries[]` | ID allocation, existence checks, scanning archives |
| `move_file` | `(src, dst) → ok` | Archiving completed tasks |
| `search_files` | `(pattern, path?) → matches[]` | Reverse lookups, reference discovery, orphan detection |

**Why these five:**
- `read_file` + `list_directory` + `search_files` = the agent can orient itself in the worklog.
- `write_file` + `move_file` = the agent can act on it (create, update, archive).
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

