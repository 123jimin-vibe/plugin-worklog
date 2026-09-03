+++
id = "t0018"
title = "Implement the field tool"
tags = ["implementation", "tooling"]
parent = "t0006"
status = "pending"
modifies = ["s0002", "s0003", "s0005", "s0008", "s0009", "s0010", "s0012", "s0015"]
blocked_by = ["t0013"]
+++

# Implement the field tool (NEEDS APPROVAL)

After its proposed behavior in s0005 is approved, implement `worklog field` for supported mutable entity fields.
Build on the library foundation from t0013 and add reusable library capabilities when this tool establishes a concrete need.

Complete when `set`, `add`, `remove`, and `unset` are shipped and their type, cardinality, reference, hierarchy, dependency, tag, protected-field, batch, failure, and result workflows are verified.
