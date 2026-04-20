---
title: "EP Cards"
description: "Native card groups and grids for PageMotor with LLM-driven import, per-card style overrides, image upload, and a public API."
sidebar:
  order: 2
---

EP Cards adds a proper card component to PageMotor. Groups, grids, per-card styling, image upload, and an LLM-driven import path that lets you hand a prompt to any AI, paste the JSON back, and get a fully-styled card group in one step. Built to reach full feature parity with Thesis Focus Cards so sites migrating from WordPress can keep their existing card content.

Published by [ElmsPark Studio](https://elmspark.com). This guide covers the standalone plugin. For migrating an existing Thesis site, see the [EP Cards Importer](#migrating-from-thesis-focus-cards) section near the end.

## Overview

A card is a compact panel with an image, title, subtitle, body text, and up to three independent links. A group is a named collection of cards rendered together as a grid (two, three or four columns).

What you get:

- **Groups and grids.** Create any number of groups, drop a shortcode on any page, render as a 2, 3 or 4-up grid.
- **Per-card or global styling.** Four shadow styles, six corner radius levels, three spacing levels, hover-raise, light and dark backgrounds, custom colours, three font options, bold or normal weight. Set globally, override per card.
- **Three link slots.** Whole-card link, title-only link, image-only link. The renderer guarantees no nested `<a>` tags whichever combination you choose.
- **Native image upload.** Drag-and-drop or click-to-browse directly in the card edit form. Files land under `user-content/uploads/ep-cards/` with MIME and extension filtering.
- **LLM-driven JSON import.** Download a prompt, paste it into Claude or ChatGPT, describe the cards you want, upload the returned JSON. Groups, cards, and styles created in one step with one-click rollback if you want to start over.
- **Thesis Focus Cards migration.** The optional EP Cards Importer add-on reads the JSON produced by the EP WP Exporter and writes your existing Focus Cards content into EP Cards, with image rehosting.
- **Public PHP API.** Commit import plans, roll back batches, render groups programmatically.

## Installation

Standard PageMotor plugin install, under a minute.

1. **Download.** Grab `ep-cards.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest) or the link in your ElmsPark account.
2. **Sign in to your PageMotor admin** at `yourdomain.com/admin/`.
3. **Go to Plugins, then Manage Plugins.**
4. **Upload the zip.** PageMotor extracts it to the correct location automatically.
5. **Activate in your Theme.** Enable EP Cards in your active Theme's plugin configuration. Database tables are created on first load.

**How to verify:** after activation, go to **Plugins then Plugin Settings** and open **EP Cards**. You should see five sections: Generate Cards with AI, Groups & Cards, Global Defaults, Import History, and Usage. If those appear, you are installed and ready.

Requires **PageMotor 0.8.2b or later**.

## Creating cards

Three ways, in order of speed for real projects.

### 1. LLM-driven JSON import (fastest for more than a couple of cards)

This is the primary design-input path, and the one to reach for whenever you have more than two or three cards to build.

1. Open the EP Cards settings page and scroll to **Generate Cards with AI**.
2. Click **Download LLM prompt**. You get a single markdown file.
3. Paste the whole file into Claude, ChatGPT or any other LLM, then describe the cards you want. For example: *"Six service cards for a bookkeeping firm, each with a short subtitle, a two-sentence description, and a Read more link to a placeholder URL. Use the services-grid sample layout."*
4. The LLM returns JSON. Copy it, save as a `.json` file, or paste it directly into the upload dialog.
5. Back on the settings page, click **Upload JSON**, pick the file, then click **Preview Import**.
6. Review what the preview shows: groups to create, sample cards rendered, any warnings.
7. Click **Import these cards** to commit. All groups, cards, and style settings are written as a single batch. If anything looks wrong after, use **Import History** to roll the whole batch back with one click.

The prompt file includes three worked examples (services grid, team cards, image-only portfolio) and full schema documentation. Sample JSONs for each example ship with the plugin and can be downloaded from a dropdown next to the prompt button.

### 2. Manual card edit form

For one or two cards or small tweaks, the hand-built path is usually faster than the LLM round-trip.

1. On the settings page, find **Groups & Cards**.
2. Type a title in **New group title** and click **Create Group**.
3. Click **View cards** next to the new group, then **+ Add Card**.
4. Fill in the inline form. **Only Title is required.** Everything else is optional:
   - Subtitle
   - Body (basic HTML allowed)
   - Image (drag-and-drop, click to upload, or paste a URL)
   - Alt text
   - Whole-card link URL, and optional title-only and image-only link alternatives
   - Display flags: Centered, Hide title, Image only
   - Per-card style overrides under the collapsible section (leave blank to inherit the site's global defaults)
5. Click **Create**. The card appears in the list with Edit, Duplicate and Delete buttons on every row.

The shortcode hint above the card list gives you the exact `[ep_card_group]` markup to paste on any page.

### 3. Importing from a WordPress Thesis site

If you are migrating a Thesis Focus Cards site, use the EP Cards Importer add-on. See [Migrating from Thesis Focus Cards](#migrating-from-thesis-focus-cards) below.

## Image upload

From v1.0.5 onwards, the Image field in the card edit form uses PageMotor's native upload widget.

- **Drag and drop** an image onto the drop zone, or click to browse.
- **Paste a URL** directly into the URL input if your image is already hosted elsewhere.
- **Alt text** has its own input and should be filled in for anything meaningful to screen readers.

Supported types: JPG, JPEG, PNG, GIF, WebP, SVG. Files land in `user-content/uploads/ep-cards/` on your server. Server-side filtering rejects anything that is not in the allowed list, including server-executable extensions regardless of client-side claims.

## Shortcodes

Two shortcodes. One for a single card, one for a group.

```text
[ep_card id=1]
[ep_card_group group=services grid=3]
[ep_card_group ids="1,4,7" grid=2 constrain=1]
[ep_card_group group=team grid=4 card_class=team-card]
```

### `[ep_card id=N]`

Render one card by its database ID. The card ID is shown next to each card title in the admin list.

### `[ep_card_group]` attributes

| Attribute | Values | Purpose |
|---|---|---|
| `group` | group slug | Render every active card in this group in sort order. |
| `ids` | comma-separated IDs | Render an explicit list of cards in the order given. Overrides `group` if both are set. |
| `grid` | 2, 3 or 4 | Number of columns. Defaults to the site's global setting. |
| `constrain` | 1 | Keep the grid inside the content column instead of breaking out to a wider page width. |
| `class` | string | Extra CSS class added to the outer group wrapper. |
| `card_class` | string | Extra CSS class added to each card inside the group. |
| `equal_heights` | 0 or 1 | Force all cards in a row to match the tallest card. Override the global default for one placement. |

## Styling

Global defaults live in the **Global Defaults** section of the settings page: style (shadow), corners, spacing, hover, fonts, colours, equal heights. Set once, applies to every card unless a specific card overrides.

Per-card overrides are on every card's edit form under **Per-card style overrides**. Leave any field blank and that card inherits the global default for that property. This is deliberate: you can bump the global corner radius on a whim without touching individual cards.

Valid values for each property:

| Property | Values |
|---|---|
| Style (shadow) | `standard`, `soft`, `subtle`, `flat` |
| Corners | `x6` (largest), `x5`, `x4`, `x3`, `x2` (smallest), `square` |
| Spacing | `x2` (compact), `x3` (comfortable), `x4` (generous) |
| Hover | `none`, `raised` |
| Title font | `f1`, `f2`, `f3` (mapped to your theme fonts) |
| Title weight | `normal`, `bold` |

Background and text colours accept any CSS colour value. Dark card backgrounds automatically swap text to light per the `text_color` setting if you set it; otherwise the renderer picks a legible default.

## LLM JSON import

The schema, rules, and three worked examples all live inside the prompt file itself so the LLM has everything it needs in one paste.

Validation on import:

- Unknown top-level keys are rejected.
- Every enum field (style, corners, spacing, hover, weight, font) is checked against the whitelist. Invalid values become null, which means "inherit global default" rather than failing the import.
- URL fields are scheme-checked. Non-http(s) URLs are rejected.
- Body HTML is sanitised through a fixed allowlist: `p`, `br`, `strong`, `em`, `a`, `ul`, `ol`, `li`, `span`, `img`, `h2`, `h3`, `h4`, `blockquote`, `code`. Anything else is stripped.
- Cards that reference an unknown `group_slug` are demoted to ungrouped with a warning, rather than failing the whole import.

Every import is stamped with a batch UUID. The **Import History** section shows every batch with a Delete button next to each. Click it and the cascade-delete removes every group and card written by that batch in one step.

### Extending the prompt from another plugin

Any active plugin can contribute a section to the generated prompt:

```php
public function ep_cards_llm_prompt_section() {
    return [
        'heading' => 'My Plugin Notes',
        'markdown' => "Tell the LLM something useful about how my plugin interacts with cards."
    ];
}
```

EP Cards Importer uses this to tell the LLM that imported cards may already exist on the site, so it doesn't recreate them.

## Migrating from Thesis Focus Cards

Optional add-on: [EP Cards Importer](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/download/latest/ep-cards-importer.zip). Install alongside EP Cards and both plugins coordinate automatically.

The workflow:

1. On the source WordPress site, install [EP WP Exporter](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest) and export your Focus Cards content as JSON.
2. On the target PageMotor site, install EP Cards and EP Cards Importer.
3. From the importer settings page, upload the JSON file.
4. The importer rehosts every featured and inline image locally (idempotent, so re-running does not duplicate), then writes groups, cards, and style settings through the EP Cards public API as a single batch.
5. Review, and if anything is wrong, one-click rollback.

## Public API

For plugin authors and bespoke integrations.

```php
// Commit any ImportPlan into the DB inside a single batch.
// Used by both LLM JSON import and EP Cards Importer.
$core = $motor->theme->_plugins->active['EP_Cards'];
$result = $core->commit_import_plan($plan, EP_Cards_Batch::SOURCE_LLM_JSON, $label);
// Returns: ['ok' => bool, 'batch_id' => string, 'stats' => ['groups' => N, 'cards' => N]]

// Cascade-delete every group and card stamped with this batch id.
$core->rollback_batch($batch_id);

// Get the renderer pre-configured with site-level global defaults.
$renderer = $core->get_renderer();
$html = $renderer->render_card($card_row);
$html = $renderer->render_card_group($cards, ['grid' => 3, 'constrain' => false]);
```

### Database tables

| Table | Purpose |
|---|---|
| `{prefix}ep_cards_groups` | Group taxonomy. Carries `import_batch_id` for rollback. |
| `{prefix}ep_cards` | Cards. 27 columns including all style overrides as nullable VARCHAR, so adding a new style value never needs an `ALTER TABLE`. |
| `{prefix}ep_cards_import_batches` | One row per import. Every imported group and card stamps `import_batch_id` with this UUID. |

### Hard guarantee: no nested `<a>` tags

The renderer resolves whole-card, title-only, and image-only link slots so you can never emit nested anchors. The root element becomes an `<a>` if and only if `link_url` is set AND both `title_link` and `image_link` are empty. Any other combination renders the root as `<div>` with the link slots attached to their specific elements only. This matters because nested anchors are invalid HTML that many browsers and accessibility tools handle unpredictably.

## Troubleshooting

### "I created a group but the card won't save"

The single most common cause is the **Title** field. Title is the only required field on the Add Card form. If it is blank, the browser silently blocks the submit and shows a tooltip on the Title input that is easy to miss. Fill in a Title, even a short placeholder, and it will save. Everything else, subtitle, body, image, links, is optional.

### "The image I pasted doesn't appear"

Check the URL resolves in a browser. If you are pasting a URL from a site that blocks hotlinking, the card will save but the image will be broken. Download the image and re-upload it instead, or use the EP Cards Importer on your source site to rehost.

### "The global defaults I set don't seem to apply"

Per-card style values win over global defaults. If you set a per-card value during testing and forgot about it, that card will ignore the global default forever. Open the card, expand **Per-card style overrides**, and set each property back to `(inherit global)` or blank.

### "My shortcode isn't rendering anything"

Check two things:
- The `group` attribute uses the group's **slug**, not its **title**. The slug is shown under the group title in the admin, and in the shortcode hint above the card list.
- The group has at least one active card. If you have only draft cards, the group renders empty.

### "I want to delete one bad import batch but not everything"

Open the EP Cards settings page and scroll to **Import History**. Every import batch has a Delete button. Clicking it cascade-deletes only the groups and cards written by that specific batch. Other cards, even in the same group, are untouched.

### "How do I upload an image without paying for external hosting"

Since v1.0.5, the card edit form has a native drop zone. Drag a file onto it or click to browse. Files are stored locally under `user-content/uploads/ep-cards/` on your own server.

### "Can I override the grid column count for one specific placement"

Yes. The `grid` attribute on the shortcode overrides the global default. Use `[ep_card_group group=services grid=4]` to force four columns on one page even if your global is three.

## Feedback and corrections

Found a bug or a missing detail in this guide? Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues) or send feedback to the forum. Corrections land quickly; we treat the guide as living documentation.
