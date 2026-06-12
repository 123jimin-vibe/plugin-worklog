+++
id = "t0025"
title = "Marker removal requires verified implementation"
status = "pending"
tags = ["methodology"]
modifies = ["s0011", "s0018"]
+++

# Marker removal requires verified implementation

Three consecutive runs (r4, c1, c2) of pitfall-spec-authoring Q6 strip all six
s0003 `UNIMPLEMENTED` markers purely on the user's verbal "collections shipped"
claim — no verification of the implementation, no surfacing of the need to
verify. The register property passes (no narration enters the body); the
marker half fails silently every time.

Root cause candidate: SKILL.md and s0011 say "remove the marker when
implemented" — testees read *implemented* as *claimed*. The archive write-back
path has the verification rule ("asserts only what the delivered work
verifiably does"); the direct spec-edit path has none.

## Scope

- Rule wording in s0011 (and SKILL.md per s0018 review trigger): removing an
  `UNIMPLEMENTED` marker outside the archive write-back requires verifying the
  implementation, or stating that verification is pending.
- Measure with spec-auth Q6 before/after — the question is already
  signal-bearing for exactly this gap.
