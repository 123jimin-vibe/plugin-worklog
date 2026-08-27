+++
id = "s0011"
title = "Reference entities"
+++

# Reference entities

## Related entities

- s0002 defines common entity rules.
- s0012 defines agent mode, which does not apply to references.
- n0001 guides writing.

## Principles

- A reference separates copied external material from Worklog judgment.
- Judgment about a reference belongs in the spec or note that cites it.

## Inherent properties

### Identity

- References do not have IDs.
- `agent_mode` does not apply to references.

### Content boundary

- Reference frontmatter is metadata, not part of the copied source contents.
- Once created, an agent SHOULD NOT change a reference.

## Desirable properties

### Creation

- Create a reference only when the external material is consulted repeatedly or its source may change or disappear.

### Organization

- References SHOULD be arranged hierarchically under `worklog/ref/`.

### Metadata

- Frontmatter SHOULD identify the original `source` via URL.
- A partial extraction SHOULD identify its `selection`.

### Fidelity

- Contents SHOULD preserve the source's contents.
- Format conversion and partial extraction MAY be performed while creating the reference.
- Copied contents SHOULD NOT be rephrased or supplemented with clarification.
