<!-- TOPIC: Claude Protocol — hook-enforced task tracking and knowledge persistence for Claude Code
  SOURCE: https://github.com/weselow/claude-protocol (v3, MIT license)
  DEPS: beads (https://github.com/steveyegge/beads) for task persistence
-->
# Reference: Claude Protocol

**Source:** [weselow/claude-protocol](https://github.com/weselow/claude-protocol) — v3, fork/rewrite of Aviv Kaplan's [The Claude Protocol](https://github.com/AvivK5498/The-Claude-Protocol).

An npm-installable package (`npx claude-protocol init`) that scaffolds Claude Code configuration for hook-enforced task tracking, branch protection, and knowledge persistence. Built on [beads](https://github.com/steveyegge/beads) (git-native task tracking by Steve Yegge).

---

## What It Does

### Components Installed

```
.beads/                        # Task database (Dolt/SQLite) + knowledge base
  memory/knowledge.jsonl       # LEARNED entries (JSONL)
  memory/recall.cjs            # Keyword search over knowledge base
.claude/
  agents/
    code-reviewer.md           # 3-phase review: demo verification → spec compliance → code quality
    merge-supervisor.md        # Conflict resolution
  hooks/                       # 8 Node.js (.cjs) enforcement hooks
  rules/
    beads-workflow.md          # Task lifecycle + bd command reference
    implementation-standard.md # Code metrics, self-review triggers
    logging-standard.md        # Trigger-based: "creating API endpoint → add logging"
    tdd-workflow.md            # Trigger-based: "new function → write test first" + exceptions
    resilience-standard.md     # Trigger-based: "calling external API → what if timeout?"
  skills/
    project-discovery/         # Scans codebase, writes project-conventions.md
  settings.json                # Hook configuration
CLAUDE.md                      # Orchestrator instructions
```

### Hook Architecture

All hooks are CommonJS Node.js (cross-platform, no ESM). Configured via `.claude/settings.json`.

| Hook | Event | What It Does |
|------|-------|-------------|
| `enforce-branch-before-edit` | PreToolUse (Edit/Write) | Blocks edits on main. On feature branches, prompts with file name and change size for confirmation. Subagents bypass. Always allows CLAUDE.md, plan files, memory files, and worktree paths. |
| `bash-guard` | PreToolUse (Bash) | Blocks `git --no-verify`. Requires `-d` description on `bd create`. Validates epic close (all children done, PR merged). |
| `validate-completion` | SubagentStop | Blocks subagent from finishing unless: checklist present with all items checked, bead status set to `inreview`, code committed and pushed, comment left on bead, response within verbosity limits (25 lines / 1200 chars). |
| `memory-capture` | PostToolUse (Bash) | Extracts `LEARNED:` entries from `bd comment` commands into `.beads/memory/knowledge.jsonl`. Auto-tags by keyword matching. Rotates file at 1000 entries (archives oldest 500). |
| `session-start` | SessionStart | Shows dashboard: merged PRs awaiting cleanup, stale `inreview` beads, in-progress/ready/blocked tasks, recent knowledge entries. |
| `nudge-claude-md-update` | PreCompact | If `## Current State` section in CLAUDE.md is empty, reminds agent to update it before context compaction. |
| `recall` | (utility) | `node .beads/memory/recall.cjs "keyword"` — searches knowledge base by keyword, type, recency. Deduplicates by key. |

### Task Lifecycle (Beads Workflow)

```
Plan → Size check → Create beads → bd ready → Dispatch → Worktree → PR → Merge → Close
```

- **Size check**: >3 files or >1 domain → epic with children. >50 lines → consider splitting. Otherwise single bead.
- **One bead = one worktree = one PR = one reviewable diff.**
- Statuses: `open` → `in_progress` → `inreview` → `done`.
- Status transitions enforced by hooks (not just instructions).
- Discovered tech debt during work → immediately `bd create`, don't fix inline.
- Plan must be materialized as beads before implementation starts (plans exist only in context; beads persist through compaction).

### Knowledge Base

- `LEARNED` comments captured automatically from `bd comment` commands by `memory-capture` hook.
- Required format: problem → solution → context. Vague entries rejected ("fixed async issue" vs. "pg connection pool exhaustion under load → set max=20").
- `recall.cjs` searched before every investigation (instruction, not enforced by hook).
- Alternative of `docs/issues/*.md` notes was explicitly rejected — beads + LEARNED + recall covers it without duplication.

### Dev Rules

Rules are written as **triggers** ("when you do X, stop and do Y") rather than reference documents. The rationale: agents don't re-read reference docs on every action, but a trigger fires at action time.

- **implementation-standard**: Code metrics (CC < 10, function < 30 lines, class < 200, nesting < 4). Self-review via subagent. `/simplify` trigger when >3 files or >50 lines changed. Rule of 3 alternatives for architectural decisions.
- **tdd-workflow**: RED → GREEN → REFACTOR. Triggers: new function, bug fix, behavior change. Exceptions: configs, DTOs, migrations.
- **logging-standard**: Trigger-based for API endpoints, external calls, payments, auth, catch blocks.
- **resilience-standard**: Trigger-based for external API calls. Strategies: retry, fallback, circuit breaker, compensation.

### Code Reviewer Agent

3-phase adversarial review:
1. **Phase 0 (DEMO verification)**: Re-runs every DEMO block. If output differs from claimed, review fails immediately. Addresses the problem that implementers may paste fake output.
2. **Phase 1 (Spec compliance)**: Compares `bd show` description against `git diff`. Missing or extra work.
3. **Phase 2 (Code quality)**: Bugs, async safety, security, tests, pattern conformance.

Anti-rubber-stamp rules: must actually run commands, must cite file:line evidence, never approve when DEMO fails, never write or edit code.

### Bootstrap

Python script that:
- Installs beads CLI (tries Homebrew, npm, go in sequence).
- Copies templates with placeholder replacement.
- Merges into existing configurations (CLAUDE.md appended, settings.json hooks merged by event type, .gitignore entries appended). Does not overwrite.

---

## Design Decisions

The project maintains a `docs/decisions-en.md` documenting every v2 → v3 decision with context, alternatives, and rationale.

### Key Decisions

**Constraints over instructions.** Blocking bad actions via hooks is more effective than asking "please don't do that." Claude may ignore an instruction in a long context or after compaction. A hook fires every time. Examples: edits on main blocked (not "please don't commit to main"), `git --no-verify` blocked, `bd create` without description blocked.

**Trigger-based rules over reference documents.** Long standard documents (200+ lines) that Claude should "remember" were replaced with triggers: "when you do X, stop and do Y." A trigger fires at code-writing time — closer to muscle memory than a reference doc.

**Personas removed.** 7 named agent personas ("Rex the reviewer") were removed. Personas come from GPT-3 era prompting. Concrete checklists improve quality; personality doesn't. Personas fill context.

**Agent hierarchy flattened.** Orchestrator → Tech Supervisor → Worker became Orchestrator → general-purpose subagent. Specialized agents (Scout, Detective, Architect) duplicated built-in Claude Code capabilities (Glob, Grep, Read). Tech Supervisors generated 500+ lines of context per stack for technologies Claude already knows. Each intermediate agent = context loss.

**Beads as single source of truth.** All tasks in beads, not markdown, not TodoWrite. Beads survive compaction, session restarts, context switches. Plans exist only in context; they must be materialized as beads before implementation.

**Markdown issue notes rejected.** `docs/issues/*.md` after each closed task was considered and rejected. `bd show` + `bd comments` already contain everything. Markdown = double work.

**Node.js hooks, not bash.** Cross-platform (Windows). CommonJS because Claude Code hooks run via `node`; ESM would require package.json with `"type": "module"` in the hooks directory.

---

## Meta-Observations

### About the Project Itself

The project's `docs/decisions-en.md` is itself a notable artifact: a flat decision log documenting 20+ decisions across 7 categories, each with "before / decision / why" structure. It serves as both internal documentation and external rationale. This is effectively a lightweight ADR log in a single file — no tooling, no frontmatter, just prose sections.

The v2 → v3 rewrite was primarily subtractive: 5 specialized agents removed, 19 bash hooks replaced with 8 Node.js hooks, tech supervisor generation removed, persona system removed. The project's own evolution demonstrates the "less context is more" principle consistent with the ETH Zurich findings on context file effectiveness.

### Scope and Assumptions

The project is Claude Code-specific (hooks API, subagent model, settings.json format). It does not target Codex or Copilot.

It depends on an external CLI tool (beads) for task persistence. The bootstrap handles beads installation failure gracefully (creates `.beads/` manually, falls back to SQLite), but the workflow assumes `bd` commands are available.

The dev rules (implementation-standard, logging-standard, tdd-workflow, resilience-standard) are opinionated and domain-specific (web backend: API endpoints, SQL injection, Sentry, external API resilience). They are optional (`--no-rules` flag).

The knowledge base is append-only JSONL with keyword search. No semantic search, no expiry, no conflict resolution. Rotation at 1000 entries is the only maintenance.
