+++
id = "t0016"
title = "Implement the status tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "pending"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0010", "s0011", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the status tool (NEEDS APPROVAL)

After its proposed behavior in s0005 is approved, implement `worklog status` without turning it into a validator or certification mechanism.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when the command is shipped and its whole-worklog, selected-entity, path-selected, hierarchy, actionability, agent-mode, marker, tag-database, failure, and result workflows are verified.
