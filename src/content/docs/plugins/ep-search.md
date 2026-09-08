---
title: "EP Search"
description: "Site search for PageMotor. Search form shortcode, results page, title and body matching, basic filtering, optional search analytics."
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

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

## Installation

1. `ep-search.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
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

## Clearing a search

Once results are showing, a “Clear search” link appears next to the result count. Clicking it returns to the unsearched URL, the same page with no `?s=...` parameter, so the form input clears and the results panel disappears.

Refreshing the page does **not** clear results, because the search term is part of the URL. Use the Clear link, or navigate away and back.

## Customising colours

Every colour is driven by a `--eps-*` CSS custom property. Override them in your theme's CSS to recolour the form, button, links, and result divider in one place:

```css
:root {
    --eps-button-bg: #1a73e8;
    --eps-button-bg-hover: #1557b0;
    --eps-link: #1a73e8;
}
```

Available: `--eps-input-border`, `--eps-input-focus`, `--eps-input-bg`, `--eps-input-text`, `--eps-button-bg`, `--eps-button-bg-hover`, `--eps-button-text`, `--eps-link`, `--eps-url`, `--eps-clear-link`, `--eps-clear-link-hover`, `--eps-text-muted`, `--eps-text-subtle`, `--eps-divider`, `--eps-mark-bg`, `--eps-mark-text`.

## Troubleshooting

### “Search returns no results for terms I know are in my content”

Check:
- The content is Published, not Draft.
- The content type is in the "include" list in settings.
- The terms actually appear — search is literal, not fuzzy. "CEO" won't match "Chief Executive Officer".

### “Results page returns 404”

The page at the Results page URL (default `/search/`) needs to exist and contain `[ep-search-results]`. Create it.

### “Highlighting breaks page styling”

Highlighting wraps matches in `<mark>` tags. If your theme styles `<mark>` oddly, the highlights look wrong. Override in your theme's CSS.

### “Search is slow on a large site”

`LIKE '%query%'` queries don't use indexes. On sites with thousands of pages, search slows. If this becomes a problem, consider external search (Algolia, Meilisearch) via a custom integration — EP Search is deliberately simple.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
