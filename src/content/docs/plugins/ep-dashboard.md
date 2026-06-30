---
title: "EP Dashboard"
description: "A branded Command Centre for the PageMotor 0.10 admin dashboard. Every active EP Suite plugin contributes its own panel: shop takings, background-task heartbeat, newsletter audience, email deliverability, site traffic, SEO health, events, and your active plugin set."
---

EP Dashboard fills PageMotor 0.10's native admin dashboard with a branded EP Suite Command Centre. Every EP plugin you have active contributes its own panel, so the screen you land on at login shows the health of your whole suite at a glance: shop takings, background-task heartbeat, newsletter audience, email deliverability, site traffic, SEO health, upcoming events, and the EP plugins running on the site. The panels assemble themselves — activate more EP plugins and their panels appear, in priority order, with nothing to configure.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Native to PM 0.10.** PageMotor 0.10 added a real admin dashboard; EP Dashboard is the EP Suite's Command Centre for it, in the EP Suite house style.
- **Every plugin brings its own panel.** EP Dashboard asks each active EP plugin for a panel and renders whatever it returns. The plugin owns its panel, so the figures are always the plugin's own and current, never a stale copy held by the dashboard.
- **Self-assembling, priority-ordered.** A panel appears only when its plugin is active, and the panels sort into a sensible order (shop first, your active-plugin set last). There is nothing to configure.
- **One glance.** Revenue, sends, traffic, deliverability, task heartbeat and SEO health, on the screen you see when you log in.

## Requirements

- **PageMotor 0.10b or later** (it renders into the 0.10 admin dashboard).
- **EP Suite base class.**

EP Dashboard works on its own, showing your active EP plugins as a set of chips. The data panels are contributed by the other EP plugins: activate EP Ecommerce, EP Cron, EP Newsletter, EP Email, EP Analytics, EP SEO, EP IndexNow or EP Events and each one adds its panel.

## Installation

1. Download `ep-dashboard.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open your PageMotor admin dashboard. The EP Suite Command Centre renders at the top.

## The panels

Each panel is provided by the plugin named, and appears only when that plugin is active.

### Shop (from EP Ecommerce)

Revenue and order counts for the last seven days and today, in your shop's main currency, with average order value and a pending-orders count, then a recent-sales list: the last five orders with their status, buyer, amount and time. See [EP Ecommerce](/plugins/ep-ecommerce/).

### Background Tasks (from EP Cron)

The heartbeat status pill (beating, stale, or down), a count of registered, overdue and dead tasks, and a table of every task with its schedule and last result. A read-only view of the [EP Cron](/plugins/ep-cron/) Background Tasks screen, surfaced where you land when you log in.

### Audience & Campaigns (from EP Newsletter)

Total subscribers on file, with active and pending counts, the number of campaigns, the count sent in the last seven days, and the last campaign. A quick read on your list and recent sending. See [EP Newsletter](/plugins/ep-newsletter/).

### Email Deliverability (from EP Email)

The active delivery transport (for example Mailgun over SMTP), emails sent and failures over the last seven days with the delivery rate, and a recent-failures list showing the reason for each. See [EP Email](/plugins/ep-email/).

### Traffic (from EP Analytics)

Views today and across the last seven days, the number of active pages, the human/bot split, and your top pages by views. Human and bot traffic are kept separate, so the headline figures are real people. See [EP Analytics](/plugins/ep-analytics/).

### SEO health (from EP SEO)

A green/amber/red health roll-up, your sitemap URL count, social-card readiness, structured-data type, and any noindex pages, plus your social image and favicon source. See [EP SEO](/plugins/ep-seo/).

### IndexNow (from EP IndexNow)

A status pill (Active, Off, or a failure flag), the number of indexable pages changed since the last submission, how long ago it last ran, and the auto-submit cadence, with the last result and key status beneath. A quick read on whether changed URLs are reaching Bing, Yandex and the Bing-powered AI search engines. See [EP IndexNow](/plugins/ep-indexnow/).

### Events (from EP Events)

Upcoming events and registration figures, so the next thing on the calendar is in front of you. See [EP Events](/plugins/ep-events/).

### Your EP Suite

The EP plugins active on the site, as a set of chips. Each chip links straight to that plugin's settings, so the dashboard doubles as a launcher for your suite.

## For plugin authors

Any EP plugin can contribute a panel by implementing `ep_dashboard_panel()` on its main class. EP Dashboard calls it on every active plugin and renders whatever comes back. You have total design freedom: return a structured array and the Command Centre styles it for you, or return raw HTML and own the whole panel.

```php
public function ep_dashboard_panel() {
    return array(
        'title'    => 'Shop',
        'source'   => 'EP Ecommerce',
        'detail'   => '3 active products',
        'accent'   => 'green',          // gold | green | blue | red | amber (left border)
        'priority' => 5,                // lower sorts higher up the grid
        'pill'     => array('label' => '4 today', 'class' => 'green'),
        'stats'    => array(
            array('value' => '£116.98', 'label' => 'Revenue (7d)', 'color' => 'green'),
            array('value' => 5,         'label' => 'Orders (7d)',  'color' => 'blue'),
        ),
        'body'     => '<ul>…your own HTML…</ul>',   // optional bespoke markup
        'empty'    => 'No sales yet.',
    );
}
```

Every struct key is optional except `title`. `stats` renders the tile row, `table` (a `head` plus `rows`) renders a result table, `meta` a small label/value footer, and `body` injects any bespoke HTML after them — style it with the dashboard's own CSS variables (`--epd-muted`, `--epd-border-soft`, `--epd-green`, and so on) so it matches the theme. Prefer the struct for a consistent look; reach for raw HTML — return a string, or `array('html' => '…', 'priority' => N)` — when you want a fully custom panel. Keep every query read-only and guarded, since the method runs on each admin dashboard load.

The shipped panels above (EP Ecommerce, EP Cron, EP Newsletter, EP Email, EP Analytics, EP SEO, EP IndexNow and EP Events) each provide their panel this way, so they are worth reading as worked examples.

## Troubleshooting

### "I don't see the dashboard"

EP Dashboard renders into the PageMotor 0.10 admin dashboard. Confirm you are on PageMotor 0.10b or later and that EP Dashboard is active. The Command Centre renders at the top of the admin landing page.

### "A panel I expected isn't there"

Each panel needs its source plugin active. No Shop panel means EP Ecommerce is not active; no Background Tasks panel means EP Cron is not active, and so on down the list. Activate the plugin and reload the dashboard.

### "The heartbeat panel says stale or down"

That is EP Cron reporting its own health, not a dashboard fault. See [EP Cron](/plugins/ep-cron/) troubleshooting: your cron job probably is not calling the heartbeat.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
