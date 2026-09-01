+++
id = "t0009"
title = "Determine SKILL.md content allocation"
tags = ["methodology", "skill"]
status = "active"
modifies = ["s0004"]
+++

# Determine `SKILL.md` content allocation

Define the content boundary for the delivered `SKILL.md`: which information belongs there, which information belongs elsewhere, and how future authors and reviewers can make that distinction consistently.

This task determines content categories and allocation criteria.
It does not draft the final prose of `SKILL.md`, specify the complete contents of any tool message or generated file, or design auxiliary-agent internals.

The result MUST:

- make `SKILL.md` shorter overall than v0.1 without setting an arbitrary size target;
- retain the information needed to enforce essential worklog invariants;
- reduce routine interpretation, file reading, and process overhead on the n0002 happy paths;
- address recurring mistakes represented by n0003 and n0004; and
- allow operation-specific guidance and prefilled state to be delegated to tooling governed by s0005, and specialized handling or auditing to agents governed by s0007.

## Proposed determination method

1. Build an inventory of candidate information units from the worklog specs, n0002, n0003, n0004, and the v0.1 `SKILL.md`.
   Keep each unit small enough to allocate independently.
2. For each unit, record:
   - the decision or action it affects;
   - when it must become available;
   - whether it applies globally or only to one operation;
   - the consequence and observed frequency of omission; and
   - whether a tool or auxiliary agent can deliver it reliably at that point.
3. Allocate each unit to exactly one primary location:
   - `SKILL.md` when the primary agent must know it before choosing or invoking the applicable tool or agent, when it is a cross-workflow invariant, or when omission could silently compromise authority, scope, verification, or completion;
   - a tool when the information is operation-specific and the tool can provide it before the affected choice through concise output or a prefilled file;
   - an auxiliary agent when the information is a bounded specialist procedure and the primary agent only needs a reliable trigger and handoff contract;
   - a governing spec or note when the information need not be present during ordinary execution; or
   - nowhere when it is rationale, history, duplication, or detail that does not change correct use.
4. For delegated units, retain in `SKILL.md` only the routing information needed to recognize when to invoke the provider and what result is required.
   Do not treat delegation as valid until s0005 or s0007 establishes that the context will actually be delivered at the required point.
   Record any missing delivery guarantee as an input to t0006 or t0007 rather than assuming it.
5. Challenge every retained unit with a deletion test: identify the concrete happy path or mistake-prevention property that becomes unreliable if the unit is removed.
   Remove or delegate units without such a justification.
6. Walk the resulting allocation through each applicable n0002 happy path, each critical or high-severity n0003 pitfall, and the relevant n0004 incidents.
   Record uncovered decisions, duplicated guidance, and unnecessary routine reads, then revise the allocation.

The inventory and allocation rationale MAY remain working material in t0009 while it is active.
Only durable content-boundary requirements and review criteria are written to s0004.

## Proposed completion criteria

Complete when s0004 is sufficient to write and review `SKILL.md` without deciding its content boundary again, including all of the following:

- every retained content category has a stated essential purpose;
- s0004 defines an objective length comparison and requires the delivered `SKILL.md` to be shorter than the v0.1 baseline;
- every excluded or delegated category has a named primary destination or an explicit reason for omission;
- every tool or agent delegation identifies the trigger and delivery guarantee that s0005 or s0007 must provide;
- the primary agent can follow the n0002 happy paths without routine methodology archaeology or avoidable delegation;
- critical and high-severity mistakes cannot be attributed to an unowned information gap in the allocation; and
- a reviewer can reject redundant content even when that content is individually correct.

## Work performed

- Reviewed all 12 current specs, n0002–n0004, the 7,646-byte final v0.1 `SKILL.md`, its recorded evaluation/compression history, the aggregate happy-path survey, and all 14 authorized case-study reports.
- Created n0005 with 94 independently allocated current units, 8 clearly separated suggested features, and fingerprints for all 16 required sources.
- Allocated 38 units to `SKILL.md`, 20 conditionally to tools, 12 conditionally to auxiliary agents, 17 to governing specs or notes, and 7 nowhere.
- Walked the allocation through every n0002 happy path, every critical or high-severity n0003 pitfall, and each relevant n0004 incident.
- Left test-first authority, verification modes, partial-adoption retirement, and multi-session work visibly unresolved rather than silently adding behavior.
- Prepared a `NEEDS APPROVAL` s0004 proposal covering content categories, allocation rules, reproducible inventory maintenance, provider guarantees, the objective v0.1 length comparison, and review criteria.
- Prepared `NEEDS APPROVAL` provider-result categories in t0006 and trigger/handoff requirements in t0007 without specifying complete messages or agent internals.
- Verified unique inventory IDs and entity IDs, valid allocation destinations, table shape, complete source fingerprints, baseline size, and clean patch whitespace before the approval correction.
