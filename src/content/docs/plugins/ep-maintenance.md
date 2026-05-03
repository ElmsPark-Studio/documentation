---
title: "EP Maintenance"
description: "Coming-soon and maintenance-mode overlays for your PageMotor site. Whitelisted admin access, configurable page, email capture for launches."
sidebar:
  order: 36
---

EP Maintenance puts a coming-soon or maintenance page in front of your site while keeping the admin and whitelisted users working normally. Useful pre-launch, during a big update, or when something is broken and you need to take the site off the air temporarily.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Two modes:

- **Coming soon.** For pre-launch sites. Shows a marketing page with optional email capture ("Notify me when you launch"). Good SEO: returns `200 OK` so it can be indexed and shared.
- **Maintenance mode.** For during-outage cover. Returns `503 Service Unavailable` with a `Retry-After` header so search engines know not to index and to come back later.

In both modes:

- **Admins bypass.** Logged-in admins see the real site.
- **Whitelisted IPs bypass.** Add your office IP for the whole team.
- **Whitelisted paths.** Sometimes you need a specific URL reachable (a webhook endpoint, a status page). Whitelist it.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

Optional:

- **EP Email** if you want to capture emails for the launch notification list.
- **EP Newsletter** to auto-add captured emails to a list.

## Installation

1. Download `ep-maintenance.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Maintenance**.

## Settings

### Mode

- **Off** (default). Plugin is inert, site behaves normally.
- **Coming Soon.** Pre-launch overlay.
- **Maintenance.** Short-term outage overlay.

### Appearance

- **Page title.** Shown in the browser tab.
- **Heading.** Main heading on the overlay page.
- **Body.** Text or HTML for the overlay body.
- **Background.** Colour or image URL.
- **Logo.** Upload or paste a URL.

### Access

- **Whitelisted IPs.** Comma-separated. Supports CIDR. Your own office IP belongs here.
- **Whitelisted paths.** Comma-separated URL paths that remain reachable. Useful for webhooks, health checks, robots.txt.

### Email capture (Coming Soon only)

- **Show form.** Toggle.
- **Placeholder text.** "your@email.com" by default.
- **Submit label.** "Notify me" by default.
- **Send captures to newsletter list.** If EP Newsletter is active, pick a list.

## HTTP status codes

The two modes return different HTTP status codes deliberately:

- **Coming Soon returns 200 OK.** Search engines can index the page. Sharing it shows the marketing page.
- **Maintenance returns 503 Service Unavailable** with a `Retry-After` header. Search engines know not to index and to come back later.

This matters for SEO. Returning 503 on a long-lived "coming soon" page can cause search engines to drop you from the index.

## Typical workflows

### Pre-launch

1. Site is built but not announced. Set mode to Coming Soon.
2. Share the link for people to sign up for launch notification.
3. On launch day, set mode to Off.
4. Export captured emails, import into EP Newsletter, send launch announcement.

### Planned maintenance

1. Before starting work, set mode to Maintenance.
2. Do your work (update plugins, database migrations, whatever).
3. Set mode to Off when done.

### Unplanned outage

1. Something broke. Set mode to Maintenance.
2. Fix the issue, test with your whitelisted admin session.
3. Set mode to Off when confident.

## Troubleshooting

### "I set mode to Coming Soon but I still see the real site"

You're probably logged in as admin. That's working as intended. Open an incognito window to see what visitors see.

### "My office team sees the overlay despite being whitelisted"

Verify the whitelisted IP is correct. Your apparent IP might be different from what you expect (corporate VPN, mobile hotspot). Check what [ifconfig.me](https://ifconfig.me) says from the affected machine.

### "Webhook endpoint returns 503 even though I whitelisted the path"

Path match must be exact. If your webhook is at `/wh/stripe/` and you whitelisted `/webhooks/`, they won't match. Be specific.

### "Search engines keep crawling my site during maintenance"

Make sure mode is set to Maintenance (returns 503), not Coming Soon (returns 200). Also check your robots.txt isn't still indicating "crawl everything".

### "Email capture form submissions aren't saving"

Check EP Email is installed and configured (for the submission to go through EP Email's processing). Check the newsletter list ID in settings is valid.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
