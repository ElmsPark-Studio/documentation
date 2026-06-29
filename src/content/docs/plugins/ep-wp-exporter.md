---
title: "EP WP Exporter"
description: "WordPress companion plugin for the EP Suite. Installs on a WordPress source site to produce a JSON snapshot for migration to PageMotor. Read-only — makes no changes to your site."
---

EP WP Exporter is the WordPress-side companion to the EP Suite. You install it on the WordPress site you want to move, click one button, and get a JSON snapshot of everything PageMotor needs to receive the migration: posts, pages, menus, widgets, theme settings (with extra extraction for Thesis 2.x and Focus), comments, and a manifest of media files.

It is read-only. It writes nothing to your WordPress database or filesystem. Install, export, uninstall.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

The plugin produces a single JSON file that mirrors the structure expected by PageMotor's import side. The export is opt-in per section, so you can pull a full snapshot or just the bits you need.

What's in the JSON:

### Site info

- Site name, tagline, URL, admin email.
- Locale, timezone, date and time formats.
- Permalink structure.
- Front page configuration (static page vs latest posts, with the front and blog page IDs/slugs).
- WordPress and PHP versions.
- A list of every active plugin (so the migration receiver can flag features that need EP equivalents).

### Content

- **Posts** — full post body, author, date, status, categories, tags, custom fields.
- **Pages** — same shape as posts, hierarchical.
- **Custom Post Types** — every registered CPT and its posts.
- **Comments** — threaded structure preserved.
- **Focus Cards** — the Focus theme's `focus_cards` CPT and its theme options, scoped specifically for the [EP Cards Importer](/plugins/ep-cards-importer/) add-on.

### Structure

- **Navigation Menus** — every menu, locations, items, parent/child structure, URLs.
- **Widgets and Sidebars** — every active widget in every sidebar with its settings.
- **Media manifest** — URL list of attachments (no binary files in the JSON; you rsync the `uploads/` folder separately).

### Theme

- Active theme name and version.
- Theme mods.
- Customizer settings.
- Extra extraction for **Thesis 2.x** and **Focus** — design options, skin data, header/footer markup, focus_cards options.

## Requirements

- WordPress 5.0 or newer.
- PHP 7.4 or newer.
- The user running the export must have the `manage_options` capability (i.e. a WordPress admin).

## Installation

This plugin installs on the **WordPress source site**, not on PageMotor.

1. Download `ep-wp-exporter.zip` from the [EP Suite downloads release](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/tag/latest).
2. In the WordPress admin, go to **Plugins → Add New → Upload Plugin**.
3. Upload the zip and activate.
4. Run the export (see below).
5. **Uninstall when finished.** The plugin is needed only during the migration window.

## Running an export

1. In the WordPress admin, go to **Tools → EP WP Export**.
2. Tick the export options you want. The defaults are sensible — posts, pages, comments, menus, widgets, media manifest, theme settings.
3. Tick **Focus Cards** if you are migrating a Thesis Focus site that uses the Focus Cards feature. This guarantees the `focus_cards` custom post type and `focus_cards` theme option are included even if you didn't tick the broader Custom Post Types and Theme Settings boxes.
4. Click **Export for PageMotor**.
5. A JSON file is streamed to your browser as a download. The filename is `<site-slug>-ep-wp-export-YYYY-MM-DD.json`.

The export runs synchronously and downloads in one shot, so for very large sites you may need to bump WordPress's PHP `memory_limit` and `max_execution_time` temporarily.

## What you do with the JSON

The JSON is what the PageMotor side of the migration consumes. Different migration paths use it differently:

- **PageMotor migrator CLI** (`pagemotor-migrator`) — point it at the JSON and it provisions a PageMotor install with content, menus, theme settings, and Focus Bridge skinning where appropriate.
- **Manual import scripts** — the `wp-to-pm-migration` runbook in the ElmsPark workspace uses parameterised PHP importers that read the JSON and `UPSERT` content into a PageMotor site by slug.
- **EP Cards Importer** — if Focus Cards were included, the [EP Cards Importer](/plugins/ep-cards-importer/) add-on reads `custom_post_types.focus_cards` and `theme.focus.options.focus_cards` to convert them to native EP Cards.

## Relationship to other plugins

- **[EP Cards Importer](/plugins/ep-cards-importer/)** depends on the Focus Cards section of this export.
- **`pagemotor-migrator`** (CLI tool, not on PageMotor) is the canonical consumer of this JSON for full-site migrations.

## Troubleshooting

### “The export times out on a large site”

The exporter runs in a single PHP request. Raise `memory_limit` (try 512M) and `max_execution_time` (try 300) in `php.ini` or via `.htaccess`, then re-run. If the site is truly huge, export sections one at a time by unticking the heaviest options on separate runs.

### “The downloaded file is empty or truncated”

Almost always a PHP timeout or memory issue mid-request. Check the WordPress error log, raise PHP limits, retry.

### “Focus Cards aren't in the export”

Tick the **Focus Cards** checkbox explicitly. The exporter will include `custom_post_types.focus_cards` and `theme.focus.options.focus_cards` even if you didn't tick Custom Post Types or Theme Settings, and it sets `_focus_cards_included: true` at the top level so the importer can verify.

### “The plugin shows nothing in Tools → EP WP Export”

The plugin uses `add_management_page` with the `manage_options` capability. You must be logged in as a WordPress administrator, not an editor or author.

## Removing the plugin

When the migration is done, deactivate and delete EP WP Exporter from the WordPress source site. It has no database tables, no options, and no scheduled events to clean up.

## Feedback and corrections

If something is wrong in this guide, or you've spotted a behaviour the plugin should expose differently, please email [help@elmspark.com](mailto:help@elmspark.com).
