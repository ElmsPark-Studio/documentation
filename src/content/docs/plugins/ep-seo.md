---
title: "EP SEO"
description: "Open Graph, Twitter Card, favicon, and Person/Organization structured data for any PageMotor site. Settings-driven, sitewide."
sidebar:
  order: 50
---

EP SEO adds the SEO essentials PageMotor's core Open Graph plugin doesn't cover: a dedicated favicon override, Person or Organization JSON-LD structured data, and a sitewide social image with stored dimensions. All settings-driven, no per-page configuration required.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP SEO does

- **Open Graph tags** in the head — `og:title`, `og:description`, `og:image`, `og:url`, `og:site_name`, `og:type` — so link previews on Facebook, LinkedIn, Slack, Discord, and WhatsApp render correctly.
- **Twitter Card tags** — `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` — for previews on X.
- **Favicon override** — point to any SVG or PNG; replaces the default PageMotor favicon site-wide.
- **Person or Organization JSON-LD** — emits `Person` or `Organization` schema at `#organization` so search engines understand who's behind the site.
- **Page title formatting** — non-home pages get titled "Page Title | Site Name".

## What EP SEO doesn't do

- **LocalBusiness schema** — that's [EP Local Business](/plugins/ep-local-business/), an optional add-on.
- **Multi-location schema** — that's [EP Locations](/plugins/ep-locations/).
- **Per-page overrides** — sitewide defaults only. PageMotor's core Open Graph plugin already covers per-page social image overrides.
- **Keyword research, content auditing, rank tracking.** Those are strategy and tooling problems, not plugin problems.

## Requirements

- **PageMotor 0.7 or later.**

## Installation

1. Download `ep-seo.zip` from your EP Suite distribution.
2. Upload via **Plugins → Manage Plugins**.
3. Activate.
4. Open the plugin's settings page and fill in the two sections.

## Settings

### Site Identity

- **Site Name.** Used for `og:site_name` and as the suffix on page titles. Falls back to PageMotor's site title if left empty.
- **Default Description.** Used as `og:description` and `twitter:description` on every page. Keep it under 160 characters for best results.
- **Open Graph Image.** Drag-and-drop upload. 1200×630 is the standard size. Image dimensions are stored on upload, so `og:image:width` and `og:image:height` are emitted automatically — no runtime fetching required.
- **Favicon URL.** Full URL to your favicon (SVG or PNG). Overrides the default PageMotor favicon by patching the bundled Favicon plugin's settings at runtime.

### Structured Data

- **Schema Type.** Choose `Person` for individual professionals or freelancers, `Organization` for businesses, or `None` to skip JSON-LD entirely.
- **Name.** Full name of the person or organisation.
- **Job Title.** Person schema only — ignored for Organization.
- **Description.** Short description used in the schema.
- **URL.** Defaults to your site URL if left empty.

The emitted schema lives in the sitewide `@graph` at `@id = <site_url>#organization`.

## Coexistence with EP Local Business and EP Locations

EP SEO 1.4 yields its Organisation branch when *either* of two sibling plugins owns the `#organization` node:

- [EP Local Business](/plugins/ep-local-business/) — single-location businesses. In its default **merged** coexistence mode, EP SEO yields and EP Local Business emits one combined `["Organization", "LocalBusiness"]` node at `#organization` folding in EP SEO's name, URL, description, plus all the LocalBusiness extras.
- [EP Locations](/plugins/ep-locations/) — multi-location chains. In its default **merged** coexistence mode, EP SEO yields and EP Locations emits one combined `Organization` parent at `#organization` plus per-branch `LocalBusiness` nodes back-referencing it.

The two are mutually exclusive at runtime: EP Local Business defers entirely whenever EP Locations is installed, so only one ever owns the node. In **additive** mode, EP SEO emits its Organisation node unchanged and the sibling adds its LocalBusiness node alongside with a `parentOrganization` back-reference.

The handshake is one-way: EP SEO checks for both siblings; neither sibling needs to check for EP SEO. Any combination works fine in isolation.

## Privacy and EP GDPR

EP SEO makes no third-party calls. Open Graph tags, Twitter Card tags, favicon links, and JSON-LD structured data are all rendered server-side from settings the admin entered. No external service is contacted, no visitor data is collected, no cookies are set. EP SEO is GDPR-neutral and does not need consent gating.

If you install [EP Local Business](/plugins/ep-local-business/) or [EP Locations](/plugins/ep-locations/) alongside EP SEO, those plugins handle their own GDPR integration for the third-party services they use (OSM Nominatim geocoding, MapTiler Cloud map tiles).

## Troubleshooting

### "Link preview on Facebook shows the old image"

Facebook caches Open Graph data aggressively. Use their [Sharing Debugger](https://developers.facebook.com/tools/debug/) to scrape the page again and force a refresh.

### "Twitter/X link preview is broken"

Test the URL in [the Card Validator](https://cards-dev.twitter.com/validator). Common causes: the OG image URL is wrong, the image is too small (Twitter wants at least 300×157 for `summary_large_image`), or the image is blocked by robots.txt.

### "Favicon doesn't update after I changed the URL"

Browsers cache favicons aggressively. Try a hard refresh (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows), or open the page in incognito mode, or in a different browser. If still wrong, view the page source and confirm the favicon URL in the head is the new one.

### "Rich Results Test shows 'unnamed property' warnings"

A required field on your schema is empty. If you've set Schema Type but left Name blank, the schema is missing the required `name` property. Fill in Name (and URL, which defaults to your site URL anyway) and re-test.

### "I want to skip rich metadata on a specific page"

EP SEO doesn't have per-page overrides. PageMotor's core Open Graph plugin handles per-page image overrides via Content Options. For schema control on individual pages, EP SEO's sitewide approach assumes you want consistent identity metadata everywhere — which you usually do.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
