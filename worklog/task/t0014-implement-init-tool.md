+++
id = "t0014"
title = "Implement the init tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "pending"
modifies = ["s0002", "s0005", "s0008", "s0012", "s0013", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the init tool (NEEDS APPROVAL)

Implement `worklog init` according to s0013 and the common tool rules in s0005.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when the command is shipped and its new-worklog, compatible-existing-worklog, idempotent, conflict, tag-database, and no-partial-change workflows are verified.
