<!-- TOPIC: Catalog of pain points with current AI coding agents
  DEFINES: Pain points across 7 categories (context, memory, coordination, codebase awareness, code hygiene, safety, workflow, strategic judgment)
  DEPS: goal-progress-tracking.md (continuation fix), goal-strategic-code-quality.md (detailed countermeasures), ref-context-file-effectiveness.md
-->
# Pain Points with Existing AI Coding Agents

## Context & Perspective Failure

- Agents cannot adopt a clean-reader perspective, even when explicitly instructed.
- Manual progress exports (e.g. to `.md`) implicitly assume the reader shares the author's full context — they never do. → Addressed by `goal-progress-tracking.md`: progress files are written *for* a context-free reader, not exported from a context-heavy session.
- Placing whole files into context: poor token economy, buries signal in noise.
- Large repos force reading many potentially huge files just to orient — no summarization or indexing layer.
- Accidentally reading massive log/JSON files: instant context window nuke with zero useful signal.
- Context files (AGENTS.md, CLAUDE.md) injected wholesale add noise that agents faithfully obey — empirically shown to *reduce* success rates by ~3% (LLM-generated) while increasing cost >20%. Agents follow unnecessary requirements (style guides, architecture overviews) even when they make the task harder. See `ref-context-file-effectiveness.md`.

## Memory & Learning

- No mechanism to learn from previous failures — same mistakes recur across sessions.
- History is ephemeral and agent-local; not serializable or shareable. → Partially addressed by `goal-progress-tracking.md`: useful state distilled into issue/spec progress files; raw history becomes an audit artifact, not the hand-off mechanism.
- Cross-session document drift: agents generate/edit documents that contradict earlier artifacts from previous sessions. No self-consistency verification across the corpus of agent-produced content.

## Multi-Agent Coordination

- Sub-agents lose parent context on spawn.
- No inter-agent communication channel. → Partially addressed by `goal-progress-tracking.md`: Markdown issue files serve as a filesystem-level lingua franca — any agent can read/update them without MCP.
- Agents lack self-awareness for orchestration (role, scope, dependencies).

## Codebase & Tooling Awareness

- No integration with language servers — agents ignore type hints, go-to-definition, symbol lookup, etc.
- Struggles with external and internal libraries: reinvents logic that already exists in deps or elsewhere in the repo.

## Code Hygiene

- Agents default to appending — they rarely refactor into separate files or remove dead code.
- Resulting file bloat compounds context problems over time.
- **Poor change locality.** Code satisfies the immediate task but doesn't organize for future edits — optimizes for "works now" over "easy to change later."
- **No refactoring judgment.** Agents don't initiate refactoring; can't distinguish messy-but-stable from messy-and-hot code.
- **Implementation-coupled tests.** Tests mirror implementation structure (mock arrangements, call order) rather than observable behavior, creating a ratchet that punishes refactoring.

Detailed analysis and countermeasures: `goal-strategic-code-quality.md` §1, §4, §5.

## Safety & Security

- Catastrophic commands: unchecked destructive operations (e.g. `rm` wiping a disk).
- Adversarial hijacking vectors:
  - Non-user-controllable malicious input (prompt injection).
  - Malicious shared skills/prompts.
  - Malicious repository content.
- **Quiet antipatterns in generated code.** Security (SQL injection, XSS, insecure defaults), performance (N+1, unbounded allocations), reliability (bare catch, no backoff) — agents know the correct patterns when asked, but satisfying the task drowns out defensive concerns.

Detailed analysis and countermeasures: `goal-strategic-code-quality.md` §2.

## Workflow & DevEx

- Agent config doesn't sync across devices.
- No local async agent deployment — can't run parallel tasks on one repo.

## Strategic Judgment

- **No abort/continue calibration.** Spiral (5 rewrites, each worse) or premature bail. No effort-vs-value estimation.
- **Tech debt blindness.** Can't recognize when creating debt or when existing debt makes the task disproportionately expensive.
- **No cost-of-change awareness.** Treat throwaway scripts and core domain modules with identical care; no model of change frequency.

Detailed analysis and countermeasures: `goal-strategic-code-quality.md` §3.
