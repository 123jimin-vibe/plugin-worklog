+++
id = "t0023"
title = "Force in-turn artifacts in exam questions"
status = "pending"
tags = ["quality"]
modifies = ["s0014"]
+++

# Force in-turn artifacts in exam questions

Four exam questions stall in legitimate orientation (reads, next_id) and end the
turn without the artifact their grading needs: happy Q1, pitfall-governance Q2,
pitfall-spec-authoring Q3, pitfall-precedence Q4. Stalls increased after the
t0018 tools.md change sanctioning verification re-reads — s0014 already records
the constraint ("questions that want artifacts must force them in-turn; an
orientation-only turn yields no verdict") and spec-authoring Q4 already received
the treatment.

During t0022 these stalls cost clean attribution: score dips needed a dedicated
r4-control run to separate exam noise from skill changes.

## Scope

- Add forcing phrases ("write the file in this response", pre-seed the reads the
  question would otherwise spend its turn on) to the four questions above.
  Precedence Q4 additionally needs its seeded read-back extended to
  `src/recipes/models.py` (the fresh run burned its turn there).
- Re-run the touched exams once to confirm each yields a gradable artifact.
- Update the per-question comments to reflect the forced shape.
