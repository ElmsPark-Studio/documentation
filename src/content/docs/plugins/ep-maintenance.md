---
title: "EP Maintenance"
description: "Coming-soon and maintenance-mode holding page for your PageMotor site. One-toggle on/off, admin bypass, SEO-safe HTTP 503."
sidebar:
  order: 36
---

EP Maintenance puts a holding page in front of your site while admins keep working normally. Useful pre-launch, during a redesign, or when something is broken and you need to take the site off the air for an hour.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

One toggle. When on:

- **Visitors** see the holding page with your heading, message, and chosen colours.
- **Admins** browse the real site as normal.
- **The browser** receives `HTTP 503 Service Unavailable` with `Retry-After: 3600` and `noindex, nofollow` meta. Search engines understand the site is temporarily down and will come back later, so your search rankings are safe.

When off, the plugin is completely inert.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-maintenance.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Maintenance**.

On first install the heading, message, and colours are pre-populated with sensible defaults so the holding page is ready to use immediately.

## Settings

### Maintenance Mode

A single status checkbox. Tick it to enable the holding page. Untick to disable.

The status card at the top of the settings page reflects the current state in plain language: *Site is Live* (green) or *Maintenance Mode Active* (red).

### Page Content

- **Heading.** The large title shown to visitors. Plain text. Default: *Coming Soon*.
- **Message.** The body text below the heading. **HTML is allowed.** Use `<h2>`, `<a href>`, `<strong>`, `<em>`, `<br>`, `<ul>`, and so on. Plain-text line breaks render as line breaks. Default: *We are working on something new. Check back soon.*

### Design

- **Background Colour.** Page background.
- **Text Colour.** Default colour for the heading and the message body.
- **Heading Colour.** *Optional.* Override colour for the heading only. Leave blank to use the Text Colour. Useful when you want the heading in a brand accent and the body in a neutral text colour.
- **Accent Colour.** A thin horizontal bar (48 × 3 pixels) above the heading. Pick a brand accent that contrasts the background.

Colours are picked with a colour wheel and stored as hex with optional alpha (`RRGGBB` or `RRGGBBAA`). Values are normalised and validated on render.

## Who sees the holding page

| Visitor type | Sees |
| --- | --- |
| Logged-out visitor | Holding page (HTTP 503) |
| Logged-in subscriber or member | Holding page (HTTP 503) |
| Logged-in admin | The real site |
| Search-engine crawler | Holding page (HTTP 503), respects `Retry-After` |
| Admin AJAX requests | Always pass through |
| File uploads | Always pass through |

If you need a non-admin to preview the site while maintenance is on, give them an admin account temporarily. The plugin does not support IP whitelisting or path whitelisting.

## What it does not do

To set expectations clearly:

- **No countdown timer.** The page is text and colour, no live timer.
- **No IP whitelist.** Preview access is admin-login only.
- **No path whitelist.** All non-admin URLs return the holding page.
- **No email capture.** This is a holding page, not a launch list. If you want email capture, drop a Mailchimp or Bunny Mail embed into the **Message** field as raw HTML.

## Troubleshooting

### "I enabled maintenance mode but visitors still see the site"

Two possible causes:

1. **You're logged in as admin.** Open the site in a private or incognito window to see what visitors see.
2. **A caching layer is serving stale pages.** Cloudflare, Nginx fastcgi cache, or a customer-side reverse proxy can keep serving the old (live) page. Purge the cache after enabling.

### "The colours I picked are not applying"

Fixed in v1.0.5. The 1.0.4 release attempted this fix but missed the alpha-channel format the picker actually uses; 1.0.5 accepts all valid hex shapes. Update via **Plugins → Updates** or download the latest zip.

### "My HTML in the Message field is showing as plain text"

Fixed in v1.0.4. HTML in the Message field is rendered, not escaped. Update to 1.0.4 or later.

### "I want to disable the plugin but the site is also down"

If the site is up: deactivate from **Plugins → Manage Plugins** in the admin.

If the site is down and you cannot reach the admin: SFTP in and delete the `user-content/plugins/ep-maintenance/` folder. PageMotor will stop loading the plugin on the next request.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
