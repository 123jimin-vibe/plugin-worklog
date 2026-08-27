+++
id = "t0004"
title = "Introduce task hierarchy"
tags = ["methodology", "tasks"]
status = "pending"
modifies = ["s0005", "s0009"]
+++

# Introduce task hierarchy (NEEDS APPROVAL)

Add an optional `child_of` task field without introducing distinct parent and child task types or explicit child lists.
A typical parent states the overall outcome and delegates implementation details to referenced children.
Clarify that the one-session expectation applies to a task's own work, not work delegated to children.
Keep `blocked_by` as an independent dependency relationship, while recommending it for children that must resolve before the parent's remaining work can proceed.
Define hierarchy validation, lifecycle, archival, and task-list reporting behavior.

Complete when the governing specs and guidance define a consistent, backwards-compatible hierarchy model.
