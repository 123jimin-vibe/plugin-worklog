+++
id = "s0004"
title = "SKILL.md"
paths = ["plugin/skills/worklog/SKILL.md"]
+++

# `SKILL.md`

## Principles

- `SKILL.md` derives its guidance from the worklog specs. It is not authoritative on its own.
- `SKILL.md` SHOULD contain the minimum reliable context needed before a tool or auxiliary agent is used.
- Ordinary use SHOULD NOT require access to this repository's specs, notes, task history, or allocation rationale.
- Concision supports reliable decisions and lowers routine context cost. Exhaustive coverage and a fixed section template are not goals.
- Notes, tasks, generated source hashes, and evaluation results MAY inform implementation and review. They MUST NOT define required skill behavior or override a spec.

## Delivered artifact (UNIMPLEMENTED)

### Required content

`SKILL.md` MUST give the primary agent enough guidance to:

- determine whether worklog applies and treat an adopted worklog as durable project state;
- identify authoritative behavior;
- resolve permission to edit separately from the authority of resulting content;
- distinguish content approval from implementation state;
- choose among current entity types and preserve the authority and lifecycle role of each;
- plan and carry out reviewable work without bypassing governing specs or task state;
- satisfy verification, spec write-back, and archival requirements;
- know when to use a tool or auxiliary agent and what it must return; and
- preserve compatible v0.1 worklogs without teaching superseded methodology.

`SKILL.md` SHOULD include only enough entity syntax and file layout to orient a new reader and use the available tools and auxiliary agents.
If a reliable tool or auxiliary agent provides a detail before it is needed, `SKILL.md` SHOULD NOT repeat it.

### Tools and auxiliary agents

- Tools governed by s0005 SHOULD provide operation-specific steps, validation, prefilled state, and close-out reminders.
- Auxiliary agents governed by s0007 SHOULD provide bounded specialist help for authoring, investigation, review, or verification.
- `SKILL.md` MUST state when a tool or auxiliary agent is required and what it must return.
- `SKILL.md` MAY omit guidance only when s0005 or s0007 requires a tool or auxiliary agent to provide it before it is needed.
- Otherwise, `SKILL.md` MUST provide enough guidance to proceed correctly without that tool or auxiliary agent.
- `SKILL.md` SHOULD omit rationale, history, obsolete v0.1 behavior, duplicate guidance, and other content irrelevant to ordinary use.
  Such content MAY remain in its governing source.

### Form

- `SKILL.md` MUST have valid agent-skill YAML frontmatter.
  Its `name` MUST be `worklog`, and its `description` MUST be concise and discriminating.
- The description MUST make Worklog operations discoverable without implying that activation authorizes adoption or initialization.
- The Markdown body SHOULD be shallow, direct, and organized around actions or workflows rather than mirroring the spec hierarchy.
- Examples SHOULD appear only when they clarify behavior that is easy to misunderstand.
- `SKILL.md` MUST use UTF-8 without a byte-order mark and LF line endings.
  In that form, it MUST be smaller than the 7,646-byte final v0.1 version.
- Guidance needed only for a specialized operation SHOULD come from the applicable tool or auxiliary agent.

### Review

- Every retained instruction MUST support ordinary use or prevent a concrete mistake.
- The primary agent MUST be able to follow ordinary workflows without routine repository access or unnecessary delegation.
- A reviewer MAY reject correct guidance that a reliable tool or auxiliary agent already provides.
- Behavioral evaluation SHOULD use a small set of realistic scenarios and assess claimed outcomes.
  It SHOULD NOT mirror individual spec requirements or merely check headings and wording.
- Notes and prior incidents MAY suggest evaluation scenarios, but expected behavior MUST derive from authoritative specs.

## Source freshness (UNIMPLEMENTED)

- Repository verification MUST automatically discover current specs under `worklog/spec/**/*.md`.
  It MUST detect additions, removals, and content changes since the last skill review.
- When verification detects a spec change, the freshness check MUST fail until its effect on `SKILL.md` and its evaluations is reviewed.
- To pass again, the check MUST require either:
  - updates to affected `SKILL.md` guidance and evaluations; or
  - confirmation that the changed specs require no changes to `SKILL.md` or its evaluations.
- Source hashes MUST be generated from the discovered specs.
  The process MUST NOT require a manually maintained semantic inventory.
- Generated source hashes and evaluation results are evidence only.
  They MUST NOT define behavior or override a spec.
- Changes to non-authoritative notes MUST NOT by themselves make the freshness check fail.
