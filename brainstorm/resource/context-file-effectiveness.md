<!-- TOPIC: ETH Zürich study on AGENTS.md/CLAUDE.md effectiveness
  DEFINES: Key findings (LLM-generated hurts -3%, developer-written +4%, cost +20%), why overviews misdirect agents, what context files should contain (residual only)
  DEPS: (none — primary source)
-->
# Reference: Context File Effectiveness (ETH Zürich, Feb 2026)

**Source:** Gloaguen et al., "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?" — [arxiv.org/html/2602.11988v1](https://arxiv.org/html/2602.11988v1)

First rigorous empirical study of whether AGENTS.md / CLAUDE.md files
actually help coding agents solve tasks. Tested across multiple agents,
models, and both popular (SWE-bench Lite) and niche (AGENTbench)
repositories.

---

## Key Findings

### 1. LLM-Generated Context Files *Hurt* Performance

- Average **−3% success rate** vs. no context file.
- Robust across different LLMs and prompts used to generate them.
- Agent-developer `/init` commands (Claude, Codex, Copilot) produce
  these automatically — and the paper says *don't use them*.

### 2. Developer-Written Context Files Barely Help

- Average **+4% success rate** vs. no context file.
- Only marginally better than nothing, despite being hand-crafted by
  maintainers who know the codebase.

### 3. Context Files Increase Cost by >20%

- Both LLM-generated and developer-written files cause agents to
  explore more broadly: more files traversed, more tests run, more
  reasoning steps.
- This extra exploration *does not translate to better outcomes* — it
  just burns tokens.

### 4. Agents Respect Instructions (Too Well)

- Context files add unnecessary requirements that agents faithfully
  follow — even when those requirements make the task harder.
- Style guides, testing mandates, and architecture rules become
  constraints that distract from the actual task.

### 5. The Paper's Recommendation

> "Human-written context files should describe only minimal
> requirements."

Omit LLM-generated files entirely. For human-written files: include
only things the agent *cannot discover on its own* and that are
*necessary for correctness* (e.g., specific tooling commands, critical
invariants).

---

## AGENTbench (Their Benchmark)

- 138 instances across 12 niche Python repos with developer-committed
  context files.
- Complements SWE-bench Lite (popular repos, no pre-existing context
  files).
- Niche repos have less strict PR conventions — many PRs lack tests,
  requiring LLM-generated test suites (75% avg coverage of changed
  code).
- Code and benchmark at: github.com/eth-sri/agentbench

---

## Deeper Analysis: Why Overviews *Feel* Helpful But Aren't

The intuitive objection: "Surely a repository overview helps an agent
orient." The paper says otherwise. Assuming the paper is not flawed,
the resolution:

**Agents and humans explore differently.** A human reading an
unfamiliar codebase is slow — opening files, scrolling, building a
mental map takes minutes to hours. An overview is a shortcut past
expensive exploration. An agent greps the entire codebase in
milliseconds. The exploration the overview bypasses is nearly free.

**Static overviews misdirect agent exploration.** Without a context
file, the agent explores *task-directed*: the issue mentions a parser
bug → find the parser → read it → fix it. With a context file, the
agent explores *document-directed*: the file mentions testing
conventions → look at tests; mentions architecture → consider
architectural constraints. The extra exploration is orthogonal to the
task and burns tokens without benefit.

**The valuable context is already IN the codebase — when the codebase
is well-engineered:**

| AGENTS.md Prose                     | Embedded Equivalent                     | Why Embedded Wins                              |
| ----------------------------------- | --------------------------------------- | ---------------------------------------------- |
| "Follow PEP 8"                      | Linter config + format-on-save          | Zero context tokens; enforced, not advisory    |
| "Auth module exposes X, Y, Z"       | JSDoc / type signatures                 | Co-located, machine-verifiable, can't go stale |
| "Expected behavior for empty input" | Test case                               | Executable, binary pass/fail feedback          |
| "We use hexagonal architecture"     | Directory structure + import lint rules | Discoverable from `ls`; enforced by tooling    |
| "Run `make test`"                   | Standard `npm test` / `pytest`          | Conventional; agent already knows              |

The gradient: prose → types/docs → tests → linter rules → CI gates.
Each step is cheaper in context tokens, harder to go stale, and
stronger in enforcement. AGENTS.md is the *worst* delivery mechanism
for every kind of context it typically contains.

**What AGENTS.md should contain (the residual):** Only non-discoverable
knowledge that cannot be encoded as tooling:
- Negative constraints / ADRs ("we rejected X because Y")
- Tooling gotchas ("Docker must be running for integration tests")
- Temporary migration notes ("module Y being rewritten in src/y-v2/")

This residual is small. The paper's +4% from developer-written files
is this residual working. The −3% from LLM-generated files is
categories 1 and 2 (discoverable + constraining) drowning it.

**Implication for Risty:** The goal is not "write better AGENTS.md."
It is "make the repo not need one." See `goal-agent-native-repo.md`.

---

## Implications for Risty

Strategic response captured in `goal-agent-native-repo.md`. Key
derived decisions: no LLM-generated AGENTS.md, context files compete
for budget (not guaranteed inclusions), section-level scoring,
`risty doctor` audits context files, warn at >600 words or >10
sections. Risty is subtractive (score → trim → budget) where
competitors are additive.

---

## Open Questions

1. **Does section-level selective inclusion actually help?** The paper
   tested all-or-nothing. Risty's proposed section-granular approach
   is untested — could be the sweet spot, could add its own overhead.

2. **Does the "minimal requirements" finding transfer to non-Python
   repos?** AGENTbench is Python-only. TypeScript repos (Risty's
   primary target) may behave differently.

3. **Are the results model-dependent?** The paper tested across
   multiple models but the landscape evolves fast. Future models
   trained *on* context files might handle them better.

4. **Task difficulty interaction.** Do context files help more on
   harder tasks? The paper's aggregated metrics may hide a useful
   signal for complex multi-file changes.

5. **Does the cost increase matter if token prices keep falling?**
   The 20% cost increase might become negligible — but the success
   rate *decrease* won't.
