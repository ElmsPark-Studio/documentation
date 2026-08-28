---
title: "EP Membership Pages"
description: "Companion to EP Membership. Themed, level-protected Members Pages whose refusal is your upgrade prompt, not a 404."
---

EP Membership Pages is the companion to [EP Membership](/plugins/ep-membership/) for sites selling tiered access. It adds a **Members Page** content type: a normal themed page of your site that PageMotor itself refuses to visitors below the level you set. When someone is refused, they do not get a dead end. A visitor with no session sees a login prompt; a signed-in member below the level sees **your upgrade message, naming the tier the page needs**, rendered inside your site's normal design.

Published by [ElmsPark Studio](https://elmspark.com).

## What it adds

- **Members Page content type**: templated (renders in your theme) and protected at the content layer. A page on it is refused by PageMotor itself, so its text is absent from the public API, the XML sitemap and site search, and files attached to it stay private. The same airtight mechanism as EP Membership's Members Only documents; different rendering, different refusal.
- **The Membership Gate box**: a container you place once in your theme template, where page content renders. It is what speaks when PageMotor refuses a Members Page. Without it, refusals fall back to PageMotor's plain wording, and the plugin shows a dismissible admin notice reminding you to place it.
- **Level-aware refusal copy**: the upgrade prompt names the required level using the labels you defined in EP Membership. Both messages can be overridden in settings.

## How it relates to EP Membership

Levels are defined **once, in EP Membership**, and this plugin reads them. A member's access is decided by PageMotor's own content-layer check against the level keys EP Membership grants, so everything EP Membership counts towards a level, purchase grants included, works here automatically, and a vip member passes a pro gate with no extra configuration.

The two protected types never interact. Content is authored onto one or the other, the same way you choose between a Page and an HTML document:

| | Members Only document (EP Membership) | Members Page (this plugin) |
|---|---|---|
| Renders as | a standalone document, verbatim | a normal themed page |
| When refused | login screen, or a 404 | login prompt, or **your upgrade pitch** |
| Best for | handbooks, downloads, anything verbatim | articles, lessons, anything you sell tiers of |

## Requirements

- **PageMotor 0.11 or later.**
- **EP Suite base class** (bundled).
- **[EP Membership](/plugins/ep-membership/)** with levels defined. Without levels, Members Pages are staff-only (fail-closed) and a breadcrumb is written to the PHP error log.

## Installation

1. Install and activate alongside EP Membership. There is nothing to configure twice: the plugin finds your levels.
2. Place the **Membership Gate** box in your theme template where page content renders (Theme → Template Editor). This is the step that gives the plugin its voice; until it is done, refusals use PageMotor's default wording and the admin shows a reminder.
3. Optionally set the **Members Page Level** in settings (blank means any signed-in member).
4. Create a Members Page, or move an existing page onto the type, and it is protected.

## Settings

- **Members Page Level** — minimum EP Membership level (slug, e.g. `pro`) required to view Members Pages. Blank = any signed-in member.
- **Logged-out Message** — shown with a log-in link to visitors with no session. Blank = default wording.
- **Upgrade Message** — shown to a signed-in member below the required level. Blank = default wording naming the required level. This is your sales pitch: name what the tier includes.

## Troubleshooting

### "A refused page shows 'You do not have permission to view this content' instead of my message"

The Membership Gate box is not placed in the template that renders your pages, so PageMotor's default wording is answering instead. Place the box (Theme → Template Editor) where page content renders.

### "Members Pages show as staff-only / nobody can see them"

No levels are defined in EP Membership, so the type fails closed. Define levels in EP Membership's **Member Levels** settings; the plugin picks them up on the next load.

### "A member who should have access is refused"

Check their effective level in EP Membership's Members panel against the **Members Page Level** here. Access is decided from the level keys EP Membership grants, so an expired purchase grant lowers access immediately.

## Changelog

### 0.2.0

27 August 2026. PageMotor 0.11.2 compatibility: update this plugin before or with the core update, or every Members Page locks out every member. Accepted keys now declared in both bare and scoped forms (one file, both cores), and the refusal copy moves to 0.11.2's Dynamic Denials, with the retired valet kept for 0.11.1b so both cores render identical copy. The Membership Gate box is still required. Rig-proven on both cores, full four-visitor matrix each.

### 0.1.0

26 August 2026. First release. The Members Page content type (templated, level-protected at the content layer), the Membership Gate box with level-aware refusal copy, settings for the minimum level and both messages, fail-closed behaviour without levels, and the unplaced-box admin notice. Verified end to end on a PageMotor 0.11.1b rig with real member sessions: anonymous refused to a login prompt, a free member refused to an upgrade prompt naming the required level, a vip member passing a pro gate through the level cascade, and the page absent from the sitemap and refused by the public content API.

## Feedback and corrections

For a quick question, **EP Support** inside your admin is the fastest option. For anything bigger, open a ticket at [help.elmspark.com](https://help.elmspark.com).
