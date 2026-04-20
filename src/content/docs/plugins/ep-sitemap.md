---
title: "EP Sitemap"
description: "Dynamic XML sitemap generation for PageMotor. Auto-updated, valid sitemaps.org schema, supports image and priority hints."
sidebar:
  order: 52
---

EP Sitemap generates a valid XML sitemap for your PageMotor site, served dynamically at `/sitemap.xml`. Always up-to-date, supports the sitemaps.org schema, and optionally includes image references and priority hints.

Published by [ElmsPark Studio](https://elmspark.com).

## Why a sitemap

Search engines use sitemaps as a hint about what to crawl. Without one, they rely on link-following, which can miss pages with no internal links pointing to them. With one, every page you care about is discoverable.

Google Search Console, Bing Webmaster Tools, and most other search services let you submit a sitemap URL for faster indexing.

## What EP Sitemap does

- **Dynamic generation.** Every request to `/sitemap.xml` renders the current state of your site. No file to manually rebuild.
- **Valid schema.** Passes the [sitemaps.org](https://www.sitemaps.org/) validation.
- **Images included.** Every page's images are referenced with `<image:image>` entries, giving Google richer context.
- **Priority hints.** Set per-page priority (0.0 to 1.0) to tell search engines which pages matter most.
- **Last modified timestamps** from page metadata.
- **Exclusions.** Draft, unpublished, and marked-noindex pages are excluded.
- **Paginated** for large sites (splits into multiple sitemap files linked via a sitemap index).

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**

## Installation

1. Download `ep-sitemap.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Visit `https://yoursite.com/sitemap.xml`. You should see the XML.
4. Submit the URL to Google Search Console and Bing Webmaster Tools.

## Settings

- **Include images.** On by default. Adds image references to each URL entry.
- **Default priority.** Priority hint for pages that don't set their own. 0.5 is the sitemaps.org default.
- **Default change frequency.** How often each URL changes (daily, weekly, monthly).
- **Exclude paths.** List of URL patterns to skip (e.g. `/admin/*`, `/private/*`).

## Per-page overrides

On any page's content options:

- **Sitemap priority.** 0.0 to 1.0.
- **Sitemap change frequency.** Always, hourly, daily, weekly, monthly, yearly, never.
- **Exclude from sitemap.** Checkbox to keep this page out entirely.

## Large site handling

Once your site has more than 50,000 URLs (the sitemaps.org limit per file), EP Sitemap switches to a sitemap index model:

- `/sitemap.xml` becomes the index.
- `/sitemap-1.xml`, `/sitemap-2.xml`, etc. hold the actual URLs in chunks.

This happens automatically; no config needed.

## robots.txt

Add this to your robots.txt (via [EP Txt Files](/plugins/ep-txt-files/) or however you manage it):

```
Sitemap: https://yoursite.com/sitemap.xml
```

Search engines that crawl robots.txt auto-discover your sitemap.

## Troubleshooting

### "/sitemap.xml returns 404"

Check the plugin is active. Check nothing else at your domain is intercepting `/sitemap.xml` (some hosting providers serve a default one).

### "Sitemap is valid but Google says it's empty"

Google takes time to process. Check back in a day. Also submit in Search Console explicitly.

### "A specific page isn't appearing in the sitemap"

Check:
- Page is Published.
- Page isn't marked Exclude from sitemap.
- Page isn't marked Noindex in its SEO options.
- Page URL doesn't match an Exclude path in settings.

### "Images aren't showing in Google image search"

Sitemap images are a hint, not a guarantee. Google picks what to show. Your images need alt text and good context to get picked up.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
