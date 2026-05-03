---
title: "EP Txt Files"
description: "Dynamically serve robots.txt and llms.txt from the PageMotor admin. Edit through a UI instead of FTP. Version history included."
sidebar:
  order: 57
---

EP Txt Files dynamically serves `/robots.txt` and `/llms.txt` from PageMotor's settings rather than files on disk. Edit through the admin UI, see version history, have changes go live instantly. No FTP, no cache-busting, no forgotten deploys.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Two files, both conventional:

### /robots.txt

The file search engines read to understand which pages they should and shouldn't crawl. Must be at the site root and served at the exact URL `/robots.txt`.

### /llms.txt

The newer convention for guiding LLM crawlers (GPTBot, ClaudeBot, etc.) with a site summary plus links to the content you want AI systems to prioritise. See [llmstxt.org](https://llmstxt.org) for the full spec.

## Why serve them dynamically

- **No FTP.** Edit from the admin.
- **Version history.** Every change is logged so you can see what it was before.
- **Instant.** Changes go live on save, no deploy step.
- **Validation.** The plugin flags obvious mistakes (syntax errors in robots.txt directives).

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

## Installation

1. Download `ep-txt-files.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Check that `https://yoursite.com/robots.txt` now returns the plugin's version.

## Settings

### robots.txt

Textarea containing your robots.txt content. Defaults to a reasonable starter:

```
User-agent: *
Allow: /
Sitemap: https://yoursite.com/sitemap.xml
```

Add specific user-agent blocks for bots you want to restrict. The **EP Sitemap** plugin's URL is auto-filled if that plugin is installed.

### llms.txt

Textarea for your llms.txt. No default content — LLMs.txt is site-specific and needs thought. Typical structure:

```
# My Site

> One-sentence description of what the site is about.

## Core content

- [Page title](/url) — short description
- [Another page](/another) — short description

## Optional

- [Less-critical page](/less-critical)
```

## Per-file controls

- **Enabled.** Toggle. Off makes the plugin inert; PageMotor falls back to whatever (if anything) is at the physical file path.
- **Cache-Control headers.** Default is to let the content be cached for 1 hour. Adjustable.

## Version history

Every save creates a history entry:

- Timestamp.
- Who changed it.
- Diff from previous version.

Click an old version to revert.

## Troubleshooting

### "/robots.txt still serves the old version"

Check:
- The plugin is active.
- The **Enabled** toggle is on for robots.txt.
- Your web server isn't serving a physical `robots.txt` file that overrides the plugin. Remove or rename any file at `/robots.txt` on disk.
- Your CDN isn't caching the old version. Purge the CDN.

### "I broke robots.txt and now Google can't crawl my site"

Revert to a previous version from the history. Or use the default starter content.

### "I don't know what to put in llms.txt"

Start simple. A one-line description and links to your 5 most important pages is enough. The spec at [llmstxt.org](https://llmstxt.org) has examples.

### "Cache-Control is ignored"

Your CDN or hosting provider might override. Check the response headers in browser dev tools. If the CDN is overriding, configure it to respect origin cache headers.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
