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
