---
title: "EP Breadcrumbs"
description: "Breadcrumb navigation for PageMotor with Schema.org structured data and Focus/Thesis-compatible CSS classes for migration-friendly styling."
sidebar:
  order: 11
---

EP Breadcrumbs walks your page's parent hierarchy and renders a trail with Schema.org markup, so search engines can use it too. CSS classes match Focus and Thesis conventions so sites migrated from WordPress retain their existing styling.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Drop a breadcrumbs element into any Block in the Theme Editor (typically just above the page title in the header), and every page gets a trail like:

> Home › Services › Consulting

The trail is built from the page parent chain. If you have `/services/consulting/` and "Consulting" has "Services" as its parent, EP Breadcrumbs auto-generates the trail.

Structured data is emitted in two places:

- **Microdata** inline with the visible HTML (BreadcrumbList schema).
- **JSON-LD** in the document head via `structured_data()`.
- The **WebPage** schema is augmented with a reference to the breadcrumb list for a fully linked structured-data graph.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class** (bundled)

## Installation

1. Download `ep-breadcrumbs.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open your Theme Editor and add an **EP Breadcrumbs** instance to any Block. Most sites put it in the header Block above the page title.

## Settings

Accessed under the **EP Suite nav → Breadcrumbs**.

- **Default home text.** What to display for the home crumb (default: "Home").
- **Default separator.** Character between crumbs (default: "›"). Can be a character or any short string.
- **Hide on home page.** Most sites want this on — no point showing "Home" alone.

### Per-instance overrides

On the element options for each breadcrumbs instance in the Theme Editor:

- Override the **home text** for this specific instance.
- Override the **separator** for this specific instance.

Useful when you have breadcrumbs in two places with different visual styles.

### Per-page overrides

On the content options for any page:

- **Custom breadcrumb text.** Overrides the page title for this page only. Use when your page title is long but you want a short crumb.

## CSS classes

Matches Focus and Thesis conventions, so existing stylesheets from migrated sites usually "just work":

- `.crumbs` — the container.
- `.crumbs-crumb` — each individual crumb link.
- `.crumbs-sep` — each separator between crumbs.

## Troubleshooting

### "Breadcrumbs show 'Home › Current page' with no middle crumbs"

The current page has no parent in the page hierarchy. Set a parent on the page's options and the trail fills in.

### "Breadcrumbs show the wrong crumb name for one page"

Use **Custom breadcrumb text** in that page's content options to override. Useful when your full page title is "The ultimate guide to XYZ for beginners" but you want the crumb to just say "XYZ Guide".

### "Breadcrumbs appear on the home page and I don't want them to"

Settings → Breadcrumbs → **Hide on home page** to on.

### "Breadcrumbs appear on a 404 page"

They shouldn't — EP Breadcrumbs hides itself automatically on error pages. If they do appear, the page is not correctly detected as an error page by PageMotor. Check PageMotor's 404 handling.

### "Schema.org warnings in Search Console"

Google's rich results testing tool validates BreadcrumbList schema. If it flags warnings, paste the test URL into the review queue and we'll look at the emitted schema.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
