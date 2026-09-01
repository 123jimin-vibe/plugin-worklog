+++
id = "t0008"
title = "Determine recommended entity structures"
tags = ["entities", "methodology"]
status = "done"
modifies = ["s0003", "s0009"]
+++

# Determine recommended entity structures

Determine recommended body structures for specs and tasks, and whether notes need one.
Notes remain free-form.
Preserve relevant anticipated variation as current changeability requirements, so agents keep listed changes low-cost without treating them as authorized future behavior.

Evaluate each recommended structure by these criteria:

- **Highly flexible:** It applies across varied uses of the entity type.
  For example, a task may only modify another task, coordinate many child tasks, or fix one bug.
- **Beneficial:** Following it clearly improves both writing and reading the entity.
- **Natural:** Its headings communicate their purpose well enough that agents can use it without separate instructions.
- **Sparse by default:** It does not encourage agents to create or fill sections whose contents are unnecessary.

Complete when the spec and task entity specs describe concise body-organization guidance that satisfies these criteria.
