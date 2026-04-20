---
title: "EP Redirects"
description: "URL redirect manager for PageMotor. 301s and 302s, wildcard patterns, bulk import for migrations, 404 log to spot missing redirects."
sidebar:
  order: 44
---

EP Redirects is a URL redirect manager for PageMotor. Set up 301s (permanent) and 302s (temporary) from any old URL to any new URL. Supports wildcard patterns for bulk migrations. Includes a 404 log so you can spot and fix missing redirects.

Published by [ElmsPark Studio](https://elmspark.com).

## When you need this

- **Migrating from WordPress, Squarespace, or any other CMS.** Your URL structure changes; redirect old URLs to new ones so existing links and search engine rankings carry over.
- **Redesigning your site.** Changed `/services/` to `/what-we-do/`? Redirect the old URL.
- **Consolidating content.** Merging two blog posts into one? Redirect the retired one to the combined one.
- **Retiring campaigns.** A landing page you ran a campaign on is now defunct; redirect to your general page.

## Overview

- **Simple redirects.** Old URL in, new URL out. 301 or 302 status code.
- **Wildcard patterns.** `/blog/*` → `/journal/*` preserves the trailing part.
- **Regex patterns** (optional) for more complex rewrites.
- **Bulk import** from CSV or JSON for large migrations.
- **404 log** showing URLs visitors hit that returned 404, so you can set up redirects before search engines drop the old URLs.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

## Installation

1. Download `ep-redirects.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.

## Adding a redirect

From **Plugin Settings → EP Redirects → Redirects**:

1. Click **Add Redirect**.
2. **From path**: the old URL, relative to your site root. e.g. `/old-page/`.
3. **To URL**: the new destination. Can be relative (`/new-page/`) or absolute (`https://otherdomain.com/`).
4. **Status code**: 301 (permanent, recommended for SEO) or 302 (temporary).
5. Save.

Next time someone (or a search engine) visits `/old-page/`, they're redirected to `/new-page/` with the selected status.

## Wildcard patterns

Use `*` in the From path to capture a segment:

- From: `/blog/*` → To: `/journal/*` — `/blog/my-post/` becomes `/journal/my-post/`.
- From: `/products/old-*/` → To: `/catalogue/*/` — `/products/old-widget/` becomes `/catalogue/widget/`.

The `*` captures everything from that point onward and substitutes at the matching `*` in the To URL.

## Bulk import

For a WordPress migration with hundreds of URLs:

1. Export your WP URL structure to CSV with columns `from,to`.
2. In EP Redirects settings, click **Import**, upload the CSV.
3. Preview the import to catch any syntax issues.
4. Confirm.

Each imported redirect gets a batch ID, so if something goes wrong you can bulk-delete the import in one click.

## 404 log

Every 404 on your site is logged with the URL and hit count. Sorted by hit count:

- Top of the list = URLs most people are trying to reach that don't exist.
- Perfect candidates for a redirect to the real page.

Click a row to create a redirect directly from the 404 log.

Log auto-purges after 30 days by default.

## Troubleshooting

### "My redirect isn't triggering"

Check:
- The From path starts with `/` and matches exactly (no trailing slash mismatch).
- No more-specific PageMotor page exists at the From path — PageMotor's page router runs before the redirect.
- Caching isn't serving an old version. Clear caches.

### "Wildcard isn't capturing what I expect"

Test the pattern in isolation. The `*` captures greedily to the end of the URL. If you want to stop at a specific character, use a more specific pattern.

### "Import is rejecting rows"

Check the CSV format: two columns, exactly `from` and `to` as headers, no BOM, UTF-8 encoded. Download a sample CSV from the import page to match the expected shape.

### "301 vs 302 — which?"

Almost always 301. Permanent redirects pass ranking signals to the new URL. Use 302 only when the old URL will genuinely come back (e.g. temporary maintenance page).

### "404 log is huge"

A bot is probing for WordPress admin URLs (`/wp-admin/`, `/xmlrpc.php`). That's normal. Filter by URL pattern to focus on real 404s from your actual content.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
