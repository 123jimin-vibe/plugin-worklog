+++
id = "s0004"
title = "SKILL.md"
paths = ["plugin/skills/worklog/SKILL.md"]
+++

# `SKILL.md` (NEEDS APPROVAL)

## Principles

- The delivered `SKILL.md` is an execution entrypoint derived from the worklog specs, not an independent source of authority.
- It SHOULD give the primary agent the smallest reliable context needed before an operation-specific tool or auxiliary agent can supply the rest.
- Ordinary use SHOULD NOT require access to this repository's specs, notes, task history, or allocation rationale.
- Concision serves reliable decisions and low routine context cost; completeness and a fixed section template are not goals.

## Content inventory

- n0005 is the non-authoritative content inventory used to write and review the delivered `SKILL.md`.
- The inventory MUST cover every current worklog spec, n0002, n0003, n0004, and the final v0.1 `SKILL.md` baseline.
- The inventory MUST divide source material into information units small enough to allocate independently.
- Each unit MUST record:
  - its source;
  - the decision or action it affects;
  - when it must become available;
  - whether it is global or operation-specific;
  - the consequence and observed frequency of omission;
  - exactly one primary location; and
  - the allocation rationale or provider guarantee.
- Primary locations are the delivered `SKILL.md`, a tool, an auxiliary agent, a governing spec or note, or nowhere.
- Suggested behavior not yet authorized MUST be visibly separate from the current allocation and MUST NOT be treated as delivered methodology.
- The inventory is derived traceability data and MUST NOT override a governing spec.
- The inventory MUST identify its complete source set and a reproducible fingerprint for each source.
- Adding, removing, or changing a source makes the inventory stale until the affected units and fingerprint are reviewed.
- A stale inventory MUST prevent acceptance of a new or changed delivered `SKILL.md`.

## Delivered artifact (UNIMPLEMENTED)

### Entrypoint content

The delivered `SKILL.md` MUST retain these categories because the primary agent needs them before it can safely choose or invoke a provider:

- **Applicability and orientation:** establish that using worklog is the project's choice, identify the worklog as durable project state, and prevent partial adoption from creating parallel authority.
- **Authority and approval:** resolve effective agent mode, distinguish permission from content authority, preserve spec precedence, and prevent implementation of unauthorized behavior.
- **Entity routing:** distinguish specs, tasks, notes, and references so information enters the correct durable record.
- **Spec integrity:** preserve current authoritative behavior, distinguish approval from implementation state, require related-spec review, and prevent durable behavior from escaping specification.
- **Task governance:** require timely task state, complete `modifies`, correct dependency semantics, and subordination to governing specs.
- **Completion integrity:** calibrate claims to evidence, reject placeholders as completion, reconcile affected specs and markers, and archive resolved tasks.
- **Backward compatibility:** preserve compatible v0.1 worklog data without reintroducing superseded methodology.
- **Provider routing:** state when a tool or auxiliary agent is required and what result the primary agent must receive.

The entrypoint SHOULD include only enough entity syntax and file layout to orient a cold reader and use the available providers.
Details that a reliable provider supplies before the affected choice SHOULD NOT be duplicated in the entrypoint.

### Delegation

- Operation-specific mechanics, validation, prefilled state, and close-out reminders SHOULD be delivered by tools governed by s0005.
- Bounded specialist procedures for authoring, investigation, review, or verification SHOULD be delivered by auxiliary agents governed by s0007.
- A delegated unit MUST retain only its trigger and required result in the entrypoint.
- Delegation is not effective until the provider's governing spec guarantees that the information arrives before the affected decision.
- Until that guarantee exists, the entrypoint MUST retain enough of the unit for correct direct operation.
- Rationale, history, obsolete v0.1 behavior, duplicated guidance, and information that does not alter correct ordinary use SHOULD remain in their governing source or be omitted.

### Form

- The skill MUST use valid agent-skill YAML frontmatter with `name: worklog` and a concise, discriminating description.
- The description MUST make Worklog operations discoverable without implying that activation authorizes adoption or initialization.
- The Markdown body SHOULD be shallow, direct, and organized around decisions or workflows rather than mirroring the spec hierarchy.
- Examples SHOULD appear only when they materially disambiguate fragile behavior.
- A canonical UTF-8 rendering with LF line endings and no byte-order mark MUST be smaller than 7,646 bytes, the final v0.1 baseline.
- Content needed only in a specialized operation SHOULD be progressively disclosed through its guaranteed provider.

### Review

- Every retained unit MUST pass a deletion test identifying the concrete happy path or mistake-prevention property that becomes unreliable without it.
- Every excluded or delegated unit MUST have a named primary destination or an explicit reason for omission.
- The allocation MUST be walked through every applicable n0002 happy path, every critical or high-severity n0003 pitfall, and relevant n0004 incidents.
- A critical or high-severity mistake MUST NOT remain attributable to an unowned information gap.
- The primary agent MUST be able to follow ordinary happy paths without routine methodology archaeology or avoidable delegation.
- A reviewer MAY reject content that duplicates another reliable provider even when the duplicated statement is correct.
- Behavioral evaluation SHOULD use realistic scenarios and claimed outcomes rather than merely checking headings or wording.
