+++
id = "t0008"
title = "Determine recommended entity structures"
tags = ["entities", "methodology"]
status = "active"
modifies = ["s0003", "s0009", "s0010"]
+++

# Determine recommended entity structures

Determine recommended structures for specs, tasks, and notes.
In particular, preserve useful forward-looking context through a `Possible future changes` section where appropriate.
Its heading and contents must distinguish possibilities from authoritative behavior, including `UNIMPLEMENTED` behavior.

Evaluate each recommended structure by these criteria:

- **Highly flexible:** It applies across varied uses of the entity type.
  For example, a task may only modify another task, coordinate many child tasks, or fix one bug.
- **Beneficial:** Following it clearly improves both writing and reading the entity.
- **Natural:** Its headings communicate their purpose well enough that agents can use it without separate instructions.

Complete when the applicable entity specs describe concise recommended structures that satisfy these criteria.
