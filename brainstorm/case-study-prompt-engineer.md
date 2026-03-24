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

### 2026-03-23 — Brainstorming a new feature

When instructed to "brainstorm a new feature (a new function, `render_table`, in `/lib`)":
- Spec is too narrow — a new spec is generated that covers `render_table` only, rather than extending the existing spec for `/lib` or creating a broader spec for the module's formatting capabilities. Single-function specs fragment the design surface and lose context about how the function relates to its neighbors.
- Spec is not marked as WIP — created as if it were an accepted design, with no TODO markers or other indication that it came from a brainstorm and hasn't been approved. Violates the approval rule (discussion ≠ approval).

### 2026-03-23 — Verbose tests

Tests tend to be too verbose and lengthy. Agents fail to exploit the fact that many parts of the codebase — especially utilities — are already well unit-tested. This means agents can lean on other code to simplify tests:
- **Test only the unit under test.** If a function produces structured data that is later rendered by another function, test the structured data — don't re-test the rendering. E.g., a token counter that builds table data and passes it to `render_table`: unit tests should assert on the table data structure, not the final string output, because `render_table` has its own tests.
- **Use other functions to simplify test setup.** Well-tested helpers can be called in test fixtures or assertions without re-validating them inline.
- **Omit downstream coverage.** If function A calls function B, and B is extensively covered, A's tests don't need to exercise B's edge cases — only that A calls B correctly.

Integration tests may still need to verify end-to-end string output, but unit tests should stay focused on the boundary of the unit.

### 2026-03-24 — Spec directory reorganization breaks cross-references

Reorganizing the spec directory requires updating all cross-referencing links throughout the project. Specs, decisions, tickets, and SKILL.md can all reference each other by relative path — moving or renaming files silently breaks those links. There is no automated check or tooling to detect stale references after a reorganization.

### 2026-03-24 — Decision supersession is one-directional

There is a `supersedes` field on decisions, but given a decision, there is no way to know whether it *has been* superseded. The `supersedes` field only points backward (new → old); there is no forward pointer (old → new). A reader looking at an older decision has no indication that it is stale unless they happen to find the newer one. This makes it easy to act on outdated decisions.

### 2026-03-24 — Test coverage gaps from agent-written tests

Findings from an agent implementing and testing a feature end-to-end. These are project-agnostic lessons for worklog-driven test authoring:

1. **Reference docs are spec surface too.** Tests were written against the primary spec and config reference but not against a secondary reference doc that introduced a new usage pattern for an existing feature. The pattern was valid per the spec's generic wording but the test suite only exercised the variant shown in the primary reference. *Rule: When a spec delegates to reference docs, tests must cover behaviors described in all referenced documents, not just the primary one.*

2. **Test all variants of a polymorphic input.** A feature accepted two input shapes (file path arrays and inline string arrays) through the same mechanism. Tests covered one shape exhaustively and the other not at all. The implementation handled only the tested shape. *Rule: When a spec says a field accepts multiple types or shapes, each shape needs at least one test.*

3. **Unit-testing a function in isolation doesn't test the pipeline.** Variable substitution was tested as a pure function (dict in, string out) but never as part of the config-loading pipeline that produces that dict from files. The unit tests passed while the integration path could silently break. *Rule: For multi-step pipelines, at least one test should exercise the full path, not just individual stages.*

4. **Testing parse is not testing behavior.** Several tests verified that a config key existed after parsing without verifying the behavior it controls. Parsing tests give false confidence — the feature can be completely broken while the test stays green. *Rule: Tests should assert on observable outcomes, not intermediate representations.*

5. **One provider tested is not all providers tested.** When code dispatches across multiple providers/backends, testing one doesn't cover the others. Each provider had a distinct code path but only one was tested. *Rule: If the spec enumerates N providers/backends, test at least the happy path for each.*

### 2026-03-24 — Worklog structural friction (agent-reported)

Additional friction points from the same agent session, focused on worklog methodology rather than test quality:

1. **Reference docs define spec-level behavior but live outside the worklog.** A reference doc in the plugin source tree introduced a new behavioral variant (prompt arrays as sweep dimensions) that the spec body didn't fully enumerate. The worklog's `paths` globs captured it as a governed file, but there's no distinction between "file this spec governs" and "file that extends this spec's behavioral surface." Drift detection wouldn't flag a reference doc introducing behavior the spec never mentioned.

2. **Spec cross-references are fragile relative paths.** (Echoes the reorganization observation above.) Forward references in spec bodies are brittle `../infra/s0003-python-environment.md`-style paths. Every structural change is a link-repair chore. Proposed alternative: reference specs by ID only (e.g., `[s0003]`) and let tooling resolve the path.

3. **No spec-to-test traceability.** Tests existed, covered some behaviors, missed others, and there was no way to know without manually auditing specs against test files. A `tests` field in spec frontmatter (or a convention like test docstrings citing spec IDs) would make gaps greppable. The worklog already acknowledges this as a TODO.

4. **`paths` conflates ownership with relevance.** Two specs both claimed `plugin/lib/**` — one for environment setup, one for library behavior. The worklog doesn't distinguish "this spec owns this path" from "this spec touches this path." The overlap looks like a bug but is structurally valid. Drift detection can't know which spec to flag.

5. **No way to mark a spec as incomplete relative to its references.** A spec said "arrays in `[[prompts]]` are sweep dimensions" generically, but only showed the file variant. The inline-string variant was only in a reference doc. There's no worklog convention for saying "this spec delegates details to X, and X is authoritative." The gap was invisible until runtime.
