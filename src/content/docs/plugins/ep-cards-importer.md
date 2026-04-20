---
title: "EP Cards Importer"
description: "WordPress-to-PageMotor migration add-on for EP Cards. Reads JSON exports from EP WP Exporter, rehosts images locally, commits groups and cards as a single rollbackable batch."
sidebar:
  order: 13
---

EP Cards Importer is the official migration add-on for [EP Cards](/plugins/ep-cards/). Feed it a JSON export from your WordPress site, click Preview, click Commit, done. Thesis Focus Cards content lands in EP Cards with images rehosted locally and every import as a single rollbackable batch.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

The importer handles both Thesis Focus Cards flavours from a single upload path:

- **The standalone Thesis addon plugin** (`wp-content/thesis/boxes/focus-cards/` with fully-populated `_focus_cards-options` meta).
- **The Focus skin's built-in `focus_cards` CPT** (mostly empty meta, style from theme-level settings).

Two-step workflow: **Preview** parses the JSON and shows you exactly what will happen, **Commit** writes it to the database. Between the two, you can check sample cards render correctly, see which groups will be created, and catch any warnings about source content that doesn't fit cleanly.

Everything in one import shares a batch UUID. If it goes wrong, the **Delete** button on the batch row deletes every group and card from that import in one SQL cascade. Zero manual cleanup.

## Requirements

- **PageMotor 0.7 or later**
- **EP Cards core** (must be active before the importer will commit)
- PHP limits: **50M** `upload_max_filesize`, **50M** `post_max_size`, **256M** `memory_limit`. The settings page shows a preflight panel that flags any of these as red if they are too low.
- **EP WP Exporter** or its legacy `pm-exporter` predecessor running on the source WordPress site to produce the JSON.

## The end-to-end migration

### On the source WordPress site

1. Install [EP WP Exporter](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Go to **Tools → EP WP Export**.
3. **Untick every default checkbox.** Tick **only** "Focus Cards (for EP Cards Importer add-on)".
4. Click **Export for PageMotor**. A JSON file downloads.

### On the destination PageMotor site

1. Install both **EP Cards** core and **EP Cards Importer**.
2. Open the **EP Cards Importer** settings page.
3. Confirm the preflight panel shows green (PHP limits adequate, EP Cards core active).
4. Click **Choose File**, pick the JSON, click **Preview Import**.
5. Review:
   - Parsed groups.
   - Sample rendered cards.
   - Proposed global style options (from the source's theme settings).
   - Any warnings.
6. Click **Import these cards** to commit.
7. The image rehoster runs automatically. Watch the response panel for per-image download stats.
8. If any images failed, click **Rehost** on the batch row in the **Import History** panel to retry just those. Idempotent — successful images are never re-downloaded.

## What gets migrated

The importer maps Thesis fields to EP Cards columns:

| Source field (WordPress) | Destination column (EP Cards) |
|---|---|
| `post_title` | `title` |
| `post_content` | `body` (sanitised on write) |
| `featured_image.url` | `image_url` (rehosted to your local uploads) |
| `featured_image.alt` | `image_alt` |
| `meta._focus_cards-options.subtitle` | `subtitle` |
| `meta._focus_cards-options.url` | `link_url` (whole-card link) |
| `meta._focus_cards-options.title-url` | `title_link` |
| `meta._focus_cards-options.image-url` | `image_link` |
| `meta._focus_cards-options.display.center` | `centered` |
| `meta._focus_cards-options.display.title-off` | `title_off` |
| `meta._focus_cards-options.display.image-only` | `image_only` |
| `meta._focus_cards-options.class` | `custom_class` |
| `meta._focus_cards-custom-image.*` | Overrides `featured_image` |
| `taxonomies.focus_cards_group` (slug) | Derives a group, sets `group_id` |
| `theme.focus.options.focus_cards` | Offered as new global defaults on Preview |

**Per-card style overrides (style, corners, spacing, hover) are NOT migrated** because Thesis Focus Cards stores styling globally rather than per-card. Imported cards inherit your site's EP Cards global defaults. If you need per-card variation, adjust after import.

## Image rehosting

The rehoster runs as a separate pass after structural import:

- Walks every card marked `needs_rehost=1` in the batch.
- Downloads each featured image and every inline `<img src>` from the body HTML to your local PageMotor uploads directory.
- Rewrites stored body HTML to point inline images at the new local URLs.
- **SVG-aware:** content-type detection, viewBox parsing for dimensions when `getimagesize()` fails.
- **Curl bounded:** 10-second connect timeout, 30-second total timeout, 10MB max body via progress callback, max 3 redirects.
- **Failure-tolerant:** any single image failure leaves `needs_rehost=1` on the card so a second Rehost run picks up where the first left off. Never aborts the structural import halfway through.
- **Re-runnable** via the **Rehost** button on the import history table. Repeated runs only try images still flagged as needing rehost.

## Legacy shortcode compatibility

The importer registers two legacy shortcode aliases that dispatch to EP Cards core:

- `[card]` → `[ep_card]`
- `[card_group]` → `[ep_card_group]`

This means page content that was copied verbatim from a Thesis source site (which used the unprefixed `[card]` shortcode) renders unchanged after migration. No search-and-replace across your content is needed.

## Three failure modes, clearly distinguished

The importer recognises and reports three separate problems with your JSON:

1. **"No Focus Cards data in this export."** You exported without ticking the Focus Cards checkbox. Re-export with that checkbox on.
2. **"No Focus Cards plugin installed on the source site."** The CPT is not registered. Check that Thesis Focus Cards (either flavour) is active on the source.
3. **"Focus Cards plugin present but no content."** CPT is registered but no posts exist. The source site simply has no cards to export.

## Generator string acceptance

The importer accepts JSON from both exporter lineages:

- **`EP WP Exporter X.Y.Z`** (1.3.0 and later).
- **`PageMotor Exporter X.Y.Z`** (legacy, pre-1.3.0).

In-flight migrations where the source site hasn't upgraded its exporter yet still work.

## Rollback

Every import stamps a batch UUID on every row it writes. The **Import History** panel lists every batch with a **Delete** button. Clicking it cascade-deletes:

- Every card stamped with that batch ID.
- Every group stamped with that batch ID.
- The batch row itself.

Other cards and groups (from other imports, or hand-created) are untouched.

## Troubleshooting

### "The preflight panel shows red for upload_max_filesize"

Edit your PHP config (`/etc/php/8.2/fpm/php.ini` or equivalent) and set `upload_max_filesize = 50M` and `post_max_size = 50M`. Reload PHP-FPM. Reload the settings page.

### "The import succeeds but images are broken"

The rehoster ran into errors. Open the batch in Import History, look at the per-image stats. Common causes:

- Source image URLs require authentication (private WordPress sites).
- Source images are huge and exceed the 10MB cap.
- Source site has firewall rules blocking your PageMotor server.

Click **Rehost** on the batch row after fixing the underlying issue.

### "Groups are created but all cards are ungrouped"

The source JSON doesn't have the `focus_cards_group` taxonomy populated on the cards, or the group slugs in taxonomies don't match what the importer created as groups. The preview panel warns about this specifically.

### "The `[card]` shortcode still doesn't work after import"

The importer registers legacy aliases only if it is active. If you uninstalled EP Cards Importer after migration, the aliases are gone. Either re-activate the importer, or do a global search-and-replace in your content from `[card` to `[ep_card`.

### "Rerunning the import duplicates cards"

Use **Delete** on the existing batch first. The importer does not deduplicate cards across batches — it trusts you to roll back before re-importing.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
