+++
id = "t0028"
title = "Drift write-back and SKILL.old.md removal"
status = "done"
tags = ["methodology", "quality"]
modifies = ["s0003", "s0010", "s0013", "s0014", "s0015", "s0017", "s0018", "s0021"]
priority = 0
+++

# Drift write-back and SKILL.old.md removal

`drift.py` reports four drifted specs (s0003, s0014, s0017, s0018). The
compression campaign (t0022, t0024, t0025, t0026, t0027) shipped four SKILL.md
revisions; t0026 and t0027 declared `modifies = ["s0018"]` and never wrote back,
and t0026 edited s0021 without it in `modifies`. Two more specs contradict
reality without showing drift because they carry no `paths` (s0015, s0021).

`plugin/skills/worklog/SKILL.old.md` is the v1 artifact, superseded at e05c3cd.

## Scope

Descriptive write-back only. Reality is the authority for what the specs say;
no rule is added, tightened, or retired.

- s0018 — record the register conventions the artifact now follows (no
  emphasis, telegraphic, ASCII connectives, numbered pipelines), complete the
  Spec/Scripts subsection inventories, add the revision verification protocol
  (probe gate, exam suite against stored baselines, per-lever attribution and
  revert), add the missing source and update triggers.
- s0021 — record the compression levers and gates applied across four rounds
  but never written down. Fix the spec's own unicode connectives against its
  tokenizer danger, and its concrete file paths against s0011 Forbidden.
- s0014 — the artifact under exam is SKILL.md, not a spec, and five of six
  exams deliver it in the conversation body; record the results pipeline the
  ignore rules and the comparison ledger encode; correct the drift-technique
  claims their own lab notes refute and the severity claim s0019 refutes.
- s0017 — the suite invokes scripts as subprocesses and loads library modules
  through a shared loader; the spec still prints per-file `importlib`
  boilerplate. Replace the pasted code with the contracts.
- s0003 — the pitfall-catalog description drifted onto s0019; the corpus holds
  a compression ledger written from SKILL.md revisions and two unresolved
  design questions, so it is not purely background.
- s0015 — tag validation shipped in `validate.py`; retire the Anticipated
  Change. s0010 gains the observable consequence of a worklog with no index:
  the tag check is skipped, not failed.
- s0013 — Required Creation binds one case while s0009 makes a hotfix
  post-mortem mandatory and forbids omitting it. Recorded, not resolved.
- Delete SKILL.old.md and the five dangling exam references to it.

## Out of scope

Divergences whose fix would add, retire, or reverse a binding rule. Recorded as
Proposals in the specs they belong to, or carried by a follow-up task.

## Verification

`validate.py` clean, test suite green, and every spec claim traced to a file in
the working tree before archiving.

## Outcome

- Eight specs written back; every changed sentence traced to a file in the
  working tree. No rule added, tightened, or retired.
- SKILL.old.md deleted (`git rm`); the five `# Also test:` comments pointing at
  it removed from the exam configs. Deletion audited first: every rule,
  constraint, forbidden item and marker in its 158 lines is either present in
  the current SKILL.md, held by a spec, obsolete (`worklog/script/`, TODO
  markers, decision `status`, "Never archived", "Chore rarely touches specs",
  "scripts not yet implemented"), or preserved in `brainstorm/`. Sole
  unpreserved fragment: the "skip decision records for tooling, config, and
  dependency choices" example, whose generalization survives in s0013 —
  removed at e05c3cd, long before the compression campaign.
- SKILL.md itself unchanged. The self-containment gaps found (tag index never
  propagated, decision creation triggers dropped, cold-reader rule never
  propagated, deliver clause with no spec home) all require an exam-gated
  revision; t0026 forbids unmeasured tail-end edits. Carried by t0029.
- Follow-up: t0029 (spec/SKILL.md rule divergence, approval-gated). Proposals
  filed in s0003, s0013, s0014, s0018. `parent` in s0011 frontmatter remains
  declared but unused by any entity or script — left as found.
- Verified: `validate.py` clean; 142 tests pass under `unittest discover`; all
  six exam configs still parse and every one resolves the artifact to SKILL.md.
