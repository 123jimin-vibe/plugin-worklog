+++
id = "t0004"
title = "Reduce spec verbosity"
tags = ["methodology"]
status = "pending"
modifies = ["s0011", "s0012", "s0013"]
+++

# Reduce spec verbosity

Current specs are too verbose. Need to make them slimmer without losing essential information.

TODO: exact methodology for slimming is TBD. Possible directions:

- Factor repeated patterns (frontmatter conventions, relationship model, forward-only rule) into s0001 and reference by ID instead of restating.
- Remove sections that restate what's already in SKILL.md.
- Compress tables and prose that could be terser.
- Identify which sections are load-bearing vs. padding.
