---
title: "EP Editor"
description: "Visual inline page editor for PageMotor. Admins click text on the live site and edit in place with a floating toolbar. No admin panel trip required. Work in progress."
sidebar:
  order: 23
---

EP Editor puts a frontend inline editor on your live site for admins. Click any text, get a floating toolbar, type directly into the page. Changes save back to the database without ever opening the admin panel.

Published by [ElmsPark Studio](https://elmspark.com).

## Status

**Work in progress** (version 0.1.3). Core inline editing works; layout and richer element handling are roadmap items. This guide describes what currently ships.

## Overview

- **Click-to-edit** text elements directly on the live page.
- **Floating formatting toolbar** appears when you select text.
- **Admin-only** — non-admin visitors never see the editor, it simply doesn't load for them.
- **Saves to PageMotor content** through the standard admin API, no separate content table.

## What EP Editor cannot do (yet)

This plugin intentionally has a narrow scope at v0.1.3. It does not:

- **Edit theme elements** (header, footer, navigation, sidebars). Those still live in the admin Theme Editor.
- **Handle drag-and-drop layout changes.** Repositioning blocks is done through the admin.
- **Upload images from the frontend.** Image replacement has to go through the admin's image upload path.

Roadmap items. When they ship, this guide will be expanded.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**

## Installation

1. Download `ep-editor.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Editor** and tick **Enabled**.
4. Visit any page on your site while logged in as admin. Click any text to start editing.

## Settings

- **Enabled.** Toggle the visual editor on the frontend for admins. Turn off if you want to view the site as a visitor would, without editing UI.

## How it works

When an admin loads a page:

1. PageMotor renders the page normally.
2. EP Editor's JS detects the admin session and attaches click handlers to editable elements.
3. Clicking an element reveals the floating toolbar.
4. Typing changes the DOM in place.
5. On blur (or explicit Save), the change is POSTed to a PageMotor content-update endpoint.

Non-admin visitors never trigger any of this. The plugin checks auth on page load and bails out if the user isn't logged in as admin.

## Troubleshooting

### "I don't see the toolbar when I click text"

Check **Settings → EP Editor → Enabled** is on. Refresh the page. Check the browser console for JS errors.

### "I clicked text but nothing happens"

Not every text element is editable. Some content is rendered from shortcodes or plugin output and doesn't map cleanly to a saveable field. The editor only attaches to elements it knows how to save.

### "Changes don't persist"

Check the network tab during save. If the save request fails, the error message tells you why. Common causes: session expired, CSRF token invalid after sitting open for hours.

### "I edited the wrong thing by accident"

Undo is not currently supported in the inline editor. Reload the page before saving to discard changes. If you already saved, restore from PageMotor's revision history if your install keeps them.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
