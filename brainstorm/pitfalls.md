# Pitfalls for AI Agents

This file documents pitfalls for AI agents:

- Known common limitations.
- Known limitations for using some forms of "test-driven" or "spec-driven" methodology.
- Problems encountered while using the [previous version of the plugin](./resource/worklog-skill-v1.md)

## Common Limitations

### Context and Memory

- **Lack of Theory of Mind**
  - Cannot adopt a clean-reader perspective, even when explicitly instructed.
  - Manual progress exports (e.g. to `.md`) implicitly assume the reader shares the author's full context — they never do.
- **Unable to Learn from Previous Failures**
  - Same mistakes recur across sessions.
  - History is ephemeral and agent-local; not serializable or shareable.
- **No Self-Consistency across Sessions**
  - Cross-session document drift: agents generate/edit documents that contradict earlier artifacts from previous sessions.
  - No self-consistency verification across the corpus of agent-produced content.

### Context Economy

- **Context Files Are Counterproductive** ([reference](./resource/context-file-effectiveness.md))
  - LLM-generated context files (AGENTS.md, CLAUDE.md) *reduce* success rates by ~3% while increasing cost >20%.
  - Developer-written context files barely help (+4%).
  - Context files add unnecessary requirements that agents faithfully follow — even when those requirements make the task harder (style guides, architecture overviews, testing mandates).
  - Agents explore *document-directed* instead of *task-directed* when context files are present, burning tokens on orthogonal concerns.
  - Valuable context is already embedded in well-engineered codebases (types, tests, linter configs, directory structure) — AGENTS.md is the *worst* delivery mechanism for every kind of context it typically contains.

### Strategic Judgment

- **No Abort/Continue Calibration**
  - Spirals into "easy-to-do" rewrites instead of revising architectures.
  - Bails prematurely when a task is more complex than expected.
  - No effort-vs-value estimation.
- **Append-Only Bias**
  - Does not try to reuse existing code, nor to factor out common occurrences.
  - Does not remove dead code or consolidate duplicates.
  - Resulting file bloat compounds context problems over time.
- **Blindness to Tech Debt**
  - Optimizes for **"works now" over "easy to change later"**.
  - Cannot recognize when creating debt or when existing debt makes the task disproportionately expensive.
  - No model of change frequency — treats throwaway scripts and core domain modules with identical care.
- **Poor Change Locality**
  - Code satisfies the immediate task but doesn't organize for future edits.
- **No Refactoring Judgment**
  - Does not initiate refactoring; can't distinguish messy-but-stable code (ugly but rarely touched — low ROI to clean up) from messy-and-hot code (ugly *and* frequently modified — high ROI to clean up because every future change pays the mess tax).

### Codebase Awareness

- **Reinvention of Existing Code**
  - Struggles with external and internal libraries: reinvents logic that already exists in dependencies or elsewhere in the repo.
  - Especially prevalent for "trivial" utilities that are too small to document but too useful to duplicate.

### Multi-Agent Coordination

- **Sub-agents Lose Parent Context**
  - When spawning sub-agents, the parent's full context is not transferred.
- **No Inter-Agent Communication**
  - No shared state or communication channel between concurrent agents working on the same repo.
- **No Self-Awareness for Orchestration**
  - Agents lack awareness of their role, scope, and dependencies relative to other agents.

### Safety and Security

- **Quiet Antipatterns in Generated Code**
  - Security: SQL injection, XSS, insecure defaults.
  - Performance: N+1 queries, unbounded allocations.
  - Reliability: bare catch, no backoff on retries.
  - Agents know the correct patterns when asked, but satisfying the immediate task drowns out defensive concerns.

## Limitations on using TDD/DDD

**Expectation**: DDD/TDD is hard to adhere for humans because writing documentations and tests are cumbersome. AI Agents would automate this process.

**Reality**: TDD/DDD are commonly used for AI agent-based programming, but it has several severe issues.

- **Test Biased Towards "Good-Path"**
  - AI agents treat test-writing as a goal to *pass*, not a tool to *find failures*.
  - They *do* write "bad-path" tests, but only basic ones.
  - They do not attempt to think about pathological cases.
  - They even miss "common and realistic" bad-path cases.
- **Test Biased Towards Implementation**
  - Even if implementation clearly does not match intended behavior, agents write tests that pass the existing implementation.
- **Implementation-Coupled Tests**
  - Tests mirror implementation structure (mock arrangements, call order) rather than observable behavior.
  - Creates a ratchet that punishes refactoring — changing internals breaks tests even when behavior is preserved.
- **No Test Decomposition**
  - Tests become hundreds or thousands of lines, even when separation by domain is possible.
- **Hierarchy Confusion**
  - When code, tests, and documentation conflict, agents have no consistent rule for which source of truth wins.
- **Sync Drift**
  - Stale docs are worse than no docs.
- **Confusion on State**
  - No distinction between TO-DO / Ongoing / Completed.

## Limitations of Worklog v1

Worklog v1 was an attempt to mitigate some of the issues above. However, it had several issues.

- **Unclear Tier Boundaries**
  - The spec (*what*) / plan (*how*) boundary is a continuum: interface design is simultaneously a behavioral contract and an implementation decision.
  - Plans are written as ordered task lists; the plan/task distinction collapses in use.
- **Docs/Specs Incompatibility**
  - Docs are not suitable as specs; specs are equally not suitable as docs.
  - Maintaining both creates duplication; collapsing them sacrifices either precision or readability.
- **Specs Over-Specify**
  - Agents define API signatures and field names, not observable behavior.
  - Over-specified specs require re-sync on every minor implementation change.
  - Under-adhering leads to silent divergence; the spec describes intent, not reality.
- **Lifecycle Bypassed**
  - Agents modify specs inline while working, bypassing the task lifecycle.
  - Code written before spec is updated; inter-spec dependency goes unnoticed.
  - Archive and validate scripts require deliberate invocation — frequently skipped.
- **Three-Tier Ceremony**
  - Spec/plan/task classification required at the moment requirements are least clear.
  - "Skip plan for reactive work" escape hatch applied inconsistently; boundaries erode.
