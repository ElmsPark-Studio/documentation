---
title: "EP Tracking"
description: "Tracked redirect links with click analytics and conversion attribution. A built-in link shortener for campaigns and affiliate tracking across EP Suite."
sidebar:
  order: 56
---

EP Tracking is a built-in link shortener with analytics. Create short tracked URLs that redirect to any destination, log every click with referrer and timestamp, and optionally attribute conversions. Designed for use inside EP Suite: campaign tracking, affiliate coordination, outbound link analysis.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Short tracked URLs** at `/go/<slug>` (configurable path).
- **Click logging** with IP, user-agent, referrer, timestamp (anonymised per GDPR defaults).
- **Destination override** — change where a link points without changing the short URL. Good for campaigns that evolve.
- **Expiry dates** on links.
- **Password protection** on links (the URL works, but the click page prompts for a password before redirecting).
- **Conversion attribution** — tie subsequent orders or signups to the click that brought the visitor.

## Status

**Version 0.1.1** — core tracking works, some analytics views still basic.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**

## Installation

1. Download `ep-tracking.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.

## Creating a tracked link

From **Plugin Settings → EP Tracking → Links**:

1. Click **Add Link**.
2. **Slug**: short identifier (e.g. `spring-sale`). Default path becomes `/go/spring-sale`.
3. **Destination URL**: where to redirect.
4. **Description**: internal note.
5. **Expiry**: optional date after which the link stops working.
6. **Password**: optional.
7. Save.

Share `https://yoursite.com/go/spring-sale` anywhere. Every click is tracked.

## Analytics dashboard

Per-link analytics:

- **Total clicks** over all time.
- **Clicks over time** chart.
- **Top referrers** — where clicks come from.
- **Device / browser breakdown.**
- **Conversions attributed** (if the visitor later bought something on the site).

Compare links side-by-side to see which campaigns performed.

## Changing the destination

A key use case: you share a tracked link in an email, later decide the destination needs to change (post moved, product sold out, etc.). Edit the link's destination — the short URL keeps working, just goes somewhere new. Historic analytics remain.

## Conversion attribution

When a visitor clicks a tracked link, a cookie is set. Later, if they complete a purchase (EP Ecommerce) or booking (EP Booking), the conversion is attributed to the click. Visible in the link's analytics view.

Cookie duration is configurable. Default 30 days.

## Password protection

Password-protected links:

- URL still works, anyone can visit.
- Before the redirect, a page prompts for the password.
- Only after correct password does the redirect happen.

Useful for semi-private links — share with a specific group, don't trust them not to share further, but raise the bar.

## Troubleshooting

### "Click doesn't redirect"

Check the destination URL is valid and not empty. Also check expiry hasn't passed.

### "No analytics data despite people clicking"

Check the EP Tracking endpoint is reachable. Try clicking the link yourself and verify the click appears in the analytics.

### "Conversion attribution doesn't work"

The visitor's browser must accept cookies. Private browsing modes sometimes don't. Also the attribution cookie is per-domain — if your tracked link redirects to a different domain, conversions there aren't tracked.

### "Short URLs clash with other plugin URLs"

The default path prefix `/go/` can be changed in settings. Pick something that doesn't collide with your site's content structure.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
