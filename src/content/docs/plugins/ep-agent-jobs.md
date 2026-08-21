---
title: "EP Agent Jobs"
description: "Scheduled AI agent runs that live on your PageMotor site instead of a laptop. Define a job — schedule, prompt, model, tools, delivery channel, budget — and the site runs it on time and delivers the result."
---

EP Agent Jobs runs AI agents on a schedule, from your site, whether or not anyone is at a computer. You define a job — when it runs, what to ask, which model, what it is allowed to touch, where the answer goes, and what it may cost — and the site takes it from there.

It rides the [EP Cron](/plugins/ep-cron/) heartbeat, so it needs no visitor traffic to fire and nothing stops when you close your laptop.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Use cases:

- **A Monday morning digest.** Summarise last week's bookings or orders and email it before you sit down.
- **A watchdog.** Check something daily and only speak up when it looks wrong.
- **A recurring content chore.** Draft the thing you rewrite every month, ready for editing rather than starting blank.

## How it works

1. You create a job: schedule, timezone, prompt, model, allowed site actions, delivery channel and monthly budget.
2. The EP Cron heartbeat wakes the scheduler and asks which jobs are due.
3. Due jobs run, up to the per-heartbeat limit and the wall-clock limit per run.
4. The result is delivered by email, Telegram or Buzz.
5. The run is recorded, with history kept for as long as you choose.

## Requirements

- **PageMotor 0.9 or later**
- **EP Cron**, providing the heartbeat that drives the scheduler
- **EP Suite base class** (bundled with the plugin)
- **An Anthropic API key**, and credentials for whichever delivery channel you use

## Installation

1. Install and configure EP Cron first, and confirm its heartbeat is actually arriving. A scheduler with no heartbeat is silent rather than noisy — nothing runs and nothing complains.
2. `ep-agent-jobs.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP Agent Jobs**.

## Settings

| Setting | What it does |
| --- | --- |
| **What site actions may an agent run?** | The ceiling on what any job can do to your site. Set this deliberately; it is the main safety control. |
| **Default email recipient** | Where results go when a job does not name someone else. |
| **Telegram chat ID** / **Buzz channel, relay URL, room** | Credentials for the non-email delivery channels. |
| **Default timezone for new jobs** | So "9am" means what you expect. Each job can override it. |
| **Jobs per heartbeat** | How many due jobs may start per beat. Keeps a backlog from stampeding. |
| **Wall-clock limit per run** | Caps a single run that would otherwise hang. |
| **Keep run history for** | How long finished runs are retained. |
| **Pause all agent jobs** | A single stop switch for every job at once. |

### The action ceiling is the setting that matters

"What site actions may an agent run?" decides what an agent is permitted to do, not merely what you meant it to do. A prompt is not a permission boundary: an agent that misreads its instructions is still limited by this setting and by nothing else. Start restrictive and widen only when a job genuinely needs it.

## Budgets

Each job carries a monthly budget, and the settings page shows the month's spend so far. A job that has spent its budget stops rather than continuing quietly, which is the behaviour you want from something that runs unattended.

## Troubleshooting

**Nothing ever runs.** Almost always the heartbeat. Check EP Cron is active and its last heartbeat is recent; the plugin's dashboard card reports a missing or stale pulse rather than assuming one.

**Jobs run at the wrong time.** Check the job's timezone rather than the default, and remember that the schedule is evaluated when a heartbeat arrives, so a sparse heartbeat makes every job late.

**A job stopped mid-month.** Check its budget and the wall-clock limit before assuming a failure.

## Changelog

### 0.1.2

PageMotor 0.11 hardening for the job action ceiling. Scheduled runs inject a token whose access tier comes from the action-ceiling setting, stored using the old `read-only` name. PageMotor 0.11 renamed that floor tier to `open` with no alias, and although 0.11 fails closed by coercing an unrecognised tier to `open`, jobs were working by coercion rather than by contract.

The dispatcher now reads the running core's actual tier ladder and translates the stored name when the core uses the new vocabulary, rather than comparing version strings. Behaviour is identical on both cores and your stored settings are untouched.

### 0.1.1

Dashboard card readiness. The status pill now reads the real heartbeat timestamp rather than merely confirming the cron class loaded, so it shows red when no heartbeat has arrived and amber when one is stale.
