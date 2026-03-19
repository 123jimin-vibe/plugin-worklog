# Worklog

## Ideas

- Manage bug and work tracking in-repo.
- Documentation-driven:
  - Specs become authoritative source on program's functions.
  - Tests are generated from specs, *not* from implementations.

## Previous Attempt

## Pitfalls

- Human-readable manual/documentation is not always suitable to be used as specs.
  - Information duplication happens between documentation and spec.
- AI agents often have problems bookkeeping specs.
- Document-driven not adhered to well in practice.
- Specs must reflect latest code change, but often become out-of-sync in practice.
  - Unexpected inter-spec dependency.
  - Agents writing codes before updating spec.
- Confusion between a 'plan' and a 'spec'.
- Confusion between a 'plan' and a 'task'.

### Writing Specs is not simpler than Writing Code

- Agents (and human) tend to try to define every aspects of public APIs, including signature, ...
- Adhering to it: need to be synced (too) often when minor details are revised.
- Not adhering to it: some "non-document-driven" aspects starts happening.