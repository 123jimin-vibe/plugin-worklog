+++
id = "s0003"
title = "Design Research & Case Studies"
tags = ["research"]
paths = ["brainstorm/**"]
+++

# Design Research & Case Studies

Design rationale, observations, prior-art research, and measurement records behind the methodology. Not part of the deliverable — and not archival either: the corpus is the sole home for unresolved design questions and for the ledger recording how the delivered artifact was compressed.

## Contents

- **Design rationale** — constraints, goals, trade-off analysis for methodology structure.
- **Agent limitations** — general LLM failure modes, most of them outside what the methodology addresses. The catalogue of pitfalls the methodology does target is a spec (s0019), not research.
- **Case studies** — observations from applying the methodology to a real project. Most record an earlier revision of the methodology rather than the current one; a case study states which revision it observed.
- **Prior art** — references on related approaches, external and internal. Internal ones include this project's own earlier revisions, which carry no authority: an idea taken from one needs independent justification.
- **Open design questions** — methodology questions raised and not settled. Nothing else records them.
- **Compression ledger** — measured rewrites of the delivered artifact: source text, candidate rewrites, token counts, and regressions (s0021).

## Relationship to Methodology

Findings reach the deliverable through a spec, never directly: research informs a spec, the spec informs SKILL.md (s0018). The compression ledger runs the other way — artifact revisions generate its entries. Research entries are refined in place; ledger entries are append-only, since a rewritten measurement is no longer a measurement.

## Anticipated Changes

- New case studies from additional projects.
- Consolidation of findings into methodology changes.
- Further compression rounds appending to the ledger.

## Proposals

- Requiring the compression ledger to carry an entry per lever in a round, so a rewrite that was never measured is distinguishable from one that was measured and kept.
- Requiring the corpus index to list every file in the corpus.
- Promoting the open design questions into s0001 Anticipated Changes, which would decide they are still live.

## Dangers

- Stale research contradicting a spec. Research never binds; the spec wins.
- Rationale recorded only in an archived task or a results file is lost (s0012). The ledger exists so compression rationale survives, and is only as complete as the rounds written into it.
