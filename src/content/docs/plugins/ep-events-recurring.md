---
title: "EP Events Recurring"
description: "Recurring class and event templates for EP Events: weekly, fortnightly, and Nth-weekday series (including the last weekday of the month) that generate a rolling timetable of real events, with cover, one-off cancellations, and per-location holiday closures."
---

EP Events Recurring turns a single class or event into a **recurring series** that automatically generates real events on a rolling forward timetable. It is the keystone of the studio-management extensions: weekly, fortnightly, and Nth-weekday schedules (including "the last Wednesday of the month"), per-occurrence cover (a substitute instructor), one-off cancellations that notify booked clients, and per-location holiday closures.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

EP Events Recurring is a companion to [EP Events](/plugins/ep-events/). EP Events handles individual events with tickets, registrations, check-in and payments; EP Events Recurring adds the **timetable** on top.

You define a **series template** once (for example "Vinyasa Flow, every Wednesday at 6pm"), and the plugin generates real EP Events occurrences forward over a rolling horizon. Each generated occurrence is an ordinary event, so it inherits everything EP Events does: tickets, registrations, check-in, payments, and the `[events]` listing.

What you get:

1. **Recurring series** — weekly, fortnightly, or Nth-weekday (1st / 2nd / 3rd / 4th / **Last** weekday of the month).
2. **A rolling forward timetable** — occurrences are generated ahead over a horizon you set in weeks, and topped up automatically over time.
3. **Cover (substitutions)** — assign a substitute instructor to a single occurrence without disturbing the rest of the series.
4. **One-off cancellations** — cancel a single occurrence; booked clients are notified, and you can restore it later.
5. **Holiday closures** — per-location closed dates. Generation skips them, and if you add a closure over an already-booked class, that class is cancelled and its clients are notified.

## Requirements

- **PageMotor 0.8.3 or later**
- **EP Events 1.0.23 or later** (this plugin extends it)
- **EP Suite base class** (bundled)

## Installation

EP Events Recurring installs like any PageMotor plugin.

1. **Download** `ep-events-recurring.zip` from your ElmsPark account.
2. **Sign in to your PageMotor admin** at `yourdomain.com/admin/`.
3. **Go to Plugins**, then **Upload a New Plugin** and drop the zip.
4. **Activate** it in your active Theme. It needs EP Events, which should already be installed and active.

## The Schedule Builder

Open **Plugins**, then **Plugin Settings**, then **EP Events Recurring**. The **Schedule Builder** is where you create and manage series.

To add a series, fill in:

- **Class name** and **class type**
- **Frequency** — `weekly`, `fortnightly`, or `nth_weekday`
- **Position** (for `nth_weekday`) — 1st / 2nd / 3rd / 4th / **Last**
- **Days** — one or more weekdays
- **Start time** (local) and **duration**
- **Timezone**
- **Location** (an EP Locations venue) or a free-text room
- **Instructor name** and **capacity**
- **Horizon (weeks)** — how far ahead to generate
- **Series start** and an optional **series end**

Save and the plugin generates the forward occurrences immediately. You can **Dry-run** a series to preview what it would generate, or **Regenerate** it at any time.

### Last weekday of the month

Set **Frequency** to `nth_weekday` and **Position** to **Last** to schedule the genuine last occurrence of that weekday each month. This is not the same as picking "4th": the 4th misses any month that has five of that weekday. "Last Wednesday", for example, lands on the 24th in a four-Wednesday month but rolls to the 29th or 30th in a five-Wednesday month.

## Cover and cancellations

From a series' occurrence list you can:

- **Assign cover** — set a substitute instructor on a single date. The series and every other date are left untouched.
- **Cancel** a single occurrence — booked clients are notified and the date drops off the timetable. You can **restore** it later.

Manual edits to a single occurrence (its time, instructor, and so on) are protected: regenerating the series does not overwrite them.

## Holiday closures

The **Holiday Closures** panel holds per-location closed dates (bank holidays, refurbishments, and the like). Generation skips any date inside a closure. If you add a closure over a date that already has a booked class, that class is cancelled and its clients are notified.

## How occurrences appear

Generated occurrences are ordinary EP Events events, so they appear wherever EP Events content does — the `[events]` listing, individual event pages, registration, and check-in. EP Events Recurring has no public shortcodes of its own; it is the admin-side engine that feeds EP Events.

## Notes

- The forward timetable is topped up automatically on a schedule, so the horizon stays full as time passes (the same cron triggers EP Events uses).
- An AI assistant or automation can create a series through the `series_create` API action / MCP tool, including `nth: -1` for the last weekday of the month.

## Feedback

EP Events Recurring is in active development. Bug reports, feature requests, and notes on rough edges are welcome via the **Send feedback** link at the bottom of the plugin's settings page, or by emailing ElmsPark.
