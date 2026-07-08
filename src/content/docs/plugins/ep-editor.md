---
title: "EP Editor"
description: "Visual inline page editor for PageMotor. Admins click text on the live site and edit in place with a floating toolbar. No admin panel trip required. Work in progress."
---

EP Editor puts a frontend inline editor on your live site for admins. Click **Edit Page**, click any text, get a floating toolbar, type directly into the page. Changes save back to the database without ever opening the admin panel.

Published by [ElmsPark Studio](https://elmspark.com).

## Status

**Work in progress** (version 0.1.12). Core inline editing is stable and the plugin is fully compatible with PageMotor 0.10; layout editing and richer element handling are roadmap items. This guide describes what currently ships.

## Overview

- **Click-to-edit** text elements directly on the live page, behind an explicit **Edit Page** toggle — browsing stays browsing until you ask to edit.
- **Floating formatting toolbar** on text selection: bold, italic, links, Heading 2, Heading 3 and paragraph, with the usual keyboard shortcuts (Ctrl/Cmd+B, Ctrl/Cmd+I, Ctrl/Cmd+K).
- **Undo and redo** while editing — Ctrl/Cmd+Z and Shift+Ctrl/Cmd+Z, per edited region — plus a **Discard** that restores the page exactly as it loaded.
- **Paste sanitisation.** Pasted content is stripped to a small whitelist of clean tags (paragraphs, headings, lists, links, images), so Word and Google Docs baggage never lands in your content.
- **Shortcode and embed protection.** Plugin output, video/audio embeds and other generated markup are detected and locked — the editor only offers text it knows how to save safely.
- **Admin-only** — non-admin visitors never see the editor; the script isn't even loaded for them.
- **Saves to PageMotor content**, no separate content table: the main page content, the text between shortcodes (the shortcode tags themselves are preserved untouched), and theme HTML Box instances.

## What EP Editor cannot do (yet)

This plugin intentionally has a narrow scope in the 0.1.x line. It does not:

- **Edit theme elements** (header, footer, navigation, sidebars). Those still live in the admin Theme Editor. Theme HTML Boxes are the exception — their content is editable.
- **Handle drag-and-drop layout changes.** Repositioning blocks is done through the admin.
- **Upload images from the frontend.** Image replacement has to go through the admin's image upload path.

Roadmap items. When they ship, this guide will be expanded.

One deliberate exclusion that is not a roadmap item: **shortcode output and media embeds are locked**, because editing rendered plugin output would overwrite the shortcode on save. Edit the shortcode itself in the admin instead.

## Requirements

- **PageMotor 0.8.2b or later** — fully compatible with PageMotor 0.10, including its central `X-CSRF-Token` enforcement.
- **EP Suite base class** (bundled)

## Installation

1. `ep-editor.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Editor** and tick **Enabled**.
4. Visit any page on your site while logged in as admin. Click the **Edit Page** button, then click any text to start editing.

## Settings

- **Enabled.** Toggle the visual editor on the frontend for admins. Turn off if you want to view the site as a visitor would, without editing UI.

## How it works

When an admin loads a page:

1. PageMotor renders the page normally, and EP Editor adds a floating **Edit Page** button. Admins only — for everyone else the script never loads.
2. Clicking **Edit Page** scans the page for editable regions: the main content, the text between shortcode output, and theme HTML Boxes. Shortcode-generated markup and media embeds are excluded. If nothing on the page qualifies, the editor says "Nothing editable on this page" rather than offering something it can't save.
3. Clicking into a region lets you type in place; selecting text reveals the floating toolbar.
4. **Save** posts the changed regions to EP Editor's own admin-only endpoint, CSRF-checked (on PageMotor 0.10 that includes the core `X-CSRF-Token` request header). The server strips scripts and inline event handlers before writing, and text edited between shortcodes is stitched back around the original shortcode tags so they survive exactly as written.
5. **Exit Editor** leaves edit mode; leaving with unsaved changes asks you to confirm first.

## Troubleshooting

### “I don't see the Edit Page button”

Check **Settings → EP Editor → Enabled** is on, and that you're logged in as an admin. Refresh the page. Check the browser console for JS errors.

### “I clicked text but nothing happens”

Not every text element is editable. Content rendered from shortcodes or plugin output, and media embeds, don't map cleanly to a saveable field, so the editor deliberately doesn't attach to them. If the whole page is generated content, you'll see "Nothing editable on this page".

### “The editor opens but changes don't save”

If your site is on PageMotor 0.10, make sure EP Editor is **0.1.11 or later** — PM 0.10 moved CSRF enforcement to a central request header, and older EP Editor builds could open and type but had every save rejected. Your site's **Updates** screen serves the current build. Otherwise, check the network tab during save: the error message tells you why. Common causes are an expired session or a security token gone stale after the page sat open for hours — reload and try again.

### “I edited the wrong thing by accident”

Press Ctrl+Z (Cmd+Z on a Mac) to undo, or Shift+Ctrl/Cmd+Z to redo — each edited region keeps its own undo history while the editor is open. If you haven't saved yet, **Discard** restores the whole page exactly as it loaded. If you already saved, restore from PageMotor's revision history if your install keeps them.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
