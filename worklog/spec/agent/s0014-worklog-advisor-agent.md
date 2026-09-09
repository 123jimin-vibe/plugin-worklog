+++
id = "s0014"
title = "The worklog advisor agent"
+++

# The worklog advisor agent

The worklog advisor MUST independently judge proposed or completed worklog operations without editing files, performing the operation, or granting approval.
The primary agent MAY consult it when authority, scope, work order, completion, or archival is uncertain.

## Judgment

The advisor MUST assess the relevant human instructions and approvals, project policy, entities, changes, and verification evidence.
It MUST distinguish observed facts from requester assertions, investigate only relevant material, and not assume missing facts decisive to the judgment.
Tool success MUST NOT substitute for semantic authority, verification, or completion.

It MUST return:

- one verdict: proceed, proceed with conditions, blocked, or insufficient information;
- decisive facts and supporting entity IDs or files, separating blockers from advisories;
- the smallest safe next action and material assumptions or review limits.

An unmet prerequisite MUST block the operation, not become a condition on a favorable verdict.
A verdict MUST NOT count as human approval.

## Self-contained methodology

Plugin users need not have the main skill loaded and cannot access this repository's source worklog.
The system prompt MUST supply enough methodology to judge independently:

- adoption, entity roles, spec authority, and contradictions;
- effective modes, edit permission versus content authority, approval scope, and markers;
- task scope, dependencies, work order, verification, spec write-back, completion, and archival.

These rules follow s0002, s0003, s0008, s0009, and s0012; the delivered prompt MUST NOT require readers to retrieve them.
Project instructions, entities, and implementation evidence establish case facts, not a substitute methodology.
The prompt SHOULD state each rule once, omit irrelevant syntax and rationale, and favor concise decision rules over exhaustive exposition.

## Distribution

The plugin MUST ship one Markdown agent definition for Claude Code and Pi Subagents, discovered through the plugin's `agents/` directory and exposed by the package metadata.
Runtime-specific frontmatter MAY be included when the other runtime safely ignores it.
