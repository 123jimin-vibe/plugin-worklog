+++
id = "s0003"
title = "Spec entities"
+++

# Spec entities

A spec is an authoritative specification of current project behavior.

## Relevant entries

- s0002 defines common entity rules and markers.
- s0008 defines project-level agent policy.
- n0001 guides writing.
- n0002 describes the expected happy path.
- n0003 records pitfalls.

## Structure

- ID prefix: `s`.
- A spec MAY declare `paths`: globs for governed project files.

## Judgment

- Create a spec for behavior expected to outlast the current task.
- State observable behavior, constraints, known failure modes, and expected future changes.
- A spec SHOULD NOT contain behavior-independent implementation details or individual file paths.
  - Name governed files with `paths` globs.
- Include only behavior authorized by the applicable `agent_mode` and its direct entailments as authoritative content.
  - Agent-authored spec content is authoritative only after required human approval, or when the applicable mode is `autonomous`.
  - Clearly mark content awaiting human approval.
- A spec outranks source code and tests.
  - Treat divergence as a code defect.
  - If the spec seems wrong, resolve it under the applicable `agent_mode`; never override it silently.
- Specs MUST NOT contradict each other.
  - Before changing a spec, check specs governing related behavior.
- Agent-authored behavioral changes MUST follow the applicable `agent_mode`, including changes made while implementing a task.
- Update a spec in the same session as any change that invalidates it.
- Remove behavior the spec no longer governs; do not retain it as history.
