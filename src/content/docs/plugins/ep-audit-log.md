---
title: "EP Audit Log"
description: "Activity log for PageMotor. Tracks content changes, user registrations, and logins via passive database observation, with a public log API for other plugins."
sidebar:
  order: 8
---

EP Audit Log is a simple activity log. It watches your database for changes to content, users, and logins and records what happened, when, and by whom. Other plugins can also record their own events through a public API.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Three event sources:

- **Content changes.** Pages created, edited, deleted.
- **User events.** Registrations, logins, password resets.
- **Plugin events.** Anything another EP Suite plugin chooses to log, via a static API.

The plugin works by observing the database every 30 seconds rather than hooking into every content save. This keeps it cheap to run and captures events from any code path that writes to the content tables, including direct SQL, API calls, and admin edits alike.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-audit-log.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**.
3. Activate. Logging starts immediately.

## Settings

| Setting | Purpose |
|---|---|
| **Retention** | How long to keep log entries. Choose 30, 60, 90, 180, 365 days, or **Forever**. Default 90. |
| **Status cards** | Dashboard shows total events and today's events, no setting needed. |

## The log viewer

The settings page shows the 100 most recent events in a colour-coded table:

- **Green** for content creation and user registration
- **Blue** for updates, logins, and general activity
- **Red** for deletions and failed logins

Each row shows timestamp, actor (user ID or "system"), event type, and a short description.

## Logging custom events from another plugin

```php
EP_Audit_Log::log([
    'event'       => 'custom_event',
    'description' => 'Something notable happened',
    'user_id'     => $motor->user->id ?? 0,
    'metadata'    => ['key' => 'value'],
]);
```

The `metadata` field is free-form JSON stored alongside the entry. Use it for details the log viewer can't display natively.

## Retention and pruning

Entries older than your configured retention are deleted automatically during a daily cleanup. On a site with heavy activity, this keeps the table at a sensible size. If you need audit records for longer than a year, pick **Forever** and budget for a large table.

## Troubleshooting

### "Events appear in the log up to 30 seconds after they happen"

That's the observation throttle. The plugin runs its database scan at most every 30 seconds. If you need real-time audit, use `EP_Audit_Log::log()` directly from your event source.

### "Failed logins don't appear"

Failed logins are not currently tracked by the automatic observer — only successful ones. If you need them, log them explicitly from your auth code via the static `log()` method.

### "I cleared the log but it looks like entries are coming back"

The log is cleared with a SQL `TRUNCATE`, but as soon as anyone creates or edits content, the next 30-second scan captures that and logs it. That is working as intended.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
