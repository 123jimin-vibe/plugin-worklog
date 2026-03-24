+++
id = "s0006"
title = "Workflow: Refactor"
tags = ["workflow"]
+++

# Workflow: Refactor

Restructuring without behavioral change. Flow: task → spec (if boundaries change).

## Requirements

- No observable behavioral change.
- Existing tests serve as safety net — they must pass before and after.
- If component boundaries change, the spec is updated to reflect new structure.
