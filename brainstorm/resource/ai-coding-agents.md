<!-- TOPIC: AI coding agent landscape — Claude Code, OpenAI Codex, GitHub Copilot
  DEFINES: Per-tool architecture/config/extensions/strengths/weaknesses, cross-cutting comparison table, emerging standards
-->
# AI Coding Agents — Claude Code, OpenAI Codex, GitHub Copilot

Landscape as of mid-2025. All three are CLI-first agentic coding tools
with IDE extensions. This doc catalogs what each tool does and where
they overlap.

---

## 1. Claude Code (Anthropic)

### Identity

Terminal-first agentic assistant. "Not a chat interface — an agentic
system." Reads your codebase, edits files, runs commands, manages
git, connects to external services. Also available as VSCode/JetBrains
extensions, a desktop app, and a web UI at claude.ai/code.

### Architecture

Three-layer model:

| Layer          | Purpose                                                                                                   |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| **Core**       | Main conversation context. Read, Edit, Bash, Glob, Grep, Web tools. 200K tokens (1M with extended).       |
| **Delegation** | Subagents (up to 10 parallel). Isolated context windows, return summaries. Cheaper model tiers available. |
| **Extension**  | MCP servers, hooks, skills, plugins. Deterministic automation and external integrations.                  |

Key insight per their docs: "Most users work entirely in the Core
Layer, watching context bloat. Power users push work to the Delegation
Layer."

### Configuration

- **CLAUDE.md** — Persistent project-level instructions, loaded every
  session. First 200
  lines of MEMORY.md also auto-loaded.
- **`.claude/rules/`** — File-path-scoped rules (load only when
  working with matching files).
- **Settings hierarchy**: `~/.claude/settings.json` (user) →
  `.claude/settings.json` (project) → `.claude/settings.local.json`
  (local, gitignored). JSON format.
- **Auto memory** — Claude saves learnings automatically across
  sessions (project patterns, preferences).

### Extension Mechanisms

| Mechanism       | Description                                                                                                                                                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Skills**      | Markdown files (`SKILL.md`) with YAML frontmatter. Invokable via `/skill-name` or auto-loaded by matching description. Can include scripts, templates, examples. Reference vs. action skills. Progressive disclosure (metadata first, full load on use).     |
| **Hooks**       | Deterministic shell commands at lifecycle points: `PreToolUse`, `PostToolUse`, `Notification`, `Stop`, `SessionStart`, `SessionEnd`, etc. "Use hooks (not prompts) for anything that must always execute." Also supports prompt-based and agent-based hooks. |
| **Subagents**   | Isolated context, return summaries. Built-in roles: explore, plan, general-purpose. Custom subagents with own instructions and preloaded skills.                                                                                                             |
| **Agent Teams** | Independent Claude Code sessions that message each other. Shared task list, peer-to-peer coordination. Higher token cost.                                                                                                                                    |
| **MCP**         | Model Context Protocol for external services (databases, GitHub, Sentry, 3000+ integrations).                                                                                                                                                                |
| **Plugins**     | Packaging layer. Bundle skills, hooks, subagents, MCP servers, LSP servers into a single installable unit. Marketplace. Namespaced (`plugin:skill`).                                                                                                         |
| **LSP Servers** | Plugins can provide Language Server Protocol servers for real-time code intelligence (type info, diagnostics, navigation).                                                                                                                                   |

### Prompt Transparency

**Partial.** `--dry-run` in chat shows the full prompt. CLAUDE.md and
skills are user-visible markdown. However, the system prompt itself is
**not user-configurable** — it's bundled with the product. Users can
append to it (`--append-system-prompt`) but not replace it. The
model-specific base instructions are maintained by Anthropic.

### Orchestration

- Up to 10 parallel subagents.
- Agent teams for peer-to-peer coordination.
- `/batch` skill: fan-out across codebase, one background agent per
  unit, each in isolated git worktree.
- Cloud and remote execution supported.

### Pricing

Subscription (Claude Pro/Max) or API usage-based (Console).

### Key Strengths

- Mature three-layer architecture.
- Rich plugin ecosystem with marketplace.
- Agent teams (peer-to-peer multi-agent).
- Hooks for deterministic automation.
- LSP integration via plugins.
- Multiple execution environments (local, cloud, remote control).

### Key Weaknesses

- No spec-driven workflow. No concept of specs preceding code.
- System prompt is append-only, not replaceable.
- CLAUDE.md is unstructured — no layered merge strategy.
- No formal coexistence model with other agents.
- JSON settings, not TOML.
- Tied to Claude models only.

---

## 2. OpenAI Codex

### Identity

Cross-platform local software agent. Open-source CLI (`@openai/codex`
on npm). Also: Codex Cloud (web/iOS), IDE extension (VSCode/Cursor),
macOS desktop app. "A teammate that understands your context."

### Architecture

Agent loop: user input → model inference (Responses API) → tool calls
→ loop until assistant message. Uses compaction to work across multiple
context windows for long-running tasks (24+ hours observed).

- **App Server**: JSON-RPC bidirectional protocol between clients and
  the Codex harness. Primitives: Item (atomic I/O), Turn (one unit of
  user→agent work), Thread (durable conversation container).
- **Execution**: Local sandbox by default (workspace-write, no network).
  Configurable sandbox modes.

### Configuration

- **`AGENTS.md`** — Project guidance. Loaded before agent starts work.
  Supports nested per-directory files (closer directory wins).
  Feedback-loop philosophy: "correct the agent, then update AGENTS.md."
- **`~/.codex/config.toml`** — User config. TOML format.
- **`.codex/config.toml`** — Project config (walks up directory tree).
- **Profiles** — Named config sets in `config.toml`, switchable via
  `codex --profile <name>`.
- **Custom model providers** — Define base URLs, headers, wire APIs
  for any provider (Azure, Ollama, Mistral, etc.).
- **OSS mode** — `--oss` flag for local models (Ollama, LM Studio).

### Extension Mechanisms

| Mechanism         | Description                                                                                                                                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Skills**        | `SKILL.md` files + optional scripts/references. Progressive disclosure (metadata → full load). Stored in `.agents/skills` (repo) or `$HOME/.agents/skills` (user) or `/etc/codex/skills` (admin). Open standard (Agent Skills spec). |
| **Multi-agents**  | Sub-agents with isolated contexts. Built-in roles: explorer, worker, monitor, default. Custom roles via `[agents]` config. CSV batch processing (`spawn_agents_on_csv`). Up to configurable `max_threads` / `max_depth`.             |
| **MCP**           | Standard integration. Codex itself can run as an MCP server (`codex mcp-server`).                                                                                                                                                    |
| **Automations**   | Desktop app feature: scheduled agent runs on a cron-like schedule.                                                                                                                                                                   |
| **Skill Creator** | Built-in `$skill-creator` for interactive skill scaffolding.                                                                                                                                                                         |

### Prompt Transparency

**Partial.** AGENTS.md is user-visible. `model_instructions_file` in
config can replace base instructions. Model-specific prompts live in
the open-source repo. But the system still bundles base prompts that
users would need to dig into source code to fully understand.
`base-instructions` parameter in MCP server mode allows override.

### Orchestration

- Multi-agent with configurable roles and model tiers per role.
- CSV fan-out (`spawn_agents_on_csv`) for batch operations.
- App Server enables multi-thread management from desktop app.
- Codex as MCP server enables orchestration via OpenAI Agents SDK.

### Pricing

Included with ChatGPT Plus/Pro/Business/Enterprise plans. API key
usage also supported.

### Key Models

GPT-5.1-Codex-Max as frontier. Compaction-trained for long-horizon
tasks. Model switching: `--model` flag or config.

### Key Strengths

- Open-source CLI (inspectable, forkable).
- TOML config — human-friendly, layered.
- Multi-provider support (Azure, Ollama, Mistral, custom).
- AGENTS.md as shared convention (emerging standard).
- Codex-as-MCP-server composability.
- Desktop app as "command center" for parallel agents.
- Automations (scheduled tasks).
- CSV batch fan-out for structured parallel work.

### Key Weaknesses

- No spec-driven workflow. AGENTS.md is guidance, not a formal pipeline.
- No prompt layering. Single instructions file or AGENTS.md.
- No formal coexistence model with other agents.
- Skills ecosystem still young.
- Multi-provider exists but optimized for OpenAI models.

---

## 3. GitHub Copilot (CLI + Agent Mode + Coding Agent)

### Identity

Three distinct but converging products:

1. **Copilot CLI** (`copilot`) — Terminal agent. Interactive and
   programmatic modes.
2. **Agent Mode** (VSCode) — Autonomous peer programmer within IDE.
   Multi-step coding, auto-correction loop.
3. **Coding Agent** (GitHub.com) — Async autonomous agent. Works in
   GitHub Actions environment, creates PRs.

### Architecture

- **CLI**: Agent loop with tool calls. Ask/execute mode + plan mode.
  Auto-compaction at 95% context. Built-in custom agents (code-review,
  plan, task, explore) that run in parallel.
- **Agent Mode (VSCode)**: LLM + tools (read_file, edit_file,
  run_in_terminal, etc.). Agentic loop with auto-error-detection and
  correction. Summarized workspace structure sent (not full codebase).
- **Coding Agent**: Ephemeral GitHub Actions environment. Full CI
  integration. Creates branches and PRs autonomously.

### Configuration

- **Custom Instructions** — Loaded from multiple locations:
  `AGENTS.md`, `.github/copilot-instructions.md`,
  `$HOME/.copilot/copilot-instructions.md`. Also reads `.cursorrules`
  and `CLAUDE.md` for compatibility.
- **Per-session config** — CLI flags: `--allow-tool`, `--model`,
  `--additional-mcp-config`, etc.
- **No formal config file hierarchy** comparable to Claude Code or
  Codex. Settings managed via CLI flags and instruction files.
- **Organization/enterprise policies** — Admins control model
  availability, tool access, agent permissions centrally.

### Extension Mechanisms

| Mechanism         | Description                                                                                                                                                                                                                   |
| ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Skills**        | `SKILL.md` files (Agent Skills open standard — same spec as Codex). Stored in `.github/skills` or `.claude/skills` (project) or `~/.copilot/skills` or `~/.claude/skills` (personal). Auto-invoked or explicit `/skill-name`. |
| **Custom Agents** | `.md` or `.agent.md` files with YAML frontmatter. Define specialized subagents (reviewer, docs writer, security auditor). Can restrict tools, add MCP servers, control invocability.                                          |
| **Hooks**         | Lifecycle event handlers. CLI only.                                                                                                                                                                                           |
| **MCP**           | Full MCP support. Built-in GitHub MCP server + Playwright. Configurable for coding agent via repository settings.                                                                                                             |
| **Plugins**       | Packages delivering skills, hooks, custom agents, MCP servers.                                                                                                                                                                |
| **Tools**         | Built-in + MCP-provided. Granular allow/deny per session.                                                                                                                                                                     |
| **Subagents**     | Delegated processes with own context window.                                                                                                                                                                                  |

### Prompt Transparency

**Low.** System prompt is not user-visible. Tool descriptions (like
`read_file`) are documented in blog posts but not directly exposed at
runtime. Custom instructions are visible to the user (they write them),
but what Copilot actually sends is not inspectable without reverse
engineering. No `--dry-run` equivalent.

### Orchestration

- CLI: built-in agents (code-review, plan, task, explore) run in
  parallel.
- Custom agents with model selection and tool restriction.
- Coding agent: async, GitHub Actions-based. Multiple agents can work
  on different issues simultaneously.
- Plan mode: structured implementation planning before execution.

### Pricing

Included with Copilot plans (Pro, Pro+, Business, Enterprise). Premium
model requests consumed for certain models.

### Key Strengths

- **GitHub-native integration.** PR creation, issue management, CI/CD,
  code review all built-in.
- **Coding agent** (async) is unique — delegates work entirely, comes
  back with a PR.
- **Plan mode** — closest to spec-driven among competitors (but not
  as formal).
- **Enterprise governance** — org/enterprise admin policies for model
  and tool access.
- **Agent Skills open standard** — shared with Codex, growing ecosystem.
- **Cross-compatibility** — reads `AGENTS.md`, `.cursorrules`,
  `CLAUDE.md`.

### Key Weaknesses

- Lowest prompt transparency of the three. No way to see what's sent.
- No formal config file — relies on instruction files and CLI flags.
- GitHub lock-in. Coding agent requires GitHub Actions.
- Plan mode is interactive, not persistent — plans not saved as documents.
- No formal orchestration primitives (fan-out, join, pipeline).

---

## Cross-Cutting Comparison

| Dimension               | Claude Code                         | OpenAI Codex                                   | GitHub Copilot                   |
| ----------------------- | ----------------------------------- | ---------------------------------------------- | -------------------------------- |
| **Prompt Transparency** | Partial (append-only system prompt) | Partial (replaceable base instructions in OSS) | Low (opaque system prompt)       |
| **Spec-Driven**         | No                                  | No                                             | Plan mode (ephemeral)            |
| **Config Format**       | JSON                                | TOML                                           | Instruction files + CLI flags    |
| **Config Layering**     | user→project→local                  | user→project (walks up tree)                   | Scattered                        |
| **Multi-Provider**      | Claude only                         | Multi (Azure, Ollama, etc.)                    | Multi (GPT, Claude, Gemini)      |
| **Orchestration**       | Subagents + agent teams             | Multi-agents + CSV fan-out                     | Custom agents + coding agent     |
| **Skills/Extensions**   | Plugins + skills + hooks            | Skills + MCP                                   | Skills + plugins + custom agents |
| **Offline / Local**     | No                                  | OSS mode (Ollama, LM Studio)                   | No                               |
| **Async Delegation**    | Cloud sessions                      | Cloud + automations                            | Coding agent (GH Actions)        |
| **Open Source**         | No                                  | CLI is open-source                             | No                               |

---

## Emerging Standards

1. **Agent Skills spec** — Open standard used by both Codex and Copilot. `SKILL.md` with YAML frontmatter.
2. **AGENTS.md** — De facto convention. Codex uses it formally; Copilot reads it.
3. **MCP (Model Context Protocol)** — Universal connector. All three support it.
4. **CLAUDE.md / .cursorrules / .windsurfrules** — Agent-specific instruction files.

## Notable Patterns

- Claude Code's three-layer model (Core/Delegation/Extension).
- Codex's open-source CLI and profile system (`--profile <name>`).
- Copilot's async coding agent (GitHub Actions-based).
- Hooks as deterministic guarantees (Claude Code's "hooks, not prompts" principle).
- Progressive disclosure for skills (metadata first, full load on invocation).
- CSV fan-out (Codex) for batch operations.
- None has a formal spec-driven workflow or formal agent coexistence model.
