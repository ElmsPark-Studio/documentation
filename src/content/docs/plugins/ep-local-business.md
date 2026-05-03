---
title: "EP Local Business"
description: "Schema.org LocalBusiness emission for single-location businesses on PageMotor. Address, hours, geo, payment methods, areas served, and a coexistence handshake with EP SEO."
sidebar:
  order: 32
---

EP Local Business adds a complete Schema.org LocalBusiness JSON-LD node to a single-location PageMotor site. Address, opening hours, geo coordinates, payment methods, areas served, per-page subtype overrides. Coordinates with EP SEO so you don't end up with two competing Organization nodes on the page, and yields entirely to EP Locations on multi-location installs.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP Local Business does

- Emits a Schema.org `LocalBusiness` (or any chosen subtype) JSON-LD node on every page of a single-location site
- Picks the right Schema.org type from a curated dropdown (Restaurant, MedicalBusiness, ProfessionalService, etc.) or accepts a free-text custom subtype
- Captures business identity (name, description, URL, telephone, email, logo, social profile URLs)
- Captures structured postal address (street, locality, region, postcode, country)
- Captures geo coordinates (latitude / longitude) with a one-click "Look up coordinates from address" helper that uses OpenStreetMap Nominatim
- Hours grid with seven-day input, supports overnight hours that split automatically into two Schema.org entries on emission (e.g. 22:00–02:00 → Mon 22:00–23:59 + Tue 00:00–02:00)
- Captures payment methods, currencies accepted, price range, areas served
- Two coexistence modes for sites running EP SEO: **merged** (single combined Organization+LocalBusiness node) or **additive** (LocalBusiness as separate node referencing the Organization)
- Six EU language translations of the entire admin UI

## What EP Local Business doesn't do

- **Multi-location.** If your business has more than one branch, install EP Locations instead. EP Local Business defers entirely to EP Locations when both are active — they're mutually exclusive at runtime.
- **Reviews / aggregateRating.** Out of scope for v1.1; planned for a later version.
- **Service catalogue / Offer schema.** Out of scope for v1.1; planned for a later version.

## Requirements

- **PageMotor** 0.8 or later
- **EP Suite** base class (auto-loaded with any EP plugin)
- **EP SEO** (optional but recommended) — coordinates the Organization node so there's no duplication. EP Local Business works fine standalone if EP SEO is not installed.

## Installation

1. Download the latest `ep-local-business.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. In PageMotor admin go to **Plugins → Manage Plugins → Upload**, select the zip, and activate.
3. Click **EP Local Business** in the admin nav. The first thing to set is the Master Switch (off by default — schema only emits when you've filled in the basics and turned it on).

## Settings

### Master Switch

Single tickbox. Off by default. Once your business identity and address are filled in, tick this and save to start emitting LocalBusiness JSON-LD on every page.

### Business

- **Business name** — the trading name as it should appear in search results
- **Schema.org type** — pick the most specific subtype from the curated list (Restaurant, MedicalBusiness, AutoRepair, ProfessionalService, etc.) or pick "Other / Custom..." to enter a custom LocalBusiness subtype by hand
- **Description** — short business description
- **URL** — site URL (defaults to the PageMotor site URL)
- **Telephone** — main business phone number, in international format (+44 1234 567890)
- **Email** — main business email
- **Logo URL** — full URL to a square or near-square logo image

### Address

Standard postal address fields: street, locality, region, postcode, country (ISO 3166-1 two-letter code; defaults to GB).

### Geo

Latitude and longitude as decimal numbers. The **Look up coordinates from address** button calls OpenStreetMap Nominatim with your address and fills the fields automatically. Manual entry always wins — Nominatim is a one-shot helper, not a continuous sync.

### Hours

Seven-day grid. For each day either set Closed or enter open / close times in 24-hour format. Multiple intervals per day are supported (e.g. lunch 12:00–14:30, dinner 18:00–22:00). Overnight intervals (close earlier than open) split automatically into two Schema.org entries on emission.

### Payment

- **Payment methods** — multi-select from a curated list (Cash, Credit Card, Debit Card, PayPal, Apple Pay, Bank Transfer, etc.)
- **Currencies accepted** — comma-separated ISO 4217 codes (GBP, EUR, USD)
- **Price range** — pick a single price band (`£`, `££`, `£££`, `££££`)

### Areas served

Free-text textarea, one area per line. Examples: "County Wexford", "Greater London", "Leinster". These render as Schema.org `areaServed` strings.

### Profile URLs

One URL per line. Facebook, LinkedIn, Instagram, Yelp, Google Business Profile, TripAdvisor, etc. These render as `sameAs` references in the JSON-LD.

### Coexistence

When EP SEO is active, choose how the two plugins share the Schema.org graph:

- **Merged** (default) — EP SEO yields its `Organization` branch; EP Local Business emits a single combined Organization + LocalBusiness node at `#organization`. One node, both intents covered. Right for most sole-trader / single-location sites.
- **Additive** — EP SEO emits its Organization node; EP Local Business emits a separate `LocalBusiness` node referencing the Organization via `parentOrganization`. Right for sites where the Organization is a holding company distinct from the trading business.

## How the EP SEO coexistence works

The two plugins coordinate via a static `EP_Local_Business::owns_organization_node()` check that EP SEO calls from its own structured-data emission. When EP Local Business is active in merged mode, EP SEO yields its Organization branch entirely; EP Local Business takes ownership of the `#organization` anchor and emits the combined node.

In additive mode the check returns false — EP SEO emits its Organization, EP Local Business emits its LocalBusiness, both reference each other.

You don't need to configure anything in EP SEO for this to work. The handshake is automatic.

## How the EP Locations coexistence works

EP Local Business is a single-location plugin. EP Locations is the multi-location alternative. They are mutually exclusive at runtime — when EP Locations is active and has at least one live location, EP Local Business defers entirely (its settings page still lets you edit data, but no schema is emitted).

If you start single-location and grow into multi-location, install EP Locations alongside EP Local Business and the data you've already entered carries over conceptually (you'll re-enter the branch data through EP Locations' content-type editor).

## Languages

The admin UI is fully translated into German (de), Spanish (es), French (fr), Italian (it), Dutch (nl), and Portuguese (pt). Schema.org code identifiers (the literal `LocalBusiness`, `Organization`, `parentOrganization` values in the emitted JSON-LD) stay English in every language because they're code, not prose.

Switch UI language from the EP Suite language dropdown in the admin nav.

## Privacy

EP Local Business makes one outbound network call: when you click **Look up coordinates from address** in the Geo section, the plugin sends your address to OpenStreetMap's Nominatim service to resolve coordinates. Nothing is sent automatically; only on explicit click.

The emitted Schema.org JSON-LD becomes part of every public page on your site. Anything you put into the settings (business name, address, telephone, hours, etc.) is therefore public by definition. Don't put internal-only data into these fields.

## Troubleshooting

### "Schema isn't appearing on my pages"

Check the Master Switch is on. Then check Business name and Address are filled in — schema won't emit if either is blank. View page source on any page and search for `application/ld+json` to confirm the node is rendering.

### "I'm seeing two Organization nodes on the page"

EP SEO and EP Local Business are both emitting an Organization. Switch the **Coexistence mode** under EP Local Business → Settings to **Merged**, save, and reload. EP SEO will yield its Organization branch.

### "The Look up coordinates button does nothing"

Three possible causes: (1) your server cannot reach `nominatim.openstreetmap.org` (check egress rules); (2) the address is too vague for Nominatim to resolve (try adding the country); (3) Nominatim's rate limit (1.5 seconds between calls) — wait a moment and try again.

### "EP Local Business says it's deferred to EP Locations"

EP Locations is active and has at least one live Location entry. They're mutually exclusive at runtime. If you actually want EP Local Business to handle schema, deactivate EP Locations or delete its live locations.

### "My hours grid won't accept overnight times"

It should. If you enter open: 22:00, close: 02:00, the emission code splits this into two daily entries automatically. If you're seeing a validation error, file a ticket with the exact times and day you entered.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
