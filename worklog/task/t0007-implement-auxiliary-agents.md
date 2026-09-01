+++
id = "t0007"
title = "Implement the full auxiliary agent set"
tags = ["agents", "implementation"]
status = "pending"
modifies = ["s0007"]
+++

# Implement the full auxiliary agent set

Implement every auxiliary agent defined by s0007 after its role is specified.

Complete when all defined auxiliary agents are shipped and their intended workflows are verified.

## Inputs from t0009 (NEEDS APPROVAL)

Before s0007 establishes an auxiliary agent as the primary provider for an n0005 unit, it must define:

- the condition that should trigger the agent;
- the minimum governing entities and project evidence it receives;
- its authority and approval boundary;
- the decisions and artifact changes it may make; and
- the evidence, uncertainty, findings, and required follow-up returned to the primary agent.

Candidate bounded roles from n0005 are spec authoring and review, investigation or audit, bug-fix and refactor review, non-successful task disposition, completion verification, and comment-quality auditing.
Ordinary Worklog use should not require delegation when the primary agent already has enough context to act reliably.
