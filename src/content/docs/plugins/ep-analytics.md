---
title: "EP Analytics"
description: "Privacy-respecting page view analytics for PageMotor. Server-side tracking with no cookies, no JavaScript pixel, no external services, no GDPR consent required."
sidebar:
  order: 6
---

EP Analytics gives you a real analytics dashboard for your PageMotor site with none of the privacy baggage. No cookies, no JavaScript tracking pixel, no third-party scripts, no data leaving your server. Your visitors don't need to click a consent banner because there is nothing to consent to.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Page views are recorded server-side during `register_shutdown_function()`, which runs after the response has already been sent to the browser. Tracking adds **zero latency** to your pages.

Data storage:

- **Hourly granularity for the last 7 days.** Drill into any day's 24-hour breakdown.
- **Daily aggregates for anything older.** Auto-rollup runs nightly.
- **Configurable retention** from 30 days to forever.

What you see in the dashboard:

- Bar chart with **Today**, **7 Days**, **30 Days**, **90 Days** tabs
- Top 10 pages with real page titles (resolved from the content database)
- Top 10 referrers (self-referrals filtered out)
- All-time, period, and today's view count cards
- AJAX tab switching so nothing reloads

What EP Analytics does NOT do:

- No user identification. No unique visitor count. It is a counter, not a behaviour tracker.
- No session tracking. A visitor viewing five pages counts as five views, not one session.
- No event tracking. No click maps, no scroll depth, no form analytics.
- No geography. No IP-to-country lookup.

If any of those matter to you, EP Analytics is not enough. If none of them matter (and for most sites they don't), EP Analytics is all you need.

## Requirements

- **PageMotor 0.8.2b or later**

That's it. No external service accounts, no JavaScript SDK, no Google tag manager.

## Installation

1. **Download** `ep-analytics.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**.
3. Activate. Tracking starts immediately.

Open the settings page to confirm. You should see status cards with zero counts and a prompt to revisit once data accumulates.

## Settings

### Tracking

- **Enable tracking.** On by default. Turn off temporarily if you need.
- **IP exclusion list.** Comma-separated IP addresses to never record. Use this to exclude your own IP and any known bot sources. Supports CIDR (`192.168.1.0/24`).

### Data retention

- **Keep data for:** 30, 60, 90, 180, 365 days, or **Forever**. Expired data is deleted during the nightly cleanup.
- Hourly-level data is kept for the most recent 7 days regardless of this setting. After 7 days, hourly rows are rolled up into a single daily row to keep the database lean.

### Bot filtering

EP Analytics automatically ignores page views from user-agents that look like bots. The blocklist covers 40+ patterns across:

- Search engine crawlers (Googlebot, Bingbot, DuckDuckBot, Yandex)
- AI scrapers (GPTBot, ClaudeBot, Bytespider, CCBot)
- Social previews (Twitterbot, facebookexternalhit, LinkedInBot, WhatsApp, Slackbot)
- Monitoring tools (UptimeRobot, Pingdom, StatusCake)
- Generic crawlers (`bot`, `spider`, `crawler`, `scraper` in the UA)

Legitimate visitors almost never match these patterns. If you spot false positives, log them in your review queue.

## Dashboard usage

### The Today tab

Bar chart of the last 24 hours, split into hourly buckets. Most recent hour is on the right. Each bar is clickable for that hour's top pages (if you hover).

### The 7 Days tab

Daily bars for the last 7 days. **Click any bar to drill into that day's 24-hour breakdown**, then use the **Back** button to return to the overview.

### The 30 / 90 Days tab

Daily bars for the period. No hourly drill-down because hourly data is only retained for 7 days.

### Top pages

Table of the 10 most-viewed pages in the selected period. Page titles resolve from PageMotor's content tables, so you see `/about-us/` as "About us" rather than just a URL.

### Top referrers

Table of the 10 domains that sent the most traffic. Direct visits (no referrer) are not counted. Self-referrals (anyone coming from your own site) are excluded.

## How tracking works

Every page request triggers a single database write during shutdown:

1. Check that tracking is enabled.
2. Check that the page is a real page (not an admin page, not an error page, not an asset).
3. Check the user-agent against the bot blocklist. Bots get skipped.
4. Check the client IP against the exclusion list. Excluded IPs get skipped.
5. Increment the hourly counter for this URL path and this hour.
6. Record the referrer domain (if present and not self-referral).

The database write happens AFTER `flush()` has sent the response, so the visitor never waits for it.

## Data management

- **Automatic cleanup** runs nightly (piggybacks on PageMotor's scheduler).
- **Hourly-to-daily rollup** during cleanup for rows older than 7 days.
- **Manual Clear All** button in settings, CSRF-protected. Wipes everything. No undo.

## Comparing to Google Analytics

| Feature | EP Analytics | GA4 |
|---|---|---|
| Server-side | Yes | No (JS pixel) |
| Cookies | None | Yes |
| Requires consent | No | Yes, everywhere in Europe |
| External service | None | Google |
| Unique visitor count | No | Yes |
| Session tracking | No | Yes |
| Event tracking | No | Yes |
| Geography | No | Yes |
| Data ownership | Your server | Google's servers |
| GDPR paperwork | None | Full DPA chain |

EP Analytics is the better choice when you need page view numbers and nothing else. Many sites discover they never needed the rest.

## Troubleshooting

### "No data is showing up after I installed"

Wait a few minutes and reload. First-load wait is normal. If you still see zeros after an hour:

- Is tracking actually enabled in settings? Toggle it off and on.
- Is your IP in the exclusion list? Check.
- Are you testing from a machine running an ad-blocker that identifies as a bot? Unlikely, but possible.

### "My own visits are being counted"

Add your IP to the exclusion list. Find your IP at [ifconfig.me](https://ifconfig.me).

### "I see bot traffic getting through"

Some bots are new and not yet in the blocklist. Log the offending user-agent in your review queue; bot patterns can be extended.

### "The Today tab shows fewer views than the 7 Days tab for today"

This is not a bug. Today data comes from hourly buckets. The 7-day bar for today is the sum of today's hourly buckets. They should match. If they don't, check whether your server clock is in the timezone you expect.

### "Dashboard loads slowly on a site with millions of page views"

Top pages and referrers queries aggregate at read time. On very large datasets this can be slow. Dropping retention from **Forever** to 180 or 365 days usually fixes it.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
