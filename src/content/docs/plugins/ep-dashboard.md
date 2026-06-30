---
title: "EP Dashboard"
description: "A branded command centre for the PageMotor 0.10 admin dashboard. Aggregates the health of your active EP Suite plugins into one screen: background-task heartbeat, newsletter audience and campaigns, and your active plugin set."
---

EP Dashboard fills PageMotor 0.10's native admin dashboard with a branded EP Suite command centre. It gathers the state of whichever EP plugins you have active into one screen: your background-task heartbeat from EP Cron, your audience and campaign figures from EP Newsletter, and the EP plugins running on the site. The panels light up on their own as you activate more EP plugins.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Native to PM 0.10.** PageMotor 0.10 added a real admin dashboard; EP Dashboard is the EP Suite's panel set for it, in the EP Suite house style.
- **Background Tasks panel.** EP Cron's heartbeat (beating, stale, or down), and a count of registered, overdue, and dead tasks, with the live task table.
- **Audience & Campaigns panel.** EP Newsletter's subscriber and campaign figures: total on file, active, pending, campaigns, sent in the last seven days, and the last campaign.
- **Your EP Suite panel.** The EP plugins currently active, so you can see your suite at a glance.
- **Self-assembling.** Each panel only appears when the plugin that feeds it is active. Activate more EP plugins and the relevant panels appear; there is nothing to configure.

## Requirements

- **PageMotor 0.10b or later** (it renders into the 0.10 admin dashboard).
- **EP Suite base class.**

The panels are populated by other EP plugins. With **EP Cron** active you get the background-tasks panel; with **EP Newsletter** active you get the audience and campaigns panel. EP Dashboard works on its own too, showing your active EP plugins.

## Installation

1. Download `ep-dashboard.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open your PageMotor admin dashboard. The EP Suite Command Centre renders at the top.

## The panels

### Background Tasks (from EP Cron)

The heartbeat status pill, a count of tasks, overdue tasks, and dead tasks, and a table of every registered task with its schedule and last result. It is a read-only summary of the [EP Cron](/plugins/ep-cron/) Background Tasks screen, surfaced where you land when you log in.

### Audience & Campaigns (from EP Newsletter)

Total subscribers on file, with active and pending counts, the number of campaigns, the count sent in the last seven days, and the last campaign sent. A quick read on your list and recent sending. See [EP Newsletter](/plugins/ep-newsletter/).

### Your EP Suite

The EP plugins active on the site, as a set of chips, with a note that panels appear automatically as you turn on more.

## How it extends

EP Dashboard reads from the EP plugins you have active and renders a panel for each one it recognises. There is nothing to configure: install an EP plugin that EP Dashboard knows about, and its panel appears on the dashboard the next time you load it. As more EP plugins gain dashboard panels, they show up here automatically.

## Troubleshooting

### "I don't see the dashboard"

EP Dashboard renders into the PageMotor 0.10 admin dashboard. Confirm you are on PageMotor 0.10b or later and that EP Dashboard is active. The Command Centre renders at the top of the admin landing page.

### "A panel I expected isn't there"

Each panel needs its source plugin active. No background-tasks panel means EP Cron is not active; no audience panel means EP Newsletter is not active. Activate the plugin and reload the dashboard.

### "The heartbeat panel says stale or down"

That is EP Cron reporting its own health, not a dashboard fault. See [EP Cron](/plugins/ep-cron/) troubleshooting: your cron job probably is not calling the heartbeat.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
