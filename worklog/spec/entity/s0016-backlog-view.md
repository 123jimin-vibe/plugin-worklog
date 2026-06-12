+++
id = "s0016"
title = "Backlog View"
tags = ["entity", "methodology"]
+++

# Backlog View

A generated, unified priority view over outstanding work: open tasks and `UNIMPLEMENTED` spec items. Computed on demand by `backlog.py` (s0010). No index file exists — persisting the view would recreate the drift the mechanism removes (d0002).

## Priority

- Priority is stored only in task frontmatter: optional `priority`, a non-negative integer, 0 most urgent (s0012). A task without `priority` is untriaged.
- An `UNIMPLEMENTED` item is triaged by covering it: an open task whose `modifies` includes the item's spec and which carries `priority`. The item inherits the lowest priority among its covering open tasks.
- Open task statuses: `pending`, `active`, `blocked`. Terminal tasks (`done`, `cancelled`) and archived tasks never contribute or appear.

## Marker Convention

A bare `UNIMPLEMENTED` token in a spec body marks the item on its line. A backticked occurrence is a mention, not a marker — meta-prose about markers backticks the word; real markers do not.

## View

- **Triaged** — tasks carrying `priority` and markers with covering prioritized tasks, ranked ascending by priority.
- **Untriaged** — open tasks without `priority`, then markers without a covering prioritized open task. Covering unprioritized tasks are still listed beside their markers for context.

## Constraints

- The view is computed, never written to a file.
- Triage state never lives in spec bodies — spec edits reset the drift watermark (s0010 Dangers).

## Anticipated Changes

- Per-marker task coverage if spec-level granularity proves insufficient.
- Validation that `priority` values stay within a project-agreed band.

## Dangers

- An unbackticked mention of `UNIMPLEMENTED` in prose reads as a real item and produces a phantom entry. Keep meta-prose backticked.
- Spec-level inheritance can overstate coverage: one prioritized task lifts every marker in its spec, including markers it does not address.
