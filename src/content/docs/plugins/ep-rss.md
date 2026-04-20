---
title: "EP RSS"
description: RSS 2.0 and Atom 1.0 feed generation for PageMotor. Auto-publishes feeds at conventional URLs with configurable content filters.
sidebar:
  order: 46
---

EP RSS adds RSS 2.0 and Atom 1.0 feed generation to PageMotor. Visitors and feed readers (Feedly, Inoreader, NetNewsWire) can subscribe to your content. Search engines also consume feeds for faster indexing.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **RSS 2.0** at `/feed/` (conventional URL).
- **Atom 1.0** at `/atom/`.
- **Configurable content filter**: posts only, pages only, specific categories, or custom queries.
- **Per-feed customisation**: title, description, image.
- **Summary or full content** per feed.
- **Valid markup** passes the [W3C Feed Validator](https://validator.w3.org/feed/).

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**

## Installation

1. Download `ep-rss.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open `https://yoursite.com/feed/` — should render a valid RSS feed of your latest content.

## Settings

- **Feed title.** Usually your site name.
- **Feed description.** Short site description.
- **Feed image.** Square logo.
- **Content filter.** All pages, specific category, or custom.
- **Summary vs full.** Show post excerpts or the full body. Full content is friendlier to readers; summary drives clicks back to your site.
- **Items per feed.** Typically 10-20.
- **Include images.** Embed images in the feed content.

## Auto-discovery

The plugin adds `<link rel="alternate">` tags to your site's head, so browsers and feed readers auto-detect the feed URL. Most readers can subscribe by just pasting your homepage URL.

## Multiple feeds

Configure additional feeds under **Custom feeds**:

- URL path (e.g. `/blog-feed/`).
- Title, description.
- Query: which content to include (specific category, tag, etc.).

Useful when you want a separate feed for a blog category, a newsletter archive, or a podcast.

## Troubleshooting

### "/feed/ returns a 404"

PageMotor's router needs to recognise the feed URL. Check the plugin is active. Also check you don't have a page at the path `/feed/` that's taking precedence.

### "Feed validates but my reader doesn't update"

Feed readers poll on their own schedule (usually every hour). Adding content doesn't instantly appear in the reader. Wait.

### "Items per feed setting isn't respected"

Double-check the setting saved. Also check your reader isn't pulling from a cached URL with different parameters.

### "Images in the feed don't load"

Check the image URLs are absolute (include `https://yoursite.com/`). Relative URLs in feed content don't resolve in most readers.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
