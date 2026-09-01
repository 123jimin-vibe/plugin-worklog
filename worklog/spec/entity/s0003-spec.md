+++
id = "s0003"
title = "Spec entities"
+++

# Spec entities

## Related entities

- s0002 defines common entity rules and markers.
- s0012 defines agent modes and entity policy.
- n0001 guides writing.
- n0002 describes the expected happy path.
- n0003 records pitfalls.

## Principles

- A spec is an authoritative specification of current project behavior.
- A spec outranks source code and tests.
  - Treat divergence as a code defect.
- The applicable `agent_mode` determines whether agent-authored spec content is authoritative.

## Inherent properties

### Identity

- ID prefix: `s`.
- A spec MAY declare `paths`: globs for governed project files.

### Authority

- Include only behavior authorized by the applicable `agent_mode` and its direct entailments as authoritative content.
  - Agent-authored content is authoritative only after required human approval, or when the applicable mode is `autonomous`.
- Clearly mark content awaiting human approval.
- Specs MUST NOT contradict each other.
- Agent-authored behavioral changes MUST follow the applicable `agent_mode`, including changes made while implementing a task.
- If a spec seems wrong, resolve it under the applicable `agent_mode`; never override it silently.

## Desirable properties

### Creation

- Create a spec for behavior expected to outlast the current task.

### Content

- State observable behavior, principles, constraints, known failure modes, and changeability requirements.
- A spec SHOULD NOT contain behavior-independent implementation details or individual file paths.
  - Name governed files with `paths` globs.
- Do not include non-binding possibilities.
  Preserve them in a note only when they provide reusable guidance, and put actionable work in a task.

### Body organization

- A principle is authoritative guidance for interpreting requirements and deciding matters they leave open.
  It MUST NOT override an explicit requirement.
- A hard constraint uses `MUST` or `MUST NOT`.
- A soft constraint uses `SHOULD` or `SHOULD NOT`.
- A permission uses `MAY`.
- A spec containing both principles and constraints SHOULD group its principles under `Principles`.
  Constraint strength remains explicit in each statement rather than depending on its heading.
- A short spec MAY put its contents directly below the title.
- A larger spec SHOULD group contents under headings named for the governed domain.
- Include `Known failure modes` when known failures affect correct use or future work.
- Include `Changeability` only when anticipated variations should constrain the current implementation.
  - Each entry SHOULD state a current hard or soft constraint on accommodating a variation; listing a possible feature is insufficient.
  - A changeability constraint does not authorize implementing the variation.
  - State what should remain unchanged or what change surface is acceptable instead of requiring unspecified “low cost.”
  - Implement only the seam or boundary needed by the current constraint, not speculative feature behavior.
- Omit sections that would be empty or merely repeat another section.
- A heading SHOULD classify content that is already needed, not prompt an agent to invent content.

### Maintenance

- Before changing a spec, check specs governing related behavior.
- Update a spec in the same session as any change that invalidates it.
- Remove behavior the spec no longer governs; do not retain it as history.
