<!-- TOPIC: Evaluation of 10 development paradigms against 8 agent-native properties
  DEFINES: 8 evaluation criteria (A-H), per-paradigm alignment scores
-->
# Development Paradigms — Evaluation

Catalog of existing software development paradigms, evaluated against
properties an agent-native codebase demands.

## Evaluation Criteria

Eight properties for agent-native development:

| #   | Property                     | What it means                                                                                       |
| --- | ---------------------------- | --------------------------------------------------------------------------------------------------- |
| A   | Agent-native by construction | Repo communicates intent via types, tests, tooling, structure — not prose. AGENTS.md length = debt. |
| B   | Spec-first, test-permanent   | Work begins as a spec; specs decay into tests; tests are the durable behavioral record.             |
| C   | Continuous verification      | Fast, tight feedback loops. Agents (and humans) verify changes within seconds, not days.            |
| D   | Small increments             | Atomic, trunk-based changes. Short-lived branches. Minimized divergence window.                     |
| E   | Tooling-as-law               | Conventions enforced by linters, formatters, type checkers, CI gates — not by documents.            |
| F   | Transparent & auditable      | All intent (prompts, specs, decisions) is visible, version-controlled, and inspectable.             |
| G   | Multi-agent / multi-actor    | Any competent agent or human can orient, navigate, verify, conform, scope — without onboarding.     |
| H   | Progressive disclosure       | Adoption is a gradient, not a gate. Value delivered at every point on the commitment spectrum.      |

---

## Existing Paradigms

### 1. Waterfall

Sequential phases: Requirements → Design → Implementation → Testing →
Deployment → Maintenance. Each phase completes before the next begins.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                                                 |
| --------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ✗     | Produces massive requirements docs and design docs — exactly the prose-heavy artifacts that become structural debt. Structure emerges late (implementation phase), divorced from the spec that motivated it. |
| B — Spec-first              | ◐     | Specs *do* come first, but they're frozen Word documents, not living artifacts that decay into tests. The spec and the code diverge permanently after handoff.                                        |
| C — Continuous verification | ✗     | Verification happens once, at the end. Feedback loop measured in months. A defect discovered in testing traces back to a requirements decision made six months ago.                                   |
| D — Small increments        | ✗     | The unit of work is a *phase*, not a change. Integration is a discrete event (often traumatic).                                                                                                       |
| E — Tooling-as-law          | ✗     | Conventions live in style guides and design standards documents. Enforcement is review-based, not automated.                                                                                          |
| F — Transparent             | ◐     | Everything is documented, but in disconnected artifacts (SRS, SDD, STD). Traceability is manual and decays.                                                                                           |
| G — Multi-agent             | ✗     | Requires extensive onboarding per phase boundary. Handoff documents *are* the onboarding — and they go stale.                                                                                         |
| H — Progressive disclosure  | ✗     | All-or-nothing. You're either doing waterfall or you're not.                                                                                                                                          |

**Takeaway:** The discipline of specifying before building.
Nothing else.

---

### 2. Agile (Scrum / Kanban / XP)

Iterative delivery in short cycles (sprints). Working software over
comprehensive documentation. Customer collaboration, responding to
change.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                                                                                                                                                  |
| --------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A — Agent-native            | ✗     | Agile's "working software over comprehensive documentation" is often interpreted as "don't document at all." The codebase communicates nothing beyond what it accidentally reveals. User stories live in Jira, not in the repo. Oral tradition ("ask Sarah, she knows the auth module") is normalized. |
| B — Spec-first              | ◐     | User stories *precede* code, but they're informal, live outside the repo, and have no mechanical path to becoming tests. Acceptance criteria exist but are checked manually. XP's test-first is the exception — see TDD below.                                                                         |
| C — Continuous verification | ◐     | Sprint reviews provide periodic verification. CI is common but not inherent to the methodology. XP mandates it; Scrum doesn't.                                                                                                                                                                         |
| D — Small increments        | ✓     | Core strength. Sprints enforce time-boxed delivery. Kanban's WIP limits enforce flow. Stories are small by design.                                                                                                                                                                                     |
| E — Tooling-as-law          | ✗     | Agile is methodology-first, tooling-agnostic. "Definition of Done" is a social contract, not a CI gate.                                                                                                                                                                                                |
| F — Transparent             | ◐     | Standups, boards, and retrospectives are transparent within the team. But the *AI-readable artifact trail* is poor — decisions live in Slack, standups are ephemeral, retro action items disappear.                                                                                                    |
| G — Multi-agent             | ✗     | Agile teams build shared mental models via co-location and conversation. An agent arriving mid-sprint has zero context. The "osmotic communication" that makes Agile work for humans is invisible to machines.                                                                                         |
| H — Progressive disclosure  | ◐     | Agile itself is adoptable incrementally (start with standups, add sprints later). But it provides no tooling gradient — you're either using the process or you're not.                                                                                                                                 |

**Takeaway:** Small increments, iterative delivery, responding
to change. The *rhythm* of agile, not the ceremonies.

---

### 3. Test-Driven Development (TDD)

Red → Green → Refactor. Write a failing test first, make it pass with
minimal code, then refactor. Tests drive design.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                                                                               |
| --------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ◐     | Tests are co-located behavioral documentation that can't go stale. Descriptive test names *are* specs. But TDD alone doesn't enforce types, directory structure, or tooling — a TDD codebase can still be a navigational nightmare. |
| B — Spec-first              | ✓     | Tests *are* the spec in TDD. The spec is executable from the start, not a prose document that decays. This is the purest form of "spec-first, test-permanent."                                                                      |
| C — Continuous verification | ✓     | Core strength. Every change is verified within seconds. The feedback loop is as tight as it gets.                                                                                                                                   |
| D — Small increments        | ✓     | Red-Green-Refactor forces tiny steps. Each cycle produces a passing test and a small code change.                                                                                                                                   |
| E — Tooling-as-law          | ◐     | Tests enforce behavior, but TDD doesn't mandate linters, formatters, or type checkers. It's a discipline, not a toolchain.                                                                                                          |
| F — Transparent             | ✓     | Tests are the most auditable form of intent — they execute, they pass or fail, they're version-controlled.                                                                                                                          |
| G — Multi-agent             | ◐     | An agent can read tests to understand behavior, run them to verify changes. But TDD doesn't address orientation (directory structure, module boundaries) or conformance (style, naming).                                            |
| H — Progressive disclosure  | ◐     | TDD can be adopted per-module. But it's a binary discipline within each scope — you're either writing the test first or you're not.                                                                                                 |

**Takeaway:** The core insight — tests are the permanent
behavioral record. The decay path: `spec → test → code`. Adding
a *prose spec* phase before the test helps, because agents (and humans)
benefit from a requirements conversation before jumping to test code.

---

### 4. Behavior-Driven Development (BDD)

Extension of TDD. Specs written in structured natural language
(Given/When/Then), executable via tools like Cucumber. Bridges the
gap between business requirements and test code.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                                                                        |
| --------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ◐     | Feature files are readable specs that live in the repo. But Gherkin's rigid syntax adds a translation layer — the `.feature` file and the step definitions are coupled but physically separated, creating a maintenance tax. |
| B — Spec-first              | ✓     | Specs precede code *and* they're executable. The spec-to-test path is mechanical (step definitions).                                                                                                                         |
| C — Continuous verification | ✓     | Scenarios run as tests. Same tight feedback loop as TDD.                                                                                                                                                                     |
| D — Small increments        | ✓     | Scenarios are naturally granular.                                                                                                                                                                                            |
| E — Tooling-as-law          | ◐     | The Gherkin-to-test toolchain enforces spec-test correspondence. But it's domain-specific tooling, not general convention enforcement.                                                                                       |
| F — Transparent             | ✓     | Feature files are the most human-readable test artifacts. Intent is explicit and version-controlled.                                                                                                                         |
| G — Multi-agent             | ◐     | An agent can read `.feature` files to understand behavior. But step definitions require navigating a non-obvious mapping layer.                                                                                              |
| H — Progressive disclosure  | ✗     | BDD requires buying into the full Gherkin + step-definition stack. High ceremony cost per scenario.                                                                                                                          |

**Takeaway:** Specs should be readable *and* verifiable. But the
translation layer is rejected — specs are Markdown, tests are native
test code, and the decay is a one-way promotion (spec → tests), not
a bidirectional sync.

---

### 5. Trunk-Based Development (TBD)

All developers commit to a single branch (trunk/main). Short-lived
feature branches (< 1 day) or direct trunk commits. Feature flags
instead of long-lived branches. CI runs on every commit.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                         |
| --------------------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ◐     | Small, frequent commits produce a readable git history. But TBD is a branching strategy, not a design methodology — it says nothing about types, structure, or documentation. |
| B — Spec-first              | ✗     | TBD is implementation-focused. No spec concept.                                                                                                                               |
| C — Continuous verification | ✓     | CI on every commit. Integration is continuous by definition.                                                                                                                  |
| D — Small increments        | ✓     | Core strength. The methodology *is* small increments.                                                                                                                         |
| E — Tooling-as-law          | ◐     | CI gates are enforced. But TBD doesn't mandate what the gates check.                                                                                                          |
| F — Transparent             | ◐     | Git history is transparent. But intent behind changes is only as good as commit messages.                                                                                     |
| G — Multi-agent             | ✓     | Minimal divergence window means minimal merge conflicts between parallel agents. Small atomic commits are easy to review and understand in isolation.                         |
| H — Progressive disclosure  | ✓     | Can be adopted by one developer on a team. No all-or-nothing ceremony.                                                                                                        |

**Takeaway:** The branching model wholesale. Short-lived
branches, atomic commits, trunk as source of truth.

---

### 6. Domain-Driven Design (DDD)

Model the domain explicitly. Bounded contexts, ubiquitous language,
aggregates, repositories, domain events. The code structure mirrors
the business domain.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                                                                                            |
| --------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A — Agent-native            | ✓     | When done well, DDD produces self-describing code — the directory structure *is* the architecture, names *are* the domain vocabulary, boundaries *are* enforceable. This is the closest existing paradigm to "repo communicates its own intent." |
| B — Spec-first              | ◐     | DDD starts with domain modeling (Event Storming, etc.), which is a form of spec work. But the models are often whiteboard artifacts, not repo-resident.                                                                                          |
| C — Continuous verification | ✗     | DDD is a design paradigm, not a verification paradigm. Compatible with CI but doesn't mandate it.                                                                                                                                                |
| D — Small increments        | ◐     | Bounded contexts enable independent evolution. But DDD projects often start with a large upfront modeling effort.                                                                                                                                |
| E — Tooling-as-law          | ◐     | Module boundaries can be enforced via import restrictions. But DDD conventions (aggregate rules, event patterns) are typically enforced by code review, not tooling.                                                                             |
| F — Transparent             | ◐     | The ubiquitous language makes intent explicit *in code*. But design decisions and boundary rationale live in wikis or architects' heads.                                                                                                         |
| G — Multi-agent             | ✓     | Bounded contexts are the ideal unit of agent scope. An agent assigned to a bounded context has clear inputs, outputs, and invariants — without needing global repo knowledge.                                                                    |
| H — Progressive disclosure  | ◐     | Can be applied to one module/context at a time. But the upfront modeling investment is significant.                                                                                                                                              |

**Takeaway:** Directory-as-architecture. Bounded contexts as
scope boundaries for agents. Ubiquitous language as self-documenting
naming. ADRs (from the DDD-adjacent community) for non-discoverable
decisions.

---

### 7. Documentation-Driven Development

Write the docs first (API docs, README, user guide), then implement
to match. The documentation is the spec.

Reference formulation: Zach Supalla's DDD manifesto (2014) —
document first → get user feedback → TDD aligned with docs → when
docs change tests change → version docs with software.

**Alignment (classical — human-maintained):**

| Property                    | Score | Notes                                                                                                     |
| --------------------------- | ----- | --------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ✗     | Produces more prose, not less. Docs drift from code. The paradigm *is* the structural debt.               |
| B — Spec-first              | ✓     | Docs-first is spec-first by definition.                                                                   |
| C — Continuous verification | ✗     | Docs aren't executable. Drift between docs and code is detected only by humans reading both.              |
| D — Small increments        | ◐     | Docs can be written incrementally. But the doc-then-code cycle adds latency per increment.                |
| E — Tooling-as-law          | ✗     | Documentation is the opposite of tooling-as-law — it's advisory by nature.                                |
| F — Transparent             | ✓     | Intent is maximally explicit (it's written down).                                                         |
| G — Multi-agent             | ✗     | Agents reading stale docs is worse than agents reading no docs (see `ref-context-file-effectiveness.md`). |
| H — Progressive disclosure  | ✓     | Write docs for what you're building. No ceremony beyond that.                                             |

**Alignment (LLM-projected — tests and docs derived by LLM):**

DDD's three fatal flaws (double maintenance, unverifiable prose,
triple cost) all stem from *human* maintenance of derived artifacts.
When an LLM serves as a projection engine — generating tests from
docs and regenerating them on doc changes — the economics invert:

| Property                    | Score | Notes                                                                                                                                                   |
| --------------------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ◐     | Prose still exists, but it is the *source* from which verifiable artifacts are projected — not dead weight. Projected tests and types are agent-native. |
| B — Spec-first              | ✓     | (unchanged)                                                                                                                                             |
| C — Continuous verification | ✓     | Prose is verified *through* its projected tests. If projected tests fail, the prose is wrong (or the code is). Mechanical linkage achieved.             |
| D — Small increments        | ✓     | Doc-then-project-tests is fast when the projection step is automated.                                                                                   |
| E — Tooling-as-law          | ◐     | The LLM projection engine *is* the tooling that enforces doc-test correspondence. Not a static linter, but an active sync mechanism.                    |
| F — Transparent             | ✓     | (unchanged)                                                                                                                                             |
| G — Multi-agent             | ✓     | Docs cannot go stale — they are the source, and all derived artifacts are regenerated. Agents read fresh projections.                                   |
| H — Progressive disclosure  | ✓     | (unchanged)                                                                                                                                             |

Under LLM projection, DDD rises from 3/8 aligned properties to
6–7/8 — the highest of any single paradigm. This categorical shift
is explored in `goal-llm-projection-model.md`.

**Takeaway:** The discipline of articulating intent before
coding. Under the projection model, DDD is effectively Spec-Decay's
ancestor — the same lifecycle, minus the engine that makes it
practical.

---

### 8. Design by Contract (DbC)

Functions declare preconditions, postconditions, and invariants.
Violations are runtime errors. Contracts are part of the code, not
external documents.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                  |
| --------------------------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ✓     | Contracts are co-located, machine-readable, and enforceable. An agent reading a function signature with contracts knows exactly what it can assume and must guarantee. |
| B — Spec-first              | ◐     | Contracts are a form of inline spec. But they specify function-level behavior, not feature-level intent.                                                               |
| C — Continuous verification | ✓     | Contracts are checked at runtime (and statically in some languages). Violation → immediate failure.                                                                    |
| D — Small increments        | ◐     | DbC is per-function. Compatible with any increment size.                                                                                                               |
| E — Tooling-as-law          | ✓     | The type system / runtime enforces contracts. No human review needed.                                                                                                  |
| F — Transparent             | ✓     | Contracts are the most explicit form of behavioral documentation.                                                                                                      |
| G — Multi-agent             | ✓     | Contracts are the ideal agent interface — machine-readable expectations at every call site.                                                                            |
| H — Progressive disclosure  | ✓     | Add contracts to one function at a time.                                                                                                                               |

**Takeaway:** Behavioral expectations should be co-located and
machine-enforceable. In TypeScript, this manifests as strict types +
branded types + runtime validation at boundaries. Combined with tests,
contracts at module boundaries replace the need for behavioral prose.

---

### 9. Continuous Delivery / Deployment (CD)

Every commit is deployable. Automated pipeline from commit to
production. Feature flags, canary releases, blue-green deployments.

**Alignment:**

| Property                    | Score | Notes                                                                                                                                               |
| --------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ◐     | CD pipelines encode deployment knowledge that would otherwise live in prose ("to deploy, run X then Y"). But CD is infrastructure, not code design. |
| B — Spec-first              | ✗     | CD is delivery-focused, not design-focused.                                                                                                         |
| C — Continuous verification | ✓     | The pipeline *is* continuous verification — builds, tests, lints, deploys, all automated.                                                           |
| D — Small increments        | ✓     | CD requires small, safe changes. Large changes break the pipeline.                                                                                  |
| E — Tooling-as-law          | ✓     | The pipeline is the ultimate enforcer. Broken build = blocked merge.                                                                                |
| F — Transparent             | ◐     | Pipeline definitions are version-controlled. But they're infrastructure, not intent.                                                                |
| G — Multi-agent             | ✓     | Multiple agents can commit independently; the pipeline validates everything.                                                                        |
| H — Progressive disclosure  | ◐     | Requires infrastructure investment upfront. But once in place, adoption is per-repo.                                                                |

**Takeaway:** CI gates as convention enforcement. The pipeline
as the arbiter of "does this change meet the bar." An automated
agent-nativeness gate in CI is the natural extension.

---

### 10. Literate Programming

Code and documentation are woven together in a single artifact.
The source is a document that generates both human-readable
explanation and executable code (e.g. Knuth's WEB, Jupyter notebooks).

**Alignment:**

| Property                    | Score | Notes                                                                                                                                                                                   |
| --------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A — Agent-native            | ✗     | Maximizes prose co-located with code. For humans, this aids understanding. For agents, it's noise — agents read types and tests, not paragraphs explaining what the next function does. |
| B — Spec-first              | ◐     | The narrative *is* the spec. But it's entangled with the implementation, making the spec non-separable.                                                                                 |
| C — Continuous verification | ✗     | Prose portions are unverifiable. Code portions run, but the toolchain (tangle/weave) adds friction.                                                                                     |
| D — Small increments        | ✗     | Literate documents tend toward monolithic narratives.                                                                                                                                   |
| E — Tooling-as-law          | ✗     | The paradigm privileges human-readable narrative over automated enforcement.                                                                                                            |
| F — Transparent             | ✓     | Maximally transparent — every decision is explained inline.                                                                                                                             |
| G — Multi-agent             | ✗     | Agents must parse through interleaved prose and code. Worse signal-to-noise than either pure code or pure docs.                                                                         |
| H — Progressive disclosure  | ✗     | Requires committing to the literate toolchain for the entire module.                                                                                                                    |

**Takeaway:** Almost nothing. Literate programming is the
philosophical opposite of agent-native design. It optimizes for a
*human reader following a narrative*; agent-native design optimizes for
a *machine reader following types and tests*. The one kernel of truth: intent
should be co-located with code — but as types and test names, not
paragraphs.

---

## Alignment Summary

| Paradigm                | A   | B   | C   | D   | E   | F   | G   | H   | Aligned Properties |
| ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------ |
| Waterfall               | ✗   | ◐   | ✗   | ✗   | ✗   | ◐   | ✗   | ✗   | 0                  |
| Agile                   | ✗   | ◐   | ◐   | ✓   | ✗   | ◐   | ✗   | ◐   | 1                  |
| TDD                     | ◐   | ✓   | ✓   | ✓   | ◐   | ✓   | ◐   | ◐   | 4                  |
| BDD                     | ◐   | ✓   | ✓   | ✓   | ◐   | ✓   | ◐   | ✗   | 4                  |
| Trunk-Based Development | ◐   | ✗   | ✓   | ✓   | ◐   | ◐   | ✓   | ✓   | 4                  |
| Domain-Driven Design    | ✓   | ◐   | ✗   | ◐   | ◐   | ◐   | ✓   | ◐   | 2                  |
| Documentation-Driven †  | ✗   | ✓   | ✗   | ◐   | ✗   | ✓   | ✗   | ✓   | 3                  |
| Design by Contract      | ✓   | ◐   | ✓   | ◐   | ✓   | ✓   | ✓   | ✓   | 6                  |
| Continuous Delivery     | ◐   | ✗   | ✓   | ✓   | ✓   | ◐   | ✓   | ◐   | 4                  |
| Literate Programming    | ✗   | ◐   | ✗   | ✗   | ✗   | ✓   | ✗   | ✗   | 1                  |

† Documentation-Driven scored at 3/8 under classical (human-maintained)
assumptions. Under LLM projection, it rises to 6–7/8 — the highest
of any paradigm. See the DDD section above and
`goal-llm-projection-model.md` for the re-evaluation.

No single paradigm satisfies all eight properties under classical
assumptions. The highest-scoring (Design by Contract) covers the
*what* of individual functions but not the *flow* of development.
TDD covers the *verification* loop but not the *structure*. DDD
covers *structure* but not *verification*. Documentation-Driven
Development, when paired with LLM projection, covers the most
properties — but requires an LLM projection engine to be practical.


