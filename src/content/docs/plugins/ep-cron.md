---
title: "EP Cron"
description: "One secure, observable background-task scheduler for the EP Suite. A single secret heartbeat drains every due task exactly once, with a Background Tasks screen that shows the heartbeat and every task's last result. Replaces the per-plugin cron URLs."
---

EP Cron is the background-task scheduler for the EP Suite. Instead of every plugin carrying its own `?ep_*_cron=` URL, you point one cron job at a single secret heartbeat and EP Cron drains every due task across every EP plugin, exactly once. A Background Tasks screen shows you the heartbeat, every registered task, its schedule, and its last result, so a silent cron failure becomes something you can see.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **One heartbeat for the whole suite.** A single secret URL replaces the per-plugin `?ep_*_cron=` endpoints. Point one system cron (or your host's scheduler) at it.
- **Exactly-once.** Every due task runs under a run-level lock and a per-task atomic claim with a fencing token, so a task can never double-run even if two triggers fire at once. This matters most for tasks that move money or send mail.
- **Observable.** The Background Tasks screen lists every registered task with its schedule, status, last run, last result, and run count, plus the heartbeat's freshness. A stalled cron shows up as a stale heartbeat instead of staying invisible.
- **Self-healing schedule.** A crashed or timed-out task is reaped and re-queued; a task whose owning plugin is deactivated is pruned automatically.
- **Backoff on failure.** A failing task retries with exponential backoff and full jitter, and dead-letters after its maximum attempts rather than hammering forever.
- **A registry for plugin authors.** Any EP plugin registers a recurring task in one line; EP Cron owns the scheduling and the exactly-once guarantee.

## Requirements

- **PageMotor 0.8b or later** (the heartbeat and Background Tasks screen; the API and MCP actions are feature-detected on newer cores).
- **EP Suite base class.**

EP Cron is optional for every other EP plugin: without it, each plugin keeps its own cron endpoint. With it active, those plugins register their work centrally and run off the one heartbeat.

## Installation

1. Download `ep-cron.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-cron).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Cron** and copy your heartbeat URL (below).

## The heartbeat

EP Cron does its work when an external cron calls one secret URL:

```
https://your-site.com/?ep_cron_run=<secret>
```

The secret is generated once and checked with a timing-safe compare; a wrong or missing token returns HTTP 403 and does no work. The ready-made URL is on the EP Cron settings screen. Point a system cron job or uptime monitor at it, every five minutes:

```
*/5 * * * * curl -s "https://your-site.com/?ep_cron_run=<secret>" >/dev/null 2>&1
```

Each beat takes a non-blocking run-level lock, so two overlapping beats cannot both drain the queue; the second simply bails. Keep the URL private (anyone with it can trigger a run, though it exposes no data).

## The Background Tasks screen

The settings screen is a live dashboard:

- **Heartbeat status.** Green when it last beat within the expected window, amber when stale, red when it has not beaten at all (your cron is not wired up).
- **Task table.** Every registered task with its owner plugin, schedule, status, last run, last result, and total runs.
- **Run now.** Force one task to run immediately.
- **Test now.** Record a heartbeat by hand to confirm the plumbing.
- **Regenerate secret.** Rotate the heartbeat URL. The old URL stops working immediately, so update wherever your cron runs.

## Settings

- **Log retention.** How long to keep the run history (7, 14, 30, or 90 days).
- **Pause all background tasks.** The heartbeat keeps beating but no task runs. Use it during maintenance. A consumer that respects the pause (EP Newsletter does) holds its work until you unpause.

## For plugin authors

A plugin registers a recurring task in its `construct()`, guarded so it is a no-op when EP Cron is not installed:

```php
if (class_exists('EP_Cron_Registry')) {
    EP_Cron_Registry::schedule(
        'my-plugin-task',                 // globally-unique key, prefixed with your plugin
        EP_Cron_Registry::EVERY_5_MIN,    // interval (named constants, floored at 60s)
        array($this, 'run_my_task'),      // handler: no args, returns an array (or throws)
        array('label' => 'My plugin — what this does')
    );
}
```

The handler runs only when due, and only ever once per due window. EP Cron has already taken the lock and claimed the job before it calls you, so the handler just does its (chunked) work and returns a summary array. Throw to signal failure and trigger backoff. Named intervals run from `EVERY_MINUTE` to `DAILY`.

EP Newsletter 1.4.1 is the first plugin to move onto EP Cron: its queue registers as `ep-newsletter-queue` and runs off the one heartbeat. See [EP Newsletter](/plugins/ep-newsletter/).

## Troubleshooting

### "The heartbeat is red / no tasks are running"

Your cron is not calling the URL. Confirm the cron line is installed (`crontab -l`), the URL and secret are exactly as shown on the settings screen, and that a manual `curl` of the URL returns a JSON run-report rather than 403 (wrong secret) or an error.

### "A task shows as dead"

It failed its maximum attempts and was dead-lettered. Check its last error on the Background Tasks screen, fix the underlying cause, then **Run now** to retry it.

### "I rotated the secret and now nothing runs"

Regenerating the secret changes the URL. Update your cron job to the new URL shown on the settings screen.

### "Tasks stopped after I ticked Pause all"

That is what it does. Untick **Pause all background tasks** to resume.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
