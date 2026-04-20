---
title: "EP SEO"
description: SEO essentials for PageMotor. Open Graph, Twitter Card, favicon, Schema.org structured data. Per-page overrides and site-wide defaults.
sidebar:
  order: 50
---

EP SEO adds the SEO essentials PageMotor core doesn't: Open Graph tags so links preview nicely on social media, Twitter Card tags for Twitter/X, favicon configuration, and Schema.org structured data. All with site-wide defaults and per-page overrides.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP SEO does

- **Open Graph** tags in the head (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`) so link previews on Facebook, LinkedIn, Slack, Discord, WhatsApp look right.
- **Twitter Card** tags for better previews on X.
- **Favicon** setup — single-file or multi-resolution pack.
- **Schema.org structured data** — Organisation, WebSite, WebPage, Article, BreadcrumbList. Emitted as JSON-LD in the head.
- **Default social image** — one image used for every page unless overridden.
- **Per-page overrides** — custom social title, description, and image per specific page.

## What EP SEO doesn't do

- **Keyword research.** That's a strategy problem, not a plugin problem.
- **Content auditing.** Different tools for that.
- **Rank tracking.** Use Ahrefs, Semrush, or Google Search Console.

EP SEO is about making sure the technical SEO metadata is right. The content quality is still your job.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**

## Installation

1. Download `ep-seo.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP SEO** and fill in the site-wide defaults.

## Settings sections

### Open Graph

- **Site name.** Used as `og:site_name`. Usually your brand.
- **Default OG image.** Used for every page unless overridden. 1200x630 is the standard recommendation. Upload via the drag-and-drop widget.
- **Default OG description.** Fallback if a page doesn't define its own.

### Twitter Card

- **Card type.** `summary`, `summary_large_image`, etc.
- **Twitter handle.** Your site's handle (e.g. `@yoursite`).

### Favicon

- **Favicon.** Upload a PNG or ICO. The plugin auto-generates the multi-resolution links in the head.
- **Apple touch icon.** Separate 180x180 PNG for iOS.
- **Theme colour.** Browser chrome colour on mobile (`<meta name="theme-color">`).

### Organisation schema

- **Organisation name, URL, logo, contact.** Emitted as JSON-LD Organisation on every page. Helps Google understand your brand.

### Site-wide defaults

- **Default meta description.** Fallback when a page hasn't set one.
- **Default meta keywords.** Rarely useful, Google ignores them, but included for completeness.

## Per-page overrides

On any page's content options:

- **OG title** (falls back to page title).
- **OG description** (falls back to default).
- **OG image** (falls back to default).
- **Schema type** — WebPage, Article, Product, etc.

For pages representing articles or products, use the specific schema type so Google shows richer search results.

## Schema.org emissions

Per page type, EP SEO emits:

- **Every page:** `WebPage` + `Organization` + `BreadcrumbList` (if EP Breadcrumbs is active) in JSON-LD.
- **Article pages:** `Article` schema with headline, author, datePublished.
- **Product pages** (if schema type = Product): `Product` schema with offer details.

Validate your emitted schema in [Google's Rich Results Test](https://search.google.com/test/rich-results).

## Troubleshooting

### "Link preview on Facebook shows old image"

Facebook caches Open Graph data aggressively. Use their [Sharing Debugger](https://developers.facebook.com/tools/debug/) to force-refresh the cache.

### "Twitter/X link preview is broken"

Test in [the Card Validator](https://cards-dev.twitter.com/validator). Common causes: OG image URL is wrong, image is too small, image is blocked by robots.txt.

### "Favicon doesn't update after I uploaded a new one"

Browsers cache favicons aggressively. Try hard refresh (Cmd+Shift+R), or incognito mode, or a different browser. If still wrong, check the image path is actually updated in your site's head.

### "Rich results test shows 'unnamed property' warnings"

One of your schema fields is empty. Check the Organisation schema setting has all required fields. If a per-page override is partial, complete it or remove it.

### "I don't want OG tags on a specific page"

Set **Noindex** on the page's content options. Most plugins (including EP SEO) will skip rich metadata on noindex pages.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
