+++
id = "t0019"
title = "Implement the task tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "pending"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0012"]
blocked_by = ["t0013"]
+++

# Implement the task tool (NEEDS APPROVAL)

After its proposed behavior in s0005 is approved, implement `worklog task` for task lifecycle transitions and atomic closure.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when `start`, `block`, `resume`, `finish`, and `cancel` are shipped and their transition, dependency, close-out, atomic archival, already-resolved, batch, failure, and result workflows are verified.
