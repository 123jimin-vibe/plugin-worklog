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

| Relevant Worklog | Relevant File(s) | Intended Task | Mistake |
| --- | --- | --- | --- |
| s00, n00 | example/test.md | Instructed to write an example. | This is an example. |
| s0002, s0003, s0008 | — | Define project agent policy. | Invented a `confirmed` frontmatter field without user approval. |
| s0003, s0008 | — | Define recommended markers. | Applied a spec change before human approval despite effective `agent_mode = "propose"`. |
| s0002, s0008 | — | Reorganize entity specs. | Added the ID-over-filepath rule without human approval despite effective `agent_mode = "propose"`. |
| n0003 | — | Fill the Worklog pitfalls note. | Invoked `list.py --type note` even though the current script does not support note entities. |
