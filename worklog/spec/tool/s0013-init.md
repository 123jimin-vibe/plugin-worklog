+++
id = "s0013"
title = "The init tool"
+++

# The `init` tool (UNIMPLEMENTED)

Initializes worklog for a project.

## Related specs

- s0002 defines the minimum entity structure.
- s0005 defines common tool rules.
- s0008 defines the generated project configuration.
- s0012 defines its default policies.
- s0015 defines the tag database.

## Usage

```text
worklog init [PROJECT]
```

`PROJECT` is the project directory.
It defaults to the current directory.

Running `init` means that the project has chosen to use worklog.
The command does not decide whether worklog is appropriate for the project.

## Behavior

`init` creates the minimum valid worklog structure defined by s0002.

It:

- creates the standard entity and archive directories;
- creates `worklog/project.toml` as defined by s0008 when it does not exist;
- creates `worklog/tags.csv` as defined by s0015 when it does not exist;
- writes explicit policies for specs, tasks, and notes using the default modes from s0012;
- preserves every existing worklog file;
- reports which paths it created and which already existed.

It does not:

- create specs, tasks, notes, references, or decisions;
- infer behavior from source code or project documentation;
- generate placeholder project coverage;
- initialize or modify version control;
- modify files outside `worklog/`;
- rewrite an existing `project.toml`;
- rewrite an existing valid `tags.csv`;
- rewrite entity tag values while creating `tags.csv`.

Creating semantic entities belongs to later workflow steps.
Initialization alone MUST NOT imply that the project has adequate spec coverage.

## Existing worklogs

`init` is idempotent.

When the project already has a complete worklog, it makes no changes and exits successfully.

When the project has a partial but compatible worklog, it creates only the missing standard structure.
Existing compatible files and directories are preserved.

When `tags.csv` is missing, `init` scans every current entity and archived task before writing.
It creates one normalized, alphabetically sorted row with an empty description for each distinct tag.
It creates only the header when no entity uses tags.

An existing valid `tags.csv` is used unchanged.
An existing `tags.csv` with invalid CSV structure, an empty normalized tag name, or duplicate normalized database rows prevents initialization.
A normalized duplicate within one entity also prevents initialization.
Unknown entity tags and unused database rows do not prevent initialization.

If a required path is occupied by an incompatible file or directory, `init` fails without making partial changes.
It never requires a destructive `--force` mode.

## Result

Success reports one of:

- Worklog initialized.
- Worklog structure completed.
- Worklog already initialized.

The result also identifies the project directory and the paths created.

Failure identifies each structural conflict and leaves the project unchanged.
