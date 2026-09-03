+++
id = "n0004"
title = "Mistakes"
agent_mode = "autonomous"
+++

Record any mistake made while working on this repository, regardless of its nature.
Entries for similar mistakes happened in one session are encouraged to be merged.

Following are **not** in scope:
- Tool use mistakes (except worklog tools).
- Mistakes happened in `local/`.

The first row is an example.

| Relevant worklog | Relevant File(s) | Intended Task | Mistake |
| --- | --- | --- | --- |
| s00, n00 | example/test.md | Instructed to write an example. | This is an example. |
| s0002, s0003, s0012 | — | Define project agent policy. | Invented a `confirmed` frontmatter field without user approval. |
| s0003, s0012 | — | Define recommended markers. | Applied a spec change before human approval despite effective `agent_mode = "propose"`. |
| s0002, s0012 | — | Reorganize entity specs. | Added the ID-over-filepath rule without human approval despite effective `agent_mode = "propose"`. |
| n0003 | — | Fill the worklog pitfalls note. | Invoked `list.py --type note` even though the current script does not support note entities. |
| t0009, s0012 | — | Make t0009 concrete and propose a content-determination method. | Left some agent-authored task content outside a `NEEDS APPROVAL` section despite effective `agent_mode = "draft"`. |
| s0002, n0004, t0009 | — | Record the missing-marker mistake in n0004. | Identified t0009 by its file path even though worklog entities should be referenced by ID. |
| t0010, s0009 | — | Analyze case studies and propose additions to n0003. | Began substantive task work before changing t0010 from `pending` to `active`. |
| t0004, t0008, s0003, s0009 | — | Define flexible entity organization and task lifecycle guidance. | Overused `MUST` and `MUST NOT` for preferred guidance and assumed normal workflows, affecting t0008’s changeability and blocker guidance and earlier s0009 activation and t0004 hierarchy rules. Treated ambiguity reduction as proof that no valid exception existed. |
| t0008, s0009 | — | Recommend task body organization. | Added too many optional headings and rules, turning flexible guidance into an implicit template. |
| t0009, s0004 | — | Determine `SKILL.md` content allocation. | Wrote the required YAML `name` field using TOML-style assignment syntax before correcting it. |
| t0009, s0004, n0005 | — | Determine `SKILL.md` content allocation. | Initially left omission frequency implicit in several inventory rows even though the required inventory fields include both consequence and observed frequency. |
| t0009, s0004, s0009, s0012, t0006, t0007 | — | Execute t0009. | Edited s0004, t0006, and t0007 without the required `NEEDS APPROVAL` markers, then marked t0009 done and archived it while required spec content still lacked approval. |
| t0009, s0009, s0012 | — | Correct t0009 after restoring the required approval markers. | Treated unresolved content approval as a task blocker and set t0009 to `blocked`, conflating content authority with task actionability even though the task remained active. |
| t0009, s0004, n0005, s0012 | — | Define maintainable `SKILL.md` content and freshness requirements. | Made s0004 normatively depend on a manually maintained 94-unit n0005 inventory whose note permissions allowed non-authoritative edits, creating a de facto authority cycle, duplicated required-content definitions, and excessive maintenance work. |
| t0009, s0004 | — | State concise `SKILL.md` requirements. | Used indirect, clause-heavy wording for delegation and freshness requirements, making unchanged semantics harder to parse than necessary. |
| s0002, s0004, s0005, s0009, s0012 | plugin/skills/worklog/SKILL.md | Write the v0.2.0 worklog skill from its specs. | Overstated recommended task creation as mandatory, omitted individual agent-mode effects, implied an agent might remove `NEEDS APPROVAL`, overconstrained tool output as preceding every action, and used fixed-width wrapping instead of semantic line breaks. |
| s0002, s0004, s0012 | plugin/skills/worklog/SKILL.md | Review and finish the v0.2.0 worklog skill. | Failed to report that s0004's delivered-artifact `UNIMPLEMENTED` marker appeared stale after verification or request scoped permission to update the `propose`-mode spec. |
| s0004, s0012 | plugin/skills/worklog/SKILL.md | Compress worklog authority guidance. | Wrote the `read_only` rule so “unless asked” could modify both the unconditional edit prohibition and the conditional preparation guidance. |
| s0004 | plugin/skills/worklog/SKILL.md | Review the worklog skill for v0.1 compatibility. | Mistook required behavioral compatibility for a requirement to mention v0.1 explicitly, proposing unnecessary historical wording. |
| t0006, t0007, s0005, s0007, s0013 | — | Propose the worklog tool inventory. | Initially omitted the local `UNIMPLEMENTED` marker from the approved `init` header, overstated the CLI's ability to distinguish human approval or judge semantic evidence, used opaque or uncommon command names, and assigned arbitrary-format reference capture to a deterministic tool. |
| t0006, s0005 | — | Define common tool complexity requirements. | Treated quasi-constant time as a requirement on an optimized current implementation rather than a counterfactual optimizability requirement that permits the current implementation to remain linear, then marked vacuously satisfied common constraints as `UNIMPLEMENTED`. |
| t0006, s0005 | — | Refine the proposed tool inventory. | Added an undemonstrated manifest input, scattered relationship updates across narrow commands, and proposed marker and broad validation tools before their need was established. |
| t0006, s0005 | — | Refine the proposed tool inventory. | Used redundant type prefixes in relationship operations, framed mutable fields as links, separated task completion from archival, and revised the inventory without rerunning it against n0002 and n0003. |
| t0006, t0012, s0005, s0013 | plugin/skills/worklog/scripts, tests, worklog/tags.csv | Carry out t0012. | Implemented tool and artifact work owned by active t0006, then completed and archived t0012 despite that ownership boundary. |
| t0006, t0012, s0002, s0015 | worklog/spec/entity/s0015-tags.md | Specify the tag database. | Treated t0006's implementation ownership as grounds to mark whole semantic sections `UNIMPLEMENTED`, conflating task ownership with the delivery state of rules that already govern manual and compatible worklog use. |
| t0006, t0013, t0014, t0015, t0016, t0017, t0018, t0019, s0012 | — | Create child implementation tasks for the worklog tools. | Treated the instruction to create tasks as approval of agent-authored scope, dependencies, `modifies` sets, and completion criteria, leaving that draft content outside `NEEDS APPROVAL` markers. |
