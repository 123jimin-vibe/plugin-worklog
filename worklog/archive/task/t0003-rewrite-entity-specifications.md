+++
id = "t0003"
title = "Rewrite entity specifications"
status = "done"
modifies = ["s0002", "s0003", "s0009", "s0010", "s0011"]
+++

# Rewrite entity specifications

## Outcome

Rewrite s0002, s0003, s0009, s0010, and s0011 so their hierarchy is coherent, their headers are uniform, and their requirements distinguish inherent properties from authoritative desirable properties.

## Concerns

- Document hierarchy is poorly structured, especially in s0002.
- A uniform set of headers is desirable across entity specifications.
- The documents do not clearly distinguish hard specifications, which describe inherent properties of their subject, from soft specifications, which remain authoritative but describe desirable properties.

## Proposed hierarchy

s0002 should define the meaning of the common headers and classification rules. Each entity specification should then use this top-level hierarchy:

1. `## Related entities`: IDs needed to interpret the document, without restating their rules.
2. `## Principles`: a small set of rules that establish the entity's purpose, authority, and interpretive priorities.
3. `## Inherent properties`: hard requirements without which the subject is not a valid entity of that type.
4. `## Desirable properties`: authoritative quality and process expectations whose violation is undesirable but does not invalidate the entity.

Entity-specific subheadings MAY be added under inherent or desirable properties, such as `Identity`, `State`, `Content`, `Creation`, `Maintenance`, or `Lifecycle`. New concerns should extend these sections instead of adding unrelated top-level sections.

### Classification rules

- Principles explain how to interpret the entity and resolve conflicts; they SHOULD be few and MUST NOT duplicate detailed requirements.
- Inherent properties SHOULD use definitive statements or MUST and MUST NOT where adherence is binary.
- Desirable properties SHOULD use SHOULD and SHOULD NOT; MAY remains available for explicit permissions.
- Each requirement belongs in exactly one place so adherence can be checked without reconciling duplicates.
- Each bullet SHOULD contain one independently checkable requirement.

### Per-entity allocation

| Entity spec | Principles | Inherent properties | Desirable properties |
| --- | --- | --- | --- |
| s0003 | Current-state authority, precedence over code and tests, and the role of approval | ID and `paths`, authority of approved or autonomous content, and non-contradiction | Creation threshold, observable content, scope discipline, related-spec checks, write-back, and removal of history |
| s0009 | One unit of work, subordination to specs, and truthful lifecycle state | ID, required fields, status values, resolution, archive eligibility and location, and terminal-state behavior | Reviewable scope, one-session sizing, outcomes and criteria, `modifies`, blocker handling, verification, write-back, and prompt archival |
| s0010 | Non-authoritative reusable guidance | ID and inability to establish authoritative behavior | Creation threshold, concise guidance, promotion into specs, and removal after replacement |
| s0011 | Faithful preservation of external material and separation of copied content from judgment | Absence of ID and `agent_mode`, source-content boundary, and read-only behavior after creation | Creation threshold, hierarchy, source and selection metadata, and permitted format conversion or extraction |

## Proposed s0002 hierarchy

s0002 should define the common classification model and contain only rules that apply across entity types or preserve compatibility for deprecated entities.

1. `## Related entities`: s0003, s0008, s0009, s0010, s0011, and relevant guidance, cited only by ID.
2. `## Principles`: the role and precedence of common rules, the definitions of inherent and desirable properties, and where new rules belong.
3. `## Inherent properties`: shared validity, authority, and interpretation requirements.
4. `## Desirable properties`: shared quality and maintainability expectations.

### Principles

- Common rules apply to every entity unless they explicitly name a subset.
- Entity-type specs refine s0002 and MUST NOT contradict it.
- Cross-entity concerns extend s0002; rules concerning only one entity type extend that entity's spec.
- Inherent properties determine validity or have binary adherence; desirable properties remain authoritative but permit a nonconforming entity to remain valid.

### Inherent-property allocation

| Subheading | Contents |
| --- | --- |
| `Files and storage` | Entity locations, supported type directories, TOML frontmatter delimiters, filename requirements, and path-independent identity |
| `Identity` | ID composition, normalization, uniqueness, standard and conventional forms, and non-reassignment |
| `Common frontmatter` | Shared fields, types, applicability, and requiredness |
| `Authority and approval` | Applicable `agent_mode`, prohibition on false approval claims, and treatment of content awaiting approval |
| `Marker semantics` | Marker meanings, Markdown-section scope, redistribution after partial status changes, and removal when conditions cease |
| `Legacy decisions` | Decision identity, immutability, and prohibition on creating new decisions |

### Desirable-property allocation

| Subheading | Contents |
| --- | --- |
| `Writing` | Context independence, one subject per entity, current-state register, ID-based references, requirement strength, and avoidance of duplication |
| `Reviewability` | Small independently reviewable changes and reporting of draft changes awaiting approval |

New common concerns should extend one of these subheadings where possible. A new subheading is justified only when its rules cannot be checked coherently under an existing concern.

## Completion criteria

- Establish and apply a uniform document hierarchy across the five entity specifications, with deviations only where an entity type requires them.
- Place common rules in s0002 and entity-specific rules in the corresponding entity specification without duplication.
- Define and consistently distinguish hard and soft specifications.
- Preserve existing requirements unless a semantic change is explicitly identified and approved.
- Update affected Worklog references by entity ID.
