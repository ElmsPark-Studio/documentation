---
title: "EP Scheduled Content"
description: "Schedule draft pages and posts for automatic publication at a future date and time. No manual intervention needed."
sidebar:
  order: 47
---

EP Scheduled Content lets you write a page or post as a draft, set a publish date and time, then walk away. When the scheduled time arrives, the content goes live automatically.

Published by [ElmsPark Studio](https://elmspark.com).

## Use cases

- **Seasonal content.** Write your "Black Friday sale" page in October, schedule for November.
- **Editorial calendar.** Queue a week's worth of blog posts; publish one per weekday at 9am.
- **Coordinated launches.** Product, blog post, and landing page all go live at the same moment.
- **Time-shifted publishing.** Write when you're free, publish when your audience is online.

## How it works

1. Create a new page or post as normal.
2. Set its status to **Scheduled**.
3. Set **Publish date and time** to a future moment.
4. Save as draft.
5. At the scheduled moment, the plugin flips status to Published.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**
- **A functional PageMotor scheduler** (this plugin piggybacks on PM's built-in cron).

## Installation

1. Download `ep-scheduled-content.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. The **Scheduled** status option appears on every page's content options.

## Settings

- **Check interval.** How often to check for due scheduled items. 5 minutes (default), 15, or 60.
- **Notification on publish.** Optionally email admin when a scheduled item goes live, as a sanity check.

## The scheduled queue

A dashboard view lists every currently-scheduled item with its publish date. You can:

- **Edit** to change the scheduled time.
- **Publish now** to override the schedule and go live immediately.
- **Cancel** to revert to draft.

## Timezone

Publish times are stored in the site's configured timezone (PageMotor settings → timezone). If your timezone and your audience's timezone differ, schedule with your audience in mind.

## Troubleshooting

### "Scheduled items aren't publishing"

PageMotor's scheduler needs to be working. Check `cron` is running on your server. A common cause of unreliable scheduling is disabled cron on shared hosting.

### "Items publish hours later than scheduled"

The check interval determines how precise the timing is. With the 60-minute check interval, an item scheduled for 9:00am might not publish until 9:59am. Reduce the interval to 5 or 15 minutes for tighter timing.

### "I scheduled for next week, the item is already live"

Check the date was saved correctly. Timezone confusion is the usual cause.

### "I want to schedule an unpublish (retract) too"

Not currently supported. Auto-unpublish is a separate feature request in the review queue.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
