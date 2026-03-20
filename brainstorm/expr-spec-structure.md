# Spec Structure: Approaches and Analysis

Evaluation of approaches for representing project *specs* — living design documents that describe what a system currently is, why, and what constraints govern it.

Guided by `index.md` (architecture principles, goals), `pitfalls.md` (known AI agent failure modes), and `case-study-bfc.md` (empirical observations from a project using the previous worklog system). Each approach is simulated against the [bfc](https://github.com/123jimin/bfc) repository (11 specs, ~40 source files, TypeScript compiler with cross-cutting optimization pipeline).

## General Criteria

Any spec representation for this plugin must satisfy the goals and avoid the pitfalls established in the brainstorm:

- **Domain- and language-agnostic.** The plugin targets arbitrary projects across arbitrary domains. Domain-specific or language-specific solutions fail the meta-goal.
- **Spec-first capable.** Specs describe *design intent*, which exists before code. Approaches that require code to exist before the spec can be written prevent iterative design-then-implement workflows.
- **Cross-cutting specs must stay intact.** Real systems have concerns that span multiple components. A spec that describes a unified strategy (like an optimization pipeline) across 5+ directories must remain a single coherent document.
- **Cross-referencing.** The bfc case study calls cross-references the "most structurally valuable feature" of the worklog system. Navigating from spec → related specs, and from tasks → specs they modify, is essential.
- **Mutable living reference.** The bfc case study observes that specs work best as "what the design currently is," not frozen requirements. Approaches must support in-place updates.
- **Minimal sync burden.** `pitfalls.md` warns: "stale docs are worse than no docs." It follows that manual maintenance obligations (markers, anchors, dual updates) that aren't enforced by tooling are likely to be skipped — this is consistent with the case study's finding that validation scripts "require deliberate invocation — frequently skipped."
- **Resilient to agent failure modes.** `pitfalls.md` (citing context-file effectiveness research) warns that agents explore "document-directed instead of task-directed when context files are present, burning tokens on orthogonal concerns." A spec system is not identical to a context file, but the risk of agents over-exploring spec graphs instead of doing the task should be considered.
- **Simplicity.** `index.md` requires architecture to be "simple," to feel "natural and easy." This applies to the spec system itself: the overhead of maintaining specs (frontmatter schemas, relationship taxonomies, directory hierarchies) must be weighed against the value they provide.
- **Hierarchy confusion.** `pitfalls.md` warns: "When code, tests, and documentation conflict, agents have no consistent rule for which source of truth wins." Any spec system creates a layer that can diverge from code. The approach must consider how spec-code conflicts are detected and resolved.
- **Over-specification resistance.** `pitfalls.md` warns: "Agents define API signatures and field names, not observable behavior. Over-specified specs require re-sync on every minor implementation change." The spec format should discourage over-specification (describing implementation details rather than observable behavior and design intent).
- **Lifecycle enforcement.** `pitfalls.md` warns: "Agents modify specs inline while working, bypassing the task lifecycle." Having lifecycle metadata (status fields, timestamps) is not sufficient if agents routinely bypass the intended lifecycle. The approach should consider how lifecycle discipline can be enforced, not just tracked.

## Test Cases for Simulation

Each approach is simulated against bfc. Two specs serve as discriminating test cases:

**s0010 (optimization):** A single spec covering a unified strategy that spans 5+ source directories across 2 layers (BF dead loops, BSM trivial optimizations, pattern matchers, optimizer passes, value tracking). Its value is the cross-cutting unified view — any approach that fragments it destroys this.

**s0003 (BSM core language):** A *language* spec with no single source file anchor. It defines what the language *is*, not how it's parsed. Tests whether approaches can represent conceptual artifacts independent of source files.

The full mapping of bfc's 11 specs to source:

| Spec | Describes | Source locations | Mapping type |
|---|---|---|---|
| s0001 (overview) | Public API surface | barrel files, CLI | scattered |
| s0002 (bf layer) | BF language + API | `src/bf/**` | 1:1 directory |
| s0003 (bsm core) | BSM core *language* | parser, ast | conceptual (no anchor) |
| s0004 (grammar) | BSM grammar rules | `src/bsm/parser/lexer/` | 1:1 directory |
| s0005 (ast) | AST structure | `src/bsm/ast/**` | 1:1 directory |
| s0006 (frames) | Frame extension | `ast/frame.ts`, `resolve/` | multi-directory |
| s0007 (macros) | Macro system | `ast/macro.ts`, `resolve/macros.ts` | multi-directory |
| s0008 (vscode) | Editor extension | `editors/vscode/` | 1:1 directory |
| s0009 (target cond.) | Conditional compilation | scattered | scattered |
| s0010 (optimization) | All optimization passes | `optimize/`, `patterns/`, `bf/optimizer.ts`, `translate/` | cross-cutting (5+ dirs) |
| s0011 (stl) | Standard macro library | `bsm-stl/`, `src/bsm/stl/` | multi-directory |

Of 11 specs: 4 map 1:1 to a directory, 3 span multiple directories, 2 are scattered, 1 is cross-cutting across 5+ directories, 1 is conceptual with no source anchor.

## Rejected Approaches

**In-source docgen (tsdoc, pydoc, rustdoc):** Specs live as structured comments in source files; a tool extracts them into browsable documentation. Language-locked (violates the language-agnosticism meta-goal). Cannot represent cross-cutting specs (s0010 would fragment across 5+ files). Cannot represent language specs (s0003 has no source anchor). Cannot support spec-first workflow (spec's container doesn't exist before the code). Conflates audiences (API reference for consumers ≠ design spec for maintainers). Only ~25% of bfc's spec content fits this model. Appropriate for API reference documentation, not for design specs.

**Schema-driven (OpenAPI, JSON Schema, EBNF):** Only ~25% of bfc's spec content is schema-expressible (type shapes, grammar rules). The most valuable parts — optimization strategy, pointer tracking semantics, design principles like "prefer Add over Set" — are fundamentally algorithmic prose. A formal grammar for s0004 and type schemas for s0005 could be useful *inputs* to a spec system, but cannot serve as the system itself.

**Executable specs (Gherkin / BDD):** Duplicates existing test suites with additional ceremony (step definitions, glue code). Critical spec content (design principles, pipeline ordering, architectural constraints) is untestable. `pitfalls.md` warns that agents treat test-writing as a goal to *pass*, not a tool to *find failures* — executable specs amplify this by making the spec itself an optimization target. Covers behavioral aspects only; architectural/design specs are unrepresentable.

**Boundary SPEC.md (SPEC.md at architectural boundary directories only):** Same fragmentation problem as per-directory README for cross-cutting specs. s0003 fits awkwardly — "BSM the language" is not "the `bsm/` directory." Merging multiple conceptual specs into one file (s0003+s0004+s0005 into `bsm/SPEC.md`) loses granularity; separating them into sub-directory SPECs loses overview. Offers locality over approach 3 but the bfc case study did not identify source-proximity as a major pain point.

## Complementary-Only Approaches

These solve real problems but cannot stand alone as a spec system.

### ADR (Architecture Decision Records)

Each document captures a single decision: context, options considered, decision taken, consequences. Immutable by convention (supersede, don't edit). Lightweight individual files with a simple template. Can coexist with any spec system — they cover the "why" that specs (the "what") often omit.

However, ADRs accumulate without synthesis: after 50 decisions, understanding the system requires reading many documents and mentally reconstructing the current state. Status tracking is minimal (accepted/superseded/deprecated — no notion of partial implementation).

Solves the gap the bfc case study identified: *"Design rationale gets buried in archives. The spec captures what was built, not why those alternatives were rejected. There's no permanent home for decision rationale."* For example, "why no recursion in macros?" would be a permanent ADR rather than an archived plan that nobody reads.

Cannot serve as specs because ADRs record decisions (*why*), not current state (*what*). An agent cannot answer "what is the current optimization pipeline?" from ADRs — it would need to reconstruct the answer from the chain of decisions. The bfc case study observes that specs work best as "what the design currently is," not frozen requirements. ADRs are the opposite: immutable historical records.

**Role:** Companion to a spec system, housing decision rationale that specs omit.

### Hybrid In-Source Anchors + Centralized Specs

Source files contain minimal markers (e.g., `// @worklog s0010`) linking to centralized spec documents. Solves the discoverability gap: an agent in `src/bsm/optimize/value-tracking.ts` immediately sees which spec to read.

**Empirically failed in bfc.** The worklog v1 design defined `@worklog` markers. In practice, 1 of ~40 source files adopted one (`value-tracking.ts:1`). Reasons:

- **Manual maintenance.** No tooling enforces marker presence or staleness.
- **Many-to-many mapping.** `compiler.ts` relates to s0003, s0006, s0007, and s0010 — the marker line becomes a metadata blob that itself drifts.
- **Friction-to-value ratio.** The marker is useful only when you're *in the file and need the spec*. The cost of maintaining markers in ~40 files for an occasional benefit wasn't justified.

Could be viable if *fully automated* — a script infers spec relationships from directory structure, tags, and content, then generates markers or provides a `which-spec <file>` query. But at that point, the query tool achieves the same result without source modification.

**Role:** Discoverability layer on top of a centralized spec system. Only viable if automated, not manually maintained.

## Viable Standalone Approaches

### Per-Directory README.md

Each source directory gets a `README.md` describing responsibilities, invariants, and interface.

**General strengths:** Locality (spec lives next to code; diffs show both together). Language-agnostic (Markdown is universal). Low ceremony (no tooling, no frontmatter, no schema). Natural granularity mapping to the "building block" concept. High discoverability (GitHub renders READMEs; any developer browsing the repo sees them).

**General weaknesses:** Flat within each directory — cross-cutting concerns (e.g., a compilation pipeline spanning `parser/` → `resolve/` → `translate/`) have no natural home. No metadata or cross-references without ad-hoc conventions. No lifecycle tracking (can't distinguish current design from aspirational). Sync drift has no enforcement mechanism. Granularity is fixed to directory boundaries — sometimes a spec covers a single file's algorithm, sometimes a subsystem spanning multiple directories.

**Simulation — what works:**
- `src/bf/README.md` ← s0002 (BF layer) is a clean 1:1 fit.
- `bsm-stl/README.md` ← s0011 (STL reference) is a clean fit.
- `editors/vscode/README.md` ← s0008 is a clean fit.
- GitHub renders READMEs automatically; PRs show spec + code changes in the same diff.

**Simulation — where it breaks:**
- **s0010 (optimization)** fragments into `optimize/README.md`, `patterns/README.md`, `translate/README.md`, plus `src/bf/README.md`. The unified optimization strategy — pipeline order, shared assumptions, design principles — has no single home. An agent in `optimize/` must somehow know to also read `patterns/README.md` and `translate/README.md`. Nothing in the file tree signals this.
- **s0006 (frames)** spans `ast/frame.ts` (type definitions) and `resolve/` (resolution semantics). The coherent spec splits across two directories, severing the connection between syntax and semantics.
- **s0003 (BSM core language)** would go in `parser/README.md` or `bsm/README.md`, but it describes the *language*, not the *parser implementation*. Placement implies a scope that doesn't match content.
- **No cross-references.** Related READMEs are siloed with no structured links. The bfc case study identifies cross-references as the most structurally valuable feature of the worklog system — READMEs can't provide this.
- **No lifecycle metadata.** Cannot distinguish current design from aspirational. Cannot track which tasks modify which specs.

**Assessment:** Works for specs that map 1:1 to a directory (~4 of bfc's 11). Fails for cross-cutting specs and specs that describe concepts rather than code. Low ceremony but also low capability.

### Flat List in Separate Directory (bfc Status Quo)

All specs in a single directory (e.g., `worklog/spec/`) as numbered files with TOML frontmatter.

**General strengths:** Language-agnostic and tool-agnostic (pure Markdown + TOML). Cross-references via frontmatter IDs (`targets`, `modifies`, `implements`). Lifecycle metadata in frontmatter (status, tags, dates). Spec-first is natural (write the spec file before any code exists). Easy to validate (scripts can check frontmatter schema, dangling references).

**General weaknesses:** No structural relationship between specs — related specs are peers in a flat list, discoverable only through frontmatter metadata. Navigation is ID-based, not spatial. Numbering is chronological, not semantic (adjacent IDs don't imply related content). Spatial disconnect from source (the spec directory is far from the code it describes). Scale ceiling when the number of specs grows large. The frontmatter schema itself is a design decision made early: choosing `modifies`/`implements`/`targets` as the relationship taxonomy before usage patterns stabilize carries the same premature-decision risk that `index.md` warns about. The ceremony of maintaining IDs, tags, and typed cross-references in TOML frontmatter echoes the "three-tier ceremony" pitfall — classification overhead that `pitfalls.md` warns agents bypass when boundaries are unclear.

**Simulation — what works:**
- **s0010 stays intact.** Agent reads one file, gets the full optimization strategy: pipeline order, design principles, pass descriptions, shared assumptions. This is the approach's killer advantage.
- **s0003 works naturally.** A language spec doesn't need a source file anchor; it exists as `s0003-bsm-core.md` on its own terms.
- **Cross-references via frontmatter** (`tags`, `modifies`, `targets`, `implements`) create a navigable graph — the case study identifies this as the most structurally valuable feature of the worklog system.
- **Spec-first workflow** is natural: write `s0012-new-thing.md` before any code exists.
- **TOML frontmatter** enables schema validation, relationship checking, and tooling.

**Simulation — where it's weak:**
- **Discoverability from source is poor.** An agent working in `src/bsm/resolve/` has no breadcrumb pointing to `s0006`. It must know (or discover) the `worklog/spec/` directory and scan filenames.
- **Numbering is chronological, not semantic.** `s0008` (vscode) sits between `s0007` (macros) and `s0009` (target conditional) — adjacent numbers, zero conceptual relationship. At 11 files this is fine; at 40+ it's a wall of opaque IDs.
- **No grouping.** All 11 files are peers. The `tags` field partially compensates, but tags are metadata you must *open files to read*, not something visible from `ls`.

**Assessment:** Proven to work for bfc's actual usage. Covers 100% of spec types. Main weaknesses are discoverability and scalability — neither of which has caused real pain at bfc's current size (11 specs), but both are foreseeable growth problems.

### Hierarchical Separate Directory

Like the flat list, but specs are organized in subdirectories reflecting the conceptual architecture.

**General strengths:** All strengths of the flat list (language-agnostic, cross-refs, lifecycle, spec-first). Spatial discoverability — the directory tree *is* the architecture map. Implicit grouping of related specs. Scales better than flat (subdirectories prevent overwhelming listings). Structure communicates design intent.

**General weaknesses:** The hierarchy itself is a design decision — choosing and maintaining it creates churn when the architecture evolves. Cross-cutting concerns remain homeless (a spec spanning multiple groups must be placed *somewhere*, and any choice is partially wrong). The spec hierarchy and source hierarchy may intentionally differ (`index.md` says architecture should be "largely independent (but still non-ignorable) from execution environment and programming language"), creating a mapping problem. Deeper nesting means longer paths. Over-structuring risk when the number of specs doesn't justify hierarchy.

```
spec/
  overview.md               ← s0001
  bf/
    layer.md                ← s0002
  bsm/
    core-language.md        ← s0003
    grammar.md              ← s0004
    ast.md                  ← s0005
    frames.md               ← s0006
    macros.md               ← s0007
    optimization.md         ← s0010
    target-conditional.md   ← s0009
  stl/
    reference.md            ← s0011
  editor/
    vscode.md               ← s0008
```

**Simulation — what it improves over flat:**
- **Spatial grouping aids discovery.** `ls spec/bsm/` pre-filters to the 7 BSM-related specs. An agent working on BSM code checks `spec/bsm/` — the directory structure itself is an architecture map.
- **Naming becomes semantic.** `spec/bsm/frames.md` is self-describing; `s0006-bsm-frames.md` requires decoding the ID convention.

**Simulation — where the hierarchy creates friction:**
- **s0010 placement dilemma.** The optimization spec covers both BF-layer dead loops and BSM-layer optimizer passes. Placing it under `spec/bsm/` means an agent working on `src/bf/optimizer.ts` might check `spec/bf/` and miss the BF optimization content. Any placement is somewhat wrong; the spec is inherently cross-cutting.
- **Hierarchy is a premature design decision.** You must choose the grouping before the design stabilizes. `index.md` warns that premature design decisions are costly and that "one also discovers true requirements through the act of implementation itself." If the conceptual architecture shifts (say, BSM splits into "compilation" and "runtime"), the spec tree needs reorganization — churning paths and cross-references.
- **Hierarchy ≠ source tree.** `index.md` says architecture should be "largely independent (but still non-ignorable) from execution environment and programming language," so the spec hierarchy *should* differ from the source tree. But then agents can't naively map `src/bsm/resolve/` → `spec/bsm/resolve/`. The mapping requires knowledge of the conceptual architecture.
- **Premature at small scale.** At 11 specs, the hierarchy has directories with 1-2 files (`spec/bf/` has one file, `spec/stl/` has one file, `spec/editor/` has one file). The structure adds depth without adding information.

**Assessment:** Strictly better than flat at scale (30+ specs). At bfc's current scale (11 specs), the hierarchy is justifiable (7/11 are BSM-related) but barely necessary. The cross-cutting placement problem is real but manageable — it exists in any organizational scheme that uses spatial grouping.

### Wiki-Style with Bidirectional Links

Specs as interconnected documents with `[[wikilinks]]` enabling bidirectional navigation.

**General strengths:** Cross-references are first-class — `[[wikilinks]]` automatically create backlinks. Flexible structure (notes can be flat, hierarchical, or graph-structured — the link topology *is* the structure). Emergent organization via tags + links allows multiple overlapping categorizations without rigid hierarchy. Tooling exists for humans (Obsidian, Foam, Dendron).

**General weaknesses:** Tooling dependency — plain Markdown readers (GitHub, `cat`) don't resolve `[[wikilinks]]`. Hard to validate programmatically (backlink resolution requires a wiki engine or custom parser). Graph tends to tangle without discipline (everything links to everything, structure conveys noise). Non-standard for AI agents, which don't natively understand wiki-link conventions.

**Simulation — what the linking model adds:**

Inline links are more natural than frontmatter references — you link *where the reference makes sense in the prose*, not in a detached metadata block. Backlinks automatically surface relationships: `[[optimization]]` referenced from `[[pattern-matchers]]` means the pattern-matchers page shows optimization as a consumer without anyone manually maintaining a reverse reference.

**Simulation — where it breaks for AI agents:**

- **Tooling dependency.** GitHub doesn't render `[[wikilinks]]`. AI agents don't natively resolve them. The spec files are less useful without a wiki engine — degrading to plain-text, they're just approach 3 with non-standard link syntax.
- **No typed relationships.** `[[optimization]]` references `[[pattern-matchers]]` — but *how*? As a dependency? A consumer? A superseder? TOML frontmatter's `modifies`, `implements`, `targets` carry semantics; wikilinks are untyped edges in a graph.
- **Tangling risk.** Without discipline, everything links to everything and the graph conveys noise, not signal. `pitfalls.md` warns agents explore "document-directed instead of task-directed when context files are present" — a wiki graph with many bidirectional links may amplify this tendency.
- **Validation is harder.** Checking for dangling `[[links]]` requires a custom parser, unlike TOML frontmatter which has standard parsers in every language.

**Assessment:** The linking model is the most natural for humans navigating specs. For AI agents working with plain-text files in a Git repo, structured TOML frontmatter provides the same semantic connections with better machine parseability and no tooling dependency. The approach's main advantage (bidirectional backlinks) only materializes with tooling that doesn't exist in the target workflow.

## Summary

Approaches that tie specs to the source tree (in-source docgen, per-directory README, boundary SPEC.md) share a fatal weakness: **cross-cutting specs fragment.** The source tree reflects implementation structure; specs reflect conceptual architecture. These are different organizations, and forcing one into the other creates friction wherever the two structures diverge. The bfc optimization spec (s0010) is the clearest example — it describes a unified strategy spanning 5+ directories, and any attempt to split it along directory boundaries destroys its value.

Approaches that give specs their own namespace (flat list, hierarchical, wiki-style) all handle cross-cutting specs well. Among these:

- **Flat list** is proven, simple, and sufficient at small scale. Its weaknesses (discoverability and scalability) are manageable with frontmatter tags at bfc's current size (11 specs) and haven't caused real pain yet.
- **Hierarchical** improves discoverability and grouping at the cost of requiring a hierarchy design and creating a cross-cutting placement dilemma. The benefit scales with project size.
- **Wiki-style** offers the richest linking model but depends on tooling that doesn't exist in the target (AI agent + plain Git) workflow.

**ADRs** and **automated in-source anchors** are viable as layers on top of any of these, solving the "decision rationale" and "source→spec navigation" gaps respectively. Neither replaces a spec system.

### Open problems across all approaches

Several pitfalls from `pitfalls.md` are *not solved by structural choice alone* — they apply equally to every viable approach:

- **Hierarchy confusion.** When spec and code disagree, agents have no consistent rule for which wins. No structural approach defines a conflict resolution protocol. This must be addressed by plugin-level policy (e.g., "code is ground truth; a spec that contradicts code is stale and must be updated").
- **Over-specification.** Agents define API signatures and field names rather than observable behavior. Freeform Markdown specs (all viable approaches) leave granularity entirely to the agent. The spec format itself cannot prevent over-specification; guidance on *what* to write in a spec is orthogonal to *where* specs live.
- **Lifecycle bypass.** Agents modify specs inline while working, bypassing intended workflows. Having lifecycle metadata in frontmatter (flat list, hierarchical) does not prevent this. Enforcement requires tooling (hooks, validation scripts) regardless of structural approach — and the case study warns that validation scripts are "frequently skipped" unless automated.
- **Three-tier ceremony.** The spec/plan/task classification from worklog v1 eroded in practice. Any approach that reintroduces typed relationships (`modifies`, `implements`, `targets`) or multi-tier document categories risks the same erosion. The ceremony must be justified by demonstrated value, not assumed to be helpful.
