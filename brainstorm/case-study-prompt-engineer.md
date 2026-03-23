# Case Study: plugin-prompt-engineer

Raw observations from using the current worklog methodology (v2) on [`../plugin-prompt-engineer`](../../plugin-prompt-engineer).

## Observations

### 2026-03-23 — Initial setup (SKILL.md only, no scripts)

- Correctly created initial specs with correct "Anticipated Changes".
  - Question: one overview spec for the entire project?
- Correctly added decision for programming language.
- Attempted decision for `requirements.txt` — over-ceremony for this repo.
- During feature discussion, modified spec without TODO markers — treated discussion as approval.
- t0001 (requirements + dependency hook): correct content and frontmatter. No mention of tests or validation.
  - Correctly archived (manually).
  - s0001 has "Structure" listing directories/files — fine for now, but risks divergence and context bloat.
  - Incorrectly assumes specific platform (Unix).

### 2026-03-23 — Post-t0001 evaluation

- Version drift: `plugin.json` already says `0.0.2`, s0001 still says `0.0.1`.
- s0002 script path mismatch: spec says `token-count.py`, actual file and SKILL.md say `count.py`.
- SKILL.md presents stub script as functional.
- `paths` in spec frontmatter tends toward enumerating specific files rather than glob patterns. e.g. s0003 lists 4 individual files instead of `plugin/scripts/**` or similar. Brittle — adding a file requires updating the spec.

### 2026-03-23 — Subagent test-writing

- Even when explicitly instructed to spawn a subagent to write tests "to prevent context pollution", the subagent read the implementation before writing tests — defeating the purpose of black-box test authoring from specs.
- Parent agent over-specifies when spawning subagents: the prompt enumerated every function, every case, and every expected behavior in plain text. This front-loads the implementation knowledge into the subagent's context anyway, making the "isolation" cosmetic. The subagent then *still* read the source file on top of that.
