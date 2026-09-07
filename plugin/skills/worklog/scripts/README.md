# Worklog tools

Run with Python 3.11 or newer; no additional packages are required.
Paths below are relative to this directory in the installed plugin.

```text
python worklog.py init [PROJECT]
python worklog.py init --help
```

`PROJECT` defaults to the current directory.
Use `init` after the project has chosen to adopt worklog.
It creates missing worklog directories, project policy configuration, and the tag database, preserving existing files.
Its output identifies created and existing paths; initialization does not establish spec coverage.

Exit status is zero on success and nonzero on failure.
On failure, follow the reported remediation before retrying.
The command preflights changes and rolls back its own creations after a caught write failure.
It does not provide crash recovery or coordination with concurrent writers.
