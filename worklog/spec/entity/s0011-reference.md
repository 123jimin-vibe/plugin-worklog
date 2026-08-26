+++
id = "s0011"
title = "Reference entities"
+++

# Reference entities

A reference is material copied from an external source.

## Relevant entries

- s0002 defines common entity rules.
- s0008 describes the convenience `agent_mode` value exposed for references.
- n0001 guides writing.

## Structure

- References do not have IDs.
- References SHOULD be arranged hierarchically under `worklog/ref/`.
- Reference frontmatter is metadata, not part of the copied source contents.
- Frontmatter SHOULD identify the original `source` via URL.
- A partial extraction SHOULD identify its `selection`.

## Judgment

- `agent_mode` does not apply to references.
- Create a reference only when the external material is consulted repeatedly or its source may change or disappear.
- Contents SHOULD preserve the source's contents.
  - Format conversion and partial extraction MAY be performed while creating the reference.
- Once created, an agent MUST NOT change a reference.
- Copied contents SHOULD NOT be rephrased or supplemented with clarification.
- Put judgment or comments about a reference in the spec or note that cites it, never in the reference itself.
