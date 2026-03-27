# Recipe App — Worklog State

This is the current worklog state for a recipe management application.

## worklog/spec/s0001-recipe-storage.md

```
+++
id = "s0001"
title = "Recipe Storage"
tags = ["core"]
paths = ["src/recipes/**"]
+++

# Recipe Storage

Recipes are stored as structured documents with a title, ingredient list, and step-by-step instructions.

## Observable Behavior

- Users can create, read, update, and delete recipes.
- Recipes are searchable by title.
- Deleting a recipe is soft-delete (recoverable for 30 days).

## Constraints

- Recipe titles must be unique per user.
- Ingredient quantities must be positive numbers.

## Anticipated Changes

**TODO:** batch import — accept a list of recipes and store them in one operation.

- Full-text search across ingredients and instructions.
- Recipe versioning.

## Dangers

- Soft-delete retention window is a product decision — do not hardcode without confirming.
```

## worklog/spec/s0002-notifications.md

```
+++
id = "s0002"
title = "Notification System"
tags = ["infra"]
paths = ["src/notify/**"]
+++

# Notification System

Sends notifications to users when events occur (e.g., recipe shared, comment added).

## Observable Behavior

- Email notifications are sent for all event types.
- Notifications are delivered within 60 seconds of the triggering event.
- Failed sends are retried up to 3 times with exponential backoff.

## Constraints

- Users can opt out of specific event types.
- Notification content must not include sensitive data (passwords, tokens).

## Anticipated Changes

- Push notification channel.
- Per-user delivery preferences (email vs. push vs. both).

## Dangers

- Retry storms under high load — backoff parameters must be tuned.
```

## worklog/task/t0001-recipe-tagging.md

```
+++
id = "t0001"
title = "Add recipe tagging"
status = "active"
tags = ["core"]
modifies = ["s0001"]
+++

# Add recipe tagging

Users can assign tags to recipes and filter recipes by tag.

## Scope

- Add a tags field to recipes (list of strings).
- Add a search-by-tag endpoint.
- Update s0001 to document tagging behavior.
```

## worklog/task/t0002-fix-email-delivery.md

```
+++
id = "t0002"
title = "Fix email delivery bug"
status = "done"
tags = ["infra"]
modifies = ["s0002"]
+++

# Fix email delivery bug

Email notifications were silently dropped when the SMTP server returned a transient 4xx error. The retry logic only handled 5xx errors.

## Scope

- Fix retry logic to handle 4xx transient errors.
- Add logging for all delivery failures.
```

## worklog/archive/task/t0003-hotfix-rate-limiter.md

```
+++
id = "t0003"
title = "Hotfix: rate limiter bypass"
status = "done"
tags = ["infra"]
modifies = ["s0002"]
+++

# Hotfix: rate limiter bypass

The notification rate limiter could be bypassed by sending requests with spoofed user IDs. Patched in production.
```

## worklog/decision/d0001-rate-limiter-postmortem.md

```
+++
id = "d0001"
title = "Rate limiter bypass post-mortem"
status = "accepted"
tags = ["infra"]
relates_to = ["s0002"]
+++

# Rate limiter bypass post-mortem

## Context

On March 3, the notification rate limiter was bypassed via spoofed user IDs, causing a spam incident.

## Options Considered

1. Add user ID validation at the API gateway.
2. Move rate limiting to a per-session basis.
3. Both — validate IDs and add per-session limits.

## Choice

Option 3. Validate user IDs at the gateway and add per-session rate limits as defense in depth.

## Rationale

Option 1 alone leaves rate limiting bypassable through other vectors. Option 2 alone doesn't prevent spoofed IDs from consuming resources. Defense in depth addresses both.

## Consequences

- s0002 needs updating to reflect the new rate-limiting behavior.
- Gateway validation adds ~2ms latency per request.
```
