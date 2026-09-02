+++
id = "n0005"
title = "SKILL.md content inventory"
+++

# `SKILL.md` content inventory

This note is a non-authoritative t0009 traceability inventory proposed for governance by s0004.
While the s0004 proposal remains `NEEDS APPROVAL`, this inventory is work product rather than current methodology.
The approved specs remain authoritative if an allocation or summary here is wrong.

## Reading the inventory

`Need` states when the information must be available and whether it is global or operation-specific.
`Omission` combines consequence severity with observed frequency in the reviewed evidence.
`Tool*` and `Agent*` are conditional allocations whose delivery guarantees are not yet established by s0005 or s0007.
Until the guarantee exists, the delivered `SKILL.md` needs a direct-operation fallback.
Rows sourced from the proposed s0004 content describe proposed allocation mechanics, not approved behavior.

## Current allocation

| ID | Source and independent information unit | Decision or action affected | Need | Omission | Primary location | Allocation rationale or required guarantee |
| --- | --- | --- | --- | --- | --- | --- |
| i001 | s0001, n0002, n0003: Worklog adoption is the project's choice. | Whether to initialize or govern work through worklog. | Before selection; global. | High; repeatedly observed. | `SKILL.md` | The agent must decide this before invoking `init`; a tool warning arrives too late if invocation itself assumes adoption. |
| i002 | s0001, s0002: Worklog is durable project intent and state shared across sessions. | Where to orient, resume, and preserve current truth. | On activation; global. | High; repeatedly observed. | `SKILL.md` | This is the minimum mental model for every operation. |
| i003 | s0001, s0002: Specs, tasks, notes, and references have different authority and lifecycle roles. | Which entity receives information or work. | Before entity selection; global. | High; repeatedly observed. | `SKILL.md` | Misrouting can strand authoritative state in history or make guidance look binding. |
| i004 | s0001, n0003: Partial adoption or coexistence with another authoritative process can create parallel truth. | Whether adoption is complete and which record governs. | Before initialization or use; global. | High; observed in multiple projects. | `SKILL.md` | No operation-specific provider can repair an already-created competing ledger. |
| i005 | s0001: Plugin users cannot read this repository's specs or notes. | How self-contained the delivered plugin must be. | During skill composition; internal. | Critical; runtime omission cannot be observed because repository access is absent by design. | Governing spec | s0004 owns the resulting composition constraint; the runtime agent does not need repository-access rationale. |
| i006 | s0001: The plugin is harness-agnostic. | Whether instructions depend on one host's hooks or prompt placement. | During implementation; internal. | High; incompatibility was observed in v0.1 hooks. | Governing spec | This constrains implementation, not ordinary worklog decisions. |
| i007 | s0002, n0003, v0.1: Durable task state outranks temporary session plans and prior conversational memory. | How to resume and where to track reviewable work. | Before planning; global. | High; repeatedly observed. | `SKILL.md` | The rule prevents an external plan from silently replacing current worklog state. |
| i008 | s0002, s0009: Entity identity is type plus numeric value; references use IDs rather than unstable paths. | How to cite, rename, and relocate entities. | During every entity operation; global. | Medium; observed. | `SKILL.md` | The convention is small and needed even when no tool is used. |
| i009 | s0002: Storage directories, TOML fences, standard filenames, ID normalization, and uniqueness. | Creating or validating files. | During create or validate; operation-specific. | Medium; omission frequency is unmeasured across routine operations. | `Tool*` | Create and validate tools must allocate IDs, prefill structure, and reject collisions before writing. |
| i010 | s0002: Common frontmatter fields and their type availability. | Creating or editing an entity. | During create or edit; operation-specific. | Medium; omission frequency is unmeasured across routine operations. | `Tool*` | The provider must expose only fields valid for the selected entity type. |
| i011 | s0002: `parent` is organizational only and implies no authority, inheritance, dependency, order, status, or lifecycle. | Interpreting hierarchy and actionability. | Before planning from hierarchy; global. | High; anticipated silent error. | `SKILL.md` | A compact negative rule prevents several consequential inferences before tools are called. |
| i012 | s0002, s0005: Parent availability, references, cycles, reverse lookup, archive inclusion, and grouping. | Creating, changing, or displaying hierarchy. | During hierarchy operations; operation-specific. | Medium; omission frequency is unmeasured because hierarchy is not yet implemented. | `Tool*` | Hierarchy tools must validate these mechanically and derive children rather than duplicate state. |
| i013 | s0002: Worklog files should remain self-descriptive without plugin access. | Generating project configuration and entity files. | At file generation; operation-specific. | High; recurring cold-reader risk. | `Tool*` | Generated files must carry concise in-band comments for non-obvious fields and authority. |
| i014 | s0002: Keep one subject per entity, extend existing entities, record current state, and avoid repeated context. | Authoring or restructuring entities. | During authoring; cross-entity operation. | Medium; repeatedly observed. | `Agent*` | Authoring and review agents must apply these checks to the complete affected entity set. |
| i015 | s0002: `NEEDS APPROVAL` marks unauthoritative content; `UNIMPLEMENTED` marks authorized behavior not yet delivered. | Interpreting authority and implementation state. | Before specification or implementation; global. | Critical/high; repeatedly observed. | `SKILL.md` | Confusing the markers changes both authority and delivery decisions. |
| i016 | s0002: Heading-marker scope, partial-section marking, and marker redistribution. | Adding, moving, or narrowing markers. | During spec editing; operation-specific. | High; observed. | `Tool*` | Editing tools must show affected scope and preserve markers on every still-affected child. |
| i017 | s0002, s0009, v0.1: Remove a marker only when its condition is verified; implementation claims alone are insufficient. | Declaring implementation or approval state current. | Before marker removal and closure; global. | High; repeatedly observed and exam-sensitive. | `SKILL.md` | Verification must remain salient even when a user or prior agent says work shipped. |
| i018 | s0002: Suggested marker ownership by task ID. | Making an implementation gap actionable. | During marker creation; operation-specific. | Low; omission has not been observed. | `Tool*` | A create/update tool can prefill an owner when one exists without burdening the entrypoint. |
| i019 | s0002, s0012: Apply effective agent mode before changing specs, tasks, or notes and never claim approval. | Whether an edit may be made and whether its content is authoritative. | Before any entity edit; global. | Critical; repeatedly observed. | `SKILL.md` | This decision precedes every editing provider. |
| i020 | s0012: Entity override, project policy, then default determines effective mode. | Resolving edit policy. | Before any entity edit; global. | Critical; omission frequency is unmeasured across routine edits. | `SKILL.md` | The selection order is compact and cannot safely be deferred past editing. |
| i021 | s0012: `read_only`, `propose`, `draft`, and `autonomous` independently control permission and resulting authority. | Whether to ask, edit, mark, or treat content as binding. | Before any entity edit; global. | Critical; repeatedly observed. | `SKILL.md` | A concise mode table prevents authority from being inferred from edit capability. |
| i022 | s0012: Content approval and edit permission are independent and scoped; discussion is not approval. | Interpreting user instructions. | Before changing behavior; global. | Critical; repeatedly observed. | `SKILL.md` | This prevents both unauthorized authority and unnecessary re-asking about stated content. |
| i023 | s0012: Executing a task approves its stated requirements and permits necessary edits only to its then-listed `modifies` specs, subject to mode. | Determining task-work authority. | Before task implementation; global. | Critical; observed. | `SKILL.md` | The execution grant is easy to overgeneralize and affects the entire workflow. |
| i024 | s0012: Unapproved behavior must not be implemented; required `read_only` changes block the task. | Whether implementation may proceed. | Before implementation; global. | Critical; observed and anticipated. | `SKILL.md` | A tool cannot reliably detect all behavioral implications before source changes begin. |
| i025 | s0012: Verified implementation-marker updates do not need content approval, but target edit mode still applies. | Removing or moving `UNIMPLEMENTED`. | Before marker edits; global. | High; omission frequency is unmeasured across routine marker edits. | `SKILL.md` | This narrow exception prevents both over-asking and unauthorized edits. |
| i026 | s0012: Tasks cannot close while required spec content awaits approval. | Completion and archival. | At closure; global. | Critical; anticipated. | `SKILL.md` | This is a terminal integrity condition. |
| i027 | s0012: Recommended in-band mode comments. | Generating `project.toml` or self-descriptive entity state. | At generation; operation-specific. | Medium; omission frequency is unmeasured across routine generation. | `Tool*` | `init` and edit tools must use wording that preserves both permission and authority. |
| i028 | s0003: A spec is authoritative current project behavior and outranks code and tests. | Resolving divergence. | Before reading implementation as truth; global. | Critical; observed and anticipated. | `SKILL.md` | This precedence must remain active throughout implementation and review. |
| i029 | s0003: If a spec seems wrong, resolve it under agent mode rather than silently overriding it. | Handling evidence that conflicts with intent. | At divergence; global. | Critical; observed. | `SKILL.md` | The rule prevents implementation from laundering a behavioral change. |
| i030 | s0003: Create or extend a spec for behavior expected to outlast the task. | Whether durable behavior needs specification. | Before implementation; global. | High; repeatedly observed. | `SKILL.md` | This is the governance gate that distinguishes behavior work from an ungoverned chore. |
| i031 | s0003, s0012: Include only authorized behavior and direct entailments; mark other permitted drafts. | Writing behavioral content. | Before and during spec authoring; global. | Critical; repeatedly observed and resistant to prose alone. | `SKILL.md` | The authority boundary must be known before any authoring provider is selected. |
| i032 | s0003: Check related behavior and overlapping specs before changing a spec; specs must not contradict. | Selecting the governing spec set and reviewing a change. | Before spec edit; global. | High; repeatedly observed. | `SKILL.md` | This search decision precedes the detailed writing procedure. |
| i033 | s0003: State observable behavior, constraints, known failures, and necessary changeability without implementation-independent detail or history. | Drafting spec contents. | During spec authoring; operation-specific. | High/medium; repeatedly observed. | `Agent*` | A spec author/reviewer must separate current behavior from design narration and inspect the implementation boundary. |
| i034 | s0002, s0003: Express principles, hard/soft constraints, permissions, and requirement strength explicitly. | Choosing authoritative wording. | During spec authoring; operation-specific. | Medium; repeatedly observed. | `Agent*` | The provider must classify each retained statement rather than apply a fixed heading template. |
| i035 | s0003: Body organization, known-failure sections, and constrained changeability are conditional on actual content. | Structuring a spec. | During spec authoring; operation-specific. | Medium; over-structuring was repeatedly observed. | `Agent*` | The provider must add headings only when they classify needed content and avoid speculative seams. |
| i036 | s0003: `paths` are globs for governed files and must remain precise as behavior boundaries move. | Establishing drift ownership and task governance links. | During spec creation, review, or refactor; operation-specific. | High; repeatedly observed. | `Agent*` | The provider must inspect the actual implementation surface; a static entrypoint cannot supply project paths. |
| i037 | s0003: Update invalidated specs in the same session and remove behavior no longer governed. | Maintaining current authority. | During implementation and closure; global. | Critical; repeatedly observed. | `SKILL.md` | Delaying write-back strands current state in code or task history. |
| i038 | v0.1: Fixed required spec sections. | Whether every spec uses one template. | Never; obsolete. | None from omission; retention repeatedly caused template bloat. | Nowhere | v0.2 explicitly makes organization content-dependent. |
| i039 | v0.1: Structural spec edits bypass approval. | Whether typo, `paths`, or reorganization edits need mode checks. | Never; obsolete. | None from omission; retention would conflict with s0012. | Nowhere | Current agent mode governs all edits except the explicit marker-content approval exception. |
| i040 | v0.1: Git last-commit drift algorithm and its commands. | Detecting code/spec drift. | Never as current behavior. | None from omission; Git-only mismatch was observed outside its valid environment. | Nowhere | s0005 does not yet define this operation, and non-Git projects made the old algorithm invalid. |
| i041 | s0009: A task is one reviewable unit expected to finish in one session. | Whether to create or split work. | Before reviewable work; global. | Medium/high; repeatedly observed. | `SKILL.md` | The boundary prevents invisible work and unreadable multi-session ledgers. |
| i042 | s0009, n0003: Create the task before reviewable work, set `pending`, and set `active` when work starts. | Establishing live task state. | Before substantive work; global. | High/medium; repeatedly observed. | `SKILL.md` | Status maintenance is a process rule vulnerable to execution momentum. |
| i043 | s0009: Status meanings, blocker explanation, and unblock checks. | Updating task lifecycle state. | During status transitions; operation-specific. | Medium; observed. | `Tool*` | A status tool must enforce valid transitions and prompt for the actual blocking condition. |
| i044 | s0009: `modifies` lists every governing spec touched; an empty list is exceptional. | Establishing authority and closure scope. | Before implementation and at scope changes; global. | High; repeatedly observed and exam-resistant. | `SKILL.md` | Incomplete links silently remove spec write-back obligations. |
| i045 | s0009: `blocked_by` contains task dependencies only and must match reality. | Determining actionability and ordering. | During planning and status changes; operation-specific. | Medium; observed. | `Tool*` | Planning/status tools must validate referenced tasks and resolved dependencies. |
| i046 | s0009, s0012: A task is subordinate to specs and grants no authority by its existence, fields, or status. | Interpreting task requirements. | Before implementation; global. | Critical; observed. | `SKILL.md` | The rule prevents task prose from becoming a parallel behavioral authority. |
| i047 | s0003, s0009, n0003: Durable behavior requires a governing spec even when framed as refactoring, cleanup, a parameter tweak, or a chore. | Classifying proposed work. | Before implementation; global. | Critical/high; repeatedly observed. | `SKILL.md` | User framing and execution momentum frequently suppress this check. |
| i048 | s0009: A task is done only when its stated completion conditions are met; stubs, mocks, and placeholders are not completion. | Declaring delivery. | Before `done`; global. | Critical; repeatedly observed and exam-sensitive. | `SKILL.md` | This must remain salient under prior commitment and positive proxy results. |
| i049 | s0009, n0003: Evidence must exercise the claimed delivery boundary, and unavailable verification must not be generalized from a proxy. | Verification and completion claims. | Before reporting or closing; global. | Critical; repeatedly observed across domains. | `SKILL.md` | The invariant applies before choosing a specialist and protects against false completion. |
| i050 | s0009: Before archive, reconcile every `modifies` spec and marker or confirm current wording, then archive promptly. | Closing a task. | At closure; global. | Critical; repeatedly observed and exam-sensitive. | `SKILL.md` | Archived task history cannot substitute for current specs. |
| i051 | s0009: Resolved tasks remain terminal; further work is a new task that references the old one. | Reopening or extending historical work. | After resolution; global. | Medium; observed. | `SKILL.md` | This preserves task history and live-state meaning. |
| i052 | s0009: Task body headings are optional and content-driven. | Formatting a task. | During task authoring; operation-specific. | Low; over-structuring was repeatedly observed, while omission was not. | `Tool*` | A create tool should prefill only necessary state and avoid a verbose mandatory template. |
| i053 | n0002, v0.1: Tests precede implementation and derive from specs. | Ordering implementation verification. | Before implementation; global. | High; repeatedly observed, but not authoritative in current specs. | Governing note | Keep as guidance until an authoritative spec establishes its scope and exceptions. |
| i054 | v0.1: A test agent receives only the spec and cannot inspect governed source. | Isolating behavioral test design. | During test authoring; specialist. | None from omission in current evidence; support exists only in old exams. | Nowhere | Current specs do not establish this strict isolation contract. |
| i055 | n0002: Survey dependencies and existing solutions before building. | Avoiding redundant implementation. | During project start or behavior design; workflow-specific. | Medium; observed. | Governing note | This is general working guidance rather than a worklog authority invariant. |
| i056 | n0002: Bug fixes reproduce the failure, resolve intended behavior, add a failing regression test, correct the general cause, and write back. | Executing a bug fix. | During bug-fix workflow; operation-specific. | High; repeatedly observed. | `Agent*` | A bug-fix/review provider must deliver the procedure and evidence expectations when triggered. |
| i057 | n0002: Investigations and reviews define evidence and stop conditions, preserve uncertainty, obtain disposition, and allow negative results. | Executing epistemic work. | During investigation or review; specialist. | High; omissions were repeatedly observed in a common workflow. | `Agent*` | A specialist must return evidence, uncertainty, findings, and required write-back or follow-up. |
| i058 | n0002: Refactors identify unchanged behavior, establish a baseline, verify preservation, and update boundaries. | Executing a refactor. | During refactor; operation-specific. | Critical/high; repeatedly observed. | `Agent*` | A refactor provider must surface any behavioral change and affected `paths` rather than rely on the label. |
| i059 | n0002, s0009: A completed current-session chore may leave worklog untouched only when no spec changes and no resumable or follow-up state remains. | Whether to omit a task. | Before a small chore; global routing. | High; exception repeatedly abused. | `SKILL.md` | The objective exception prevents excess ceremony while closing the easiest governance bypass. |
| i060 | n0002, s0009: Cancellation, blocked work, and negative findings retain truthful state and create separate follow-up work where needed. | Closing non-successful work. | During non-happy lifecycle; operation-specific. | Medium/high; observed. | `Agent*` | The provider must distinguish a valid negative result from unmet delivery and preserve disposition. |
| i061 | n0002: Starting a project, adopting worklog later, and adding behavior have full step-by-step happy paths. | Performing routine workflows. | During the selected workflow; operation-specific. | Medium; omission frequency is unmeasured across routine workflows. | `Tool*` | Workflow tools should supply the next local action and prefilled state instead of loading every path into the entrypoint. |
| i062 | n0002: Human-judgment verification and multi-session work remain future work. | Choosing acceptance gates or task boundaries. | During specialized planning; unresolved. | Critical in affected domains; repeatedly observed. | Governing note | Current sources identify the gap but do not authorize a complete method. |
| i063 | s0010: Notes preserve reusable non-authoritative guidance and never establish behavior. | Choosing a note and interpreting its authority. | Before entity selection; global. | High; anticipated. | `SKILL.md` | The distinction is short and prevents advice from becoming binding. |
| i064 | s0010: Create notes only for reusable guidance; promote authoritative content and remove fully replaced notes. | Creating or maintaining notes. | During note operations; operation-specific. | Medium; omission frequency is unmeasured because notes are new in v0.2. | `Tool*` | The provider must prompt for reuse and authority rather than create a note for every finding. |
| i065 | s0011: References preserve copied external material; judgment belongs in a citing spec or note. | Choosing a reference and separating source from interpretation. | Before entity selection; global. | High; anticipated corruption risk. | `SKILL.md` | This is the minimal authority boundary for references. |
| i066 | s0011: Reference identity, source/selection metadata, hierarchy, fidelity, and change restrictions. | Creating or maintaining a reference. | During reference operations; operation-specific. | Medium; omission frequency is unmeasured because references are new in v0.2. | `Tool*` | A reference tool must preserve source contents and keep interpretation out. |
| i067 | s0008: `project.toml` is optional, read-only to agents, and controls project-level modes. | Finding effective policy. | Before entity edits; global. | Critical; omission frequency is unmeasured across routine policy resolution. | `SKILL.md` | The primary agent must know to inspect configuration before applying defaults. |
| i068 | s0008: Configuration tables, valid values, explicit defaults, and in-band comments. | Creating or validating configuration. | During initialization; operation-specific. | Medium; omission frequency is unmeasured across routine initialization. | `Tool*` | `init` must generate a self-descriptive complete policy file. |
| i069 | s0005: Tools should expose workflow operations rather than raw frontmatter manipulation. | Designing plugin interfaces. | During tool design; internal. | Medium; repeated usability cost was observed in manual entity manipulation. | Governing spec | Runtime agents need operation names and results, not this design rationale. |
| i070 | s0005: Tool messages identify result, state change, permission to proceed, next action, and likely-forgotten constraints. | Using a worklog operation safely. | At each tool result; operation-specific. | High; process-rule suppression was repeatedly observed. | `Tool*` | Each provider must deliver local constraints at the point of choice. |
| i071 | s0005: Independent multi-target operations support batching and defined partial-failure behavior. | Performing bulk entity work. | During batch operations; operation-specific. | Medium; omission frequency is unmeasured across routine batch opportunities. | `Tool*` | The tool owns per-target execution and reporting semantics. |
| i072 | s0005: `init` confirms adoption, creates only minimum structure/configuration, preserves compatible v0.1 data, and does not imply coverage. | Initializing worklog. | During initialization; operation-specific. | High; repeatedly observed. | `Tool*` | `SKILL.md` keeps the adoption trigger; `init` must deliver all structural and compatibility details before writing. |
| i073 | s0005: `init` is idempotent and fails without partial changes on conflicts. | Re-running or repairing initialization. | During initialization; operation-specific. | High; anticipated destructive risk. | `Tool*` | Deterministic preflight and result reporting belong in the tool. |
| i074 | s0005: Tools use Python without additional dependencies. | Implementing plugin tools. | During implementation; internal. | Medium; omission has not yet been observed in v0.2. | Governing spec | This does not change an ordinary worklog decision. |
| i075 | v0.1: Exact script catalog, flags, plugin-directory invocation template, and two-step archive CLI. | Invoking old tools. | Never as v0.2 behavior. | None from omission; stale-interface use was observed after tools changed. | Nowhere | New tool interfaces must come from s0005 rather than legacy commands. |
| i076 | s0006: No auxiliary skills are currently defined. | Whether to route to another skill. | During composition; internal. | None; omission has no runtime consequence. | Nowhere | Absence of a provider needs no runtime instruction. |
| i077 | s0007: Auxiliary agents may cover writers, proofreaders, and similar delegated roles. | Whether specialist procedures can leave the entrypoint. | Before delegation; global routing. | High; omission has not occurred because delegation is not yet established. | `Agent*` | s0007 must define a trigger, inputs, authority boundary, and result contract before any unit is omitted from `SKILL.md`. |
| i078 | n0003, n0004: Unauthorized edits, contradictory specs, ungoverned behavior, false completion, stale write-back, and incomplete governance links are critical or high recurring failures. | Prioritizing limited entrypoint space and review. | During composition and evaluation; global. | Critical/high; repeatedly observed. | Governing spec | s0004 turns these evidence categories into mandatory coverage and deletion tests rather than copying the pitfall catalog. |
| i079 | n0003: Requirement-strength errors, history, implementation detail, duplication, stale status, and comment narration are recurring but more locally repairable. | Choosing direct rules versus specialist review. | During authoring/review; operation-specific. | Medium; repeatedly observed. | `Agent*` | Authoring and audit providers can inspect the concrete artifact at lower routine context cost. |
| i080 | n0003: Legacy decisions must not be rewritten or erased. | Migrating or maintaining a v0.1 worklog. | Before compatibility work; global. | High; observed. | Nowhere | The user authorized omitting decision-specific skill guidance; generic v0.1 preservation in the entrypoint and i072 prevents destructive cleanup without naming the deprecated entity. |
| i081 | s0002: New decisions are deprecated and must not be created. | Choosing an entity for rationale or further work. | Before entity selection; global. | High; repeatedly observed in v0.1. | Nowhere | The user authorized omission; exhaustive routing among current entity types and current tool interfaces makes a separate deprecated-type warning redundant and avoids suggesting its use. |
| i082 | n0004: Repository-specific mistakes remain evidence rather than general methodology by themselves. | Whether one incident becomes a universal prompt rule. | During composition; internal. | Medium; overfitting and bloat were repeatedly observed in prior rule writing. | Governing note | Generalize only when a governing spec, recurring pitfall, or cross-case consequence supports it. |
| i083 | v0.1 and its exams: Strong archive wording, explicit marker verification, chore framing, and script-path negatives changed behavior; many duplicated or non-preventing prompts did not. | Selecting and compressing entrypoint language. | During composition/evaluation; internal. | High; context costs and behavioral regressions were repeatedly measured. | Governing note | Preserve the demonstrated mechanisms through s0004 review criteria without freezing v0.1 prose. |
| i084 | v0.1: Decisions as a supported entity, priority/backlog behavior, mandatory hotfix post-mortems, and fixed workflow tables. | Reusing legacy methodology. | Never unless reauthorized. | None from omission; retention would reintroduce superseded behavior. | Nowhere | These behaviors are absent, deprecated, or not authoritative in v0.2. |
| i085 | n0002: Adoption surveys establish verified current state and do not reconstruct project history. | What evidence becomes the initial authoritative spec set. | During later adoption; operation-specific. | High; observed. | `Agent*` | An adoption specialist must distinguish current behavior, human intent, and historical narration before drafting coverage. |
| i086 | s0002, n0002: Report agent-authored entities or content that still requires human review. | Ending a session without hiding draft authority. | At closure; global. | High; observed. | `Tool*` | Entity and close-out tools must surface unresolved `NEEDS APPROVAL`; the entrypoint retains a fallback until that query exists. |
| i087 | s0005, n0004: Supported operations and entity types come from the current tool interface rather than assumption or legacy behavior. | Choosing and invoking a tool. | At invocation; operation-specific. | Medium; observed. | `Tool*` | Help, validation, and errors must make unsupported operations visible before state changes. |
| i088 | s0004: The entrypoint is derived execution guidance and not independent authority. | Resolving a conflict between generic skill text and project specs. | During composition and use; global. | Critical; reversal has not been observed in v0.2. | Governing spec | Runtime precedence is already carried by i028; composition must not turn summaries into a second methodology source. |
| i089 | s0004: The entrypoint supplies the smallest reliable pre-provider context and ordinary use avoids repository archaeology. | Deciding whether a unit remains loaded routinely. | During allocation; internal. | High; recurring context cost was measured in v0.1. | Governing spec | This is the central allocation principle, not runtime methodology content. |
| i090 | s0004: Applicability, authority, entity routing, spec integrity, task governance, completion, compatibility, and provider routing are retained categories. | Reviewing category coverage. | During composition; internal. | Critical/high; no omission is observed because the v0.2 artifact is unimplemented. | Governing spec | Category requirements preserve purpose while n0005 carries unit detail. |
| i091 | s0004: Tool or agent delegation requires a pre-decision delivery guarantee and a direct-operation fallback until established. | Omitting detail from the entrypoint. | During allocation and provider design; global routing. | Critical/high; no omission is observed because delegation is not yet effective. | Governing spec | This prevents aspirational providers from becoming justification for missing context. |
| i092 | s0004: YAML frontmatter, discriminating discovery, shallow form, meaningful examples, and the 7,646-byte baseline. | Building and reviewing the final artifact. | During skill implementation; internal. | Medium/high; one syntax error was observed and context/discovery risks are anticipated. | Governing spec | These constraints concern the delivered artifact rather than ordinary worklog operations. |
| i093 | s0004: The inventory has complete source coverage, stable units, one destination, fingerprints, and deterministic staleness. | Maintaining allocation after source changes. | Before skill acceptance; internal. | High; manual-sync drift was observed in v0.1 and remains anticipated here. | Governing spec | n0005 stores the derived state; s0004 establishes its required properties. |
| i094 | s0004: Deletion tests, happy-path walkthroughs, pitfall coverage, and realistic behavioral evaluation gate the artifact. | Deciding whether the entrypoint is sufficient and nonredundant. | During review; internal. | Critical/high; behavioral regressions were repeatedly observed in v0.1 evaluations. | Governing spec | These checks replace intuition that concise or complete-looking prose will work. |

## Suggested features (NEEDS APPROVAL)

These items are evidence-backed possibilities, not current worklog behavior or approved allocations.

| ID | Suggested feature | Evidence and benefit | Likely destination |
| --- | --- | --- | --- |
| f001 | Add an automated inventory-staleness check that discovers all current specs and compares source fingerprints. | Prevents a new or edited spec from bypassing this inventory through memory alone. | Repository verification or a tool governed by s0005. |
| f002 | Allow substantial conditional guidance in lazily loaded `references/` beneath the main skill. | The skill-creator guidance supports progressive disclosure without requiring a separate skill or agent for every detailed procedure. | s0004 and the delivered skill package. |
| f003 | Add structural spec-authoring support that separates authorized behavior, unapproved suggestions, and implementation markers before prose is written. | v0.1 exams found speculative placement and missing markers resistant to prompt wording alone. | A create/update tool governed by s0005. |
| f004 | Define an explicit verification taxonomy, including representative runtime, serialized-wire, perceptual, editorial, expert, and human acceptance gates. | Mechanical proxy success repeatedly produced false completion across otherwise unrelated projects. | s0009 or a dedicated verification spec, then an auxiliary verifier. |
| f005 | Decide whether tests-before-implementation and isolated spec-derived test design are authoritative v0.2 behavior. | The guidance exists in n0002 and v0.1 and has repeated supporting evidence, but current specs do not establish it. | s0009 or a separate testing spec. |
| f006 | Define how to reject, retire, or reconcile partial worklog adoption when another team process is authoritative. | Confirming adoption prevents creation but does not repair an already-partial competing ledger. | s0002 or a project-adoption spec. |
| f007 | Define checkpointing and splitting for genuinely multi-session investigations and external runs. | One-session tasks fit ordinary work but do not cover long experiments without either stale state or oversized tasks. | s0009 and an investigation agent. |
| f008 | Add a specialist audit for comments that duplicate authority, narrate task history, or assert a spec rule over divergent code. | Comment narration recurred after direct correction, while simple entrypoint wording was previously non-preventing. | s0007 auxiliary agent. |

## Coverage walkthrough

### Happy paths

| n0002 path | Principal coverage | Remaining suggested work |
| --- | --- | --- |
| Starting a new project | i001–i003, i009–i018, i030–i037, i041–i050, i055, i061, i063–i068, i072–i073 | f003 and f005 could strengthen authoring and test order. |
| Introducing worklog to an existing project | i001–i004, i030–i037, i067–i068, i072–i073, i085 | f006 would define reconciliation of an already-partial adoption. |
| Adding or changing behavior | i019–i037, i041–i050, i056, i061 | f003 and f005 could make specification and test ordering structural. |
| Fixing a bug | i028–i032, i041–i050, i053, i056 | f005 would decide whether the currently non-authoritative test-first guidance binds. |
| Investigating or reviewing | i041–i051, i049, i057, i060, i086 | f004 and f007 would cover human judgment and multi-session evidence. |
| Refactoring | i030, i036, i041–i050, i058 | f005 could establish authoritative baseline-test ordering. |
| Performing a chore or urgent fix | i041–i050, i059–i061 | No unowned current rule; the narrow i059 exception remains vulnerable and should be scenario-tested. |

### Critical and high-severity pitfalls

| n0003 pitfall | Covering units |
| --- | --- |
| Unauthorized spec modification | i019–i026, i031 |
| Implementation treated as authority | i028–i029 |
| Behavioral change framed as non-behavioral work | i030, i044, i047 |
| `UNIMPLEMENTED` treated as unapproved | i015, i017, i025 |
| Related specs left contradictory | i032, i036 |
| Unbuilt behavior presented as implemented | i015–i017, i049–i050 |
| Durable behavior has no spec | i030, i047 |
| Placeholder work marked done | i048–i050 |
| Current state stranded in task history | i037, i044, i050 |
| Governance links do not match the implementation surface | i036, i044–i045 |
| Parallel authority through partial adoption | i001, i004, i085 |
| Worklog state reconstructed after delivery | i007, i041–i042 |
| Claimed result stronger than evidence | i017, i048–i050 |
| Legacy decision history rewritten or erased | Generic v0.1 preservation in s0004 and i072; decision-specific units i080–i081 are intentionally omitted from runtime guidance. |

### Repository incidents

| n0004 incident family | Covering units or disposition |
| --- | --- |
| Unauthorized or unmarked agent-authored content | i019–i026, i031, i086 |
| Entity referenced by unstable file path | i008 |
| Unsupported tool capability assumed | i087 |
| Substantive work began before task activation | i042–i043 |
| Preferred guidance over-strengthened into absolutes | i034–i035 and s0004's deletion review |
| Optional body guidance expanded into a mandatory template | i035, i052, i089, i094 |
| YAML field written with TOML assignment syntax during t0009 | Corrected and recorded; i092 requires valid frontmatter, while artifact validation remains implementation work. |
| Inventory impact recorded without explicit omission frequency during t0009 | Corrected in every current row; i093–i094 and f001 cover future inventory validation. |
| Required spec approval unresolved when t0009 was completed and archived | Corrected by reopening t0009 as active; i017, i025–i026, i049–i050, and i086 cover approval-aware completion and close-out. |

### Allocation findings

- The current sources leave test-first authority, verification modes, partial-adoption retirement, and multi-session work unresolved; f004–f007 keep these gaps visible without silently adding behavior.
- v0.1 entity templates, superseded entity creation, priority/backlog behavior, script interfaces, Git-only drift, and fixed workflow tables are intentionally excluded rather than carried forward by inertia.
- Decision-specific runtime guidance is intentionally omitted with user authorization: current-entity routing makes deprecated creation unavailable, while generic v0.1 preservation covers compatibility without teaching the obsolete entity.
- Tool and agent allocations are conditional because s0005 and s0007 do not yet establish most providers.
- The old evaluation history supports keeping marker verification, governance framing, and close-out integrity salient while moving mechanical detail out of the entrypoint.

## Source review state

The required dynamic source set is every current entity under `worklog/spec/`.
The named evidence sources are n0002, n0003, n0004, and the final v0.1 `SKILL.md` baseline.
Fingerprints use Git blob object IDs so line-ending conversion and entity renames can be checked reproducibly.

| Source | Fingerprint |
| --- | --- |
| s0001 | `7ac1f801311449ef1841691e60c3478635425986` |
| s0002 | `efbb365ad7108f1f54b50b346d19b51063cbd402` |
| s0003 | `d17626f4dce4eafc41e9f330f0e21d6da8633e14` |
| s0004 | `279f79bf06951d51e8d362efd2b805775031a090` |
| s0005 | `c9cb5369c07eb9ef5197c18eb4d130ed30021faf` |
| s0006 | `5d107410fba90040699e240927f2f46fae4772f1` |
| s0007 | `262324af94fe107411d154f9aac9d6c5cf53b21c` |
| s0008 | `6d07905aa0f0532d0a12de2404b5363b44e0afb8` |
| s0009 | `c200403b730f8b60b4e5584a33db8669317eb6eb` |
| s0010 | `923ea333cb90c2205d9b29ad0a7983649a9fdb7a` |
| s0011 | `f3f06dee98b2c190528e89dc3676a6a497300199` |
| s0012 | `5a65bf77759cb96ef46f2848bf7c38eee3100799` |
| n0002 | `50ee5e8463b7e24b11a31f1adb6e0d209f73d8fb` |
| n0003 | `844c41fedf4c1328fc3c6de4e1c80a248515ab81` |
| n0004 | `fa17ff5d660f7ce26d7b31f69add287126a83232` |
| v0.1 `SKILL.md` baseline | `bd3f656b3ceb457e3eaf2583223b6083204a0a9b` |
