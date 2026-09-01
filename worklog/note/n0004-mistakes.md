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
