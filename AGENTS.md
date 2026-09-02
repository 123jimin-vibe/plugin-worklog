You're working on the main repository for the 'worklog' agent skill.

- `local/` holds local references. Git-tracked files (incl. specs, comments) must not mention anything in or referenced by `local/` without explicit user permission in the session.
- Whenever you committed a mistake, append an entry to `worklog/note/n0004-*.md`. Tool use mistakes (except worklog tools) and mistakes happend in `local/` are exceptions.
- This project's MarkDown documents use semantic line breaks, not fixed-width wrapping.
- Capitalize 'worklog' as if it's an ordinary noun (i.e. not a proper noun "Worklog").

NOTE: We're currently working on v0.2.0, which is a rework of previous revision of worklog.
New worklog should be backwards-compatible with old one.
