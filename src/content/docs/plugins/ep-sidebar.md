---
title: "EP Sidebar"
description: "Activates PageMotor's sidebar layout with manageable widget blocks. Pick which pages get sidebars and which widgets they contain."
sidebar:
  order: 51
---

EP Sidebar activates PageMotor's built-in sidebar layout and gives you an admin UI to manage which widgets appear in it. Sidebars can be site-wide or per-page. Widget types include recent posts, text blocks, menu, RSS feed, and custom HTML.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Enable the sidebar** for your active theme. PageMotor supports sidebar layouts natively; this plugin makes them configurable.
- **Widget management** — drag-and-drop arrangement of widgets.
- **Per-page sidebar toggle** — some pages have sidebars, some don't.
- **Widget types**:
  - **Text/HTML.** Arbitrary content.
  - **Menu.** A navigation menu.
  - **Recent posts.** Most recent blog posts.
  - **RSS feed.** External feed content.
  - **Shortcode.** Runs any shortcode inside the widget.

## Requirements

- **PageMotor 0.7 or later**
- **EP Suite base class**
- **A theme that supports sidebar layouts** (most PageMotor themes do).

## Installation

1. Download `ep-sidebar.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open your Theme's configuration and enable the sidebar layout.
4. Go to **Plugin Settings → EP Sidebar → Widgets** to add widgets.

## Adding widgets

From the Widgets panel:

1. Click **Add Widget**.
2. Pick a widget type.
3. Configure it — text body, menu selection, feed URL, shortcode name, etc.
4. Save.
5. Drag to reorder. Order is top-to-bottom in the sidebar.

## Per-page control

On any page's content options:

- **Show sidebar.** On / off / use site default.

If off, the page renders without a sidebar even though the theme supports it. Useful for landing pages where you want full-width focus.

## Widget type details

### Text/HTML

Free-form block. Use for "About this site", contact info, legal notices, anything static.

### Menu

Pick from the menus you've defined in your theme. Renders the menu items in the sidebar. Good for a "Categories" list or a secondary navigation.

### Recent posts

Shows the most recent N posts (configurable count). Filter by category if you have them.

### RSS feed

Paste a feed URL. Widget shows the feed title and latest N items. Useful for embedding your podcast feed, a partner's blog, etc.

### Shortcode

Wraps any shortcode in a widget. Examples:

- `[newsletter-form]` — subscription form in the sidebar.
- `[ep-analytics]` or similar custom shortcodes.

## Troubleshooting

### "Sidebar doesn't appear on my site"

Check the theme's layout is set to include a sidebar. EP Sidebar activates the layout but the theme has to support it. Some landing-page themes deliberately don't.

### "Widgets show in admin but nothing on the front end"

Check **Per-page Show sidebar** isn't set to off globally. Also double-check the theme layout.

### "RSS widget is empty"

The feed URL is unreachable, or the feed is malformed. Test the feed URL in a browser — should see XML.

### "Menu widget shows the wrong items"

Your menu was updated but the widget still references the old one. Re-pick the menu in the widget settings.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
