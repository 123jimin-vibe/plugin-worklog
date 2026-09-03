+++
id = "t0017"
title = "Implement the create tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "pending"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0010", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the create tool (NEEDS APPROVAL)

After its proposed behavior in s0005 is approved, implement `worklog create` for specs, tasks, and notes.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when single and batch creation, ID allocation, type-specific fields, pending task state, tag handling, effective-mode reporting, validation failure, and per-target result workflows are verified.
