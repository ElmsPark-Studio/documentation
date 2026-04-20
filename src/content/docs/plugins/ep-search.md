---
title: "EP Search"
description: "Site search for PageMotor. Search form shortcode, results page, title and body matching, basic filtering, optional search analytics."
sidebar:
  order: 48
---

EP Search adds site search to PageMotor. Drop in a search form shortcode, and a dedicated results page renders matches across your content. Basic but reliable full-text search.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Search form** shortcode for any page (header, sidebar, dedicated page).
- **Results page** at a configurable URL (typically `/search/`).
- **Title + body matching** on pages and posts.
- **Relevance ranking** — title matches rank above body matches.
- **Filter by content type** — pages only, posts only, or all.
- **Paginated results.**
- **Search analytics** — optional logging of what people search for.

What EP Search doesn't do: AI-powered semantic search, fuzzy matching, spelling correction, search across external content (like PDFs). It's a basic SQL LIKE search. For most sites this is plenty.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**

## Installation

1. Download `ep-search.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Create a page at `/search/` and add `[ep-search-results]`.
4. Add `[ep-search-form]` to your header or wherever you want the search box.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[ep-search-form]` | Search input with submit button. |
| `[ep-search-results]` | Renders results of the current search query (`?q=...`). |

## Settings

- **Results page URL.** Where search forms submit to (default `/search/`).
- **Results per page.** Pagination size.
- **Content types to include.** Pages, posts, custom types.
- **Excerpt length.** How much body text to show under each result.
- **Highlight matches.** Bold the search terms in results.
- **Log searches.** Enable search analytics.

## Search analytics

When logging is on, every search is recorded: query, timestamp, results count. View in the admin dashboard:

- **Top searches.** What people are looking for most.
- **Zero-result searches.** Queries that returned nothing. Prime candidates for new content.
- **Search volume over time.**

Useful for spotting content gaps.

## Troubleshooting

### "Search returns no results for terms I know are in my content"

Check:
- The content is Published, not Draft.
- The content type is in the "include" list in settings.
- The terms actually appear — search is literal, not fuzzy. "CEO" won't match "Chief Executive Officer".

### "Results page returns 404"

The page at the Results page URL (default `/search/`) needs to exist and contain `[ep-search-results]`. Create it.

### "Highlighting breaks page styling"

Highlighting wraps matches in `<mark>` tags. If your theme styles `<mark>` oddly, the highlights look wrong. Override in your theme's CSS.

### "Search is slow on a large site"

`LIKE '%query%'` queries don't use indexes. On sites with thousands of pages, search slows. If this becomes a problem, consider external search (Algolia, Meilisearch) via a custom integration — EP Search is deliberately simple.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
