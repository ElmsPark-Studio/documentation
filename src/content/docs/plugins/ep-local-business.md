---
title: "EP Local Business"
description: "Schema.org LocalBusiness emission for any single-location PageMotor site. Address, opening hours, geo coordinates, service area, payment methods, tax identifiers, and a coexistence handshake with EP SEO."
---

EP Local Business adds full Schema.org LocalBusiness emission to any PageMotor site. Address, opening hours (with overnight splitting), geo coordinates, service area, payment methods, currencies, tax identifiers, and 30 curated business subtypes from `Restaurant` to `Veterinary`. Settings-driven, sitewide, and built to coexist cleanly with EP SEO.

For multi-location operators, install [EP Locations](/plugins/ep-locations/) instead. EP Local Business defers to it automatically.

This page documents EP Local Business **1.1.15**.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP Local Business does

- **30 curated LocalBusiness subtypes** plus an "Other / Custom…" override for any Schema.org `LocalBusiness` child type.
- **Full address** with ISO 3166-1 country code, and optional one-click geocoding via OpenStreetMap Nominatim.
- **Weekly opening hours grid** with multi-interval days (lunch closures, split shifts), copy-to-all helpers, and automatic splitting of overnight intervals on emission (22:00 to 02:00 emits as Mon 22:00-23:59 plus Tue 00:00-02:00).
- **Service area:** at-address only, a radius around your address (emitted as `GeoCircle`), or a list of named areas (`AdministrativeArea`).
- **Price range, payment methods, accepted currencies** (ISO 4217).
- **Profile URLs** (`sameAs`) for social, augmenting any Organisation-level `sameAs`.
- **VAT, tax, and ISIC v4 identifiers**, with advisory UK VAT format validation.
- **Open Graph business contact-data tags** emitted automatically when the address is sufficiently complete.
- **JSON-LD preview tool** that renders the live schema against the current form state, before you save.
- **Schema.org validator deep-link** for instant external validation.
- **Coexistence with EP SEO** in two modes, merged or additive.
- **Six EU language translations** of the entire admin UI.

## What EP Local Business doesn't do

- **Multiple locations.** That is [EP Locations](/plugins/ep-locations/), which is what you want for chains, franchises, or any business with more than one branch.
- **Holiday or special hours overrides.** Planned for a future release.
- **`hasOfferCatalog` (structured services with prices).** Planned.
- **`aggregateRating` or review CRUD.** Use EP Reviews when it ships.
- **Per-page LocalBusiness overrides.** Settings-driven sitewide only.

## Requirements

- **PageMotor 0.8.3 or later.** Required because EP Local Business uses PageMotor's framework-level CSRF (an auto-injected `X-CSRF-Token` header on authenticated AJAX). Earlier versions reject the preview, geocode and hours-validation requests.
- **EP Suite** base class (auto-loaded with any EP plugin).
- **EP SEO**, optional. Needed only for the merged-mode handshake that produces a single combined `Organization` plus `LocalBusiness` node. Additive mode and standalone operation work fine without it.

## Installation

1. Download the latest `ep-local-business.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-local-business).
2. In PageMotor admin go to **Plugins → Manage Plugins → Upload**, select the zip, and activate.
3. Open the plugin's settings page and tick **Enable LocalBusiness schema** in the Business section. Without this gate, no LocalBusiness JSON-LD is emitted.
4. Fill in at least the business name, address and country code. Add hours and geo coordinates for a richer schema.

## Settings

The settings page has nine sections, each rendered as a collapsible card.

### Business

Identity, type, and description.

- **Enable LocalBusiness schema.** Master gate. Required for any emission.
- **Business Type.** Pick the most specific match from the curated list (AutoRepair, Bakery, Restaurant, Dentist, and so on) or choose **Other / Custom…** to enter any Schema.org `LocalBusiness` subtype by hand. Custom values outside the recognised allowlist still emit; you just see an advisory warning.
- **Business Name.** The trading name. **Required.** The schema does not emit without it, even when the master gate is on.
- **Legal Name.** Registered legal entity, if different from the trading name.
- **Description.** One or two sentences. Keep it under 200 characters.
- **Founding Date.** ISO 8601 date (`YYYY-MM-DD`).
- **Slogan.** Tagline or catchphrase, if you use one.

### Contact

Phone, email, logo, and photos.

- **Telephone.** Use E.164 format where possible (`+44 1234 567890`). Stored and emitted as entered.
- **Email.** Public-facing business email. Optional.
- **Logo URL.** Full URL to the business logo. Recommended: 600x600 PNG with a transparent background.
- **Photo URLs.** One image URL per line. These become the LocalBusiness `image` property. Storefront and interior shots work well.

### Location

Address and coordinates.

- **Street Address, Town/City, County/Region, Postcode.** Standard postal address fields.
- **Country (ISO 3166-1).** Two-letter alpha-2 code (`GB`, `IE`, `US`, `DE`).
- **Latitude / Longitude.** Decimal degrees, range -90 to 90 and -180 to 180. Out-of-range values are silently dropped from the emitted schema.
- **Look up coordinates from address.** One-click geocoding via OpenStreetMap Nominatim. The button sends the assembled address fields to `nominatim.openstreetmap.org` on click and fills in latitude and longitude from the first match. Throttled client-side to one request every 1.5 seconds, in line with Nominatim's terms of use. Pasting coordinates from Google Maps or Apple Maps works just as well; geocoding is opt-in only.
- **Map URL.** Optional Google Maps, OpenStreetMap or Apple Maps URL pointing to the location. Emitted as `hasMap`.

### Opening Hours

The trickiest UI in the plugin, and the one most worth exploring.

- Each day (Mon to Sun) has an **Open / Closed** toggle.
- Open days take **one or more time intervals**, useful for businesses that close for lunch (08:00-12:00 plus 13:00-17:30) or run split shifts.
- The **+ Add interval** button on each day stacks multiple opens and closes per day.
- The **Copy to all** button on each row copies that day's status and intervals to every other day. Set Monday once, click Copy to all, then tweak the weekend.
- 24 hours a day is representable as a single `00:00` to `23:59` interval.
- **Overnight intervals are handled automatically.** Enter `22:00` to `02:00` on Monday, the typical late-bar pattern, and the schema emits two `OpeningHoursSpecification` entries: Monday 22:00-23:59 and Tuesday 00:00-02:00. Enter the natural interval on the day it starts and let the plugin do the split.
- Stored as JSON in a single hidden field, emitted as a Schema.org `openingHoursSpecification` array.

### Service

Area, pricing, payment.

- **Service Area.** Three modes:
  - **At our address only.** Suits walk-in businesses.
  - **Radius around our address.** Combines with latitude and longitude to emit a `GeoCircle` with `geoMidpoint` and `geoRadius` in metres.
  - **List of named areas.** One area per line ("County Wexford", "Greater London"). Each line emits as an `AdministrativeArea` entry.
- **Service Radius (km).** Used by radius mode. Converted to metres for Schema.org.
- **Areas Served.** Used by list mode. One area per line.
- **Price Range.** From `£` inexpensive through `££££` premium.
- **Payment Methods Accepted.** Tick boxes for Cash, Credit Card, Debit Card, Cheque, Bank Transfer, Invoice, PayPal, Apple Pay, Google Pay and Cryptocurrency. Joined into a comma-separated `paymentAccepted` string.
- **Currencies Accepted.** Comma-separated ISO 4217 codes (`GBP, EUR`). Whitespace is stripped and codes are uppercased.

### Social Profiles

- **Profile URLs.** One URL per line. Facebook page, LinkedIn company page, X/Twitter profile, Instagram, and so on. Emitted as the `sameAs` array on the LocalBusiness node.

### Tax & Identifiers

- **VAT ID.** When the country code is `GB`, the value is format-checked against UK VAT patterns (9-digit, 12-digit, government-department `GD###`, health-authority `HA###`). Advisory only; the schema emits regardless.
- **Tax ID.** Other tax registration number (CRO, EIN, and similar).
- **ISIC v4 Code.** International Standard Industrial Classification. Optional.

### Integration

Coexistence with EP SEO.

- **Coexistence Mode.** See the next section.
- **Schema ID Anchor.** The fragment used in `@id` for additive mode, so `localbusiness` yields `https://example.com/#localbusiness`. Letters, numbers, hyphens and underscores only. Default `localbusiness`. Ignored in merged mode, which always uses `#organization`.

### Tools

- **Preview JSON-LD.** Sends the current form state to the plugin and renders the resulting `@graph` in a modal, with no need to save first. Shows the current coexistence mode, whether emission is active, whether EP SEO is present, and whether EP Locations has taken over.
- **Open in Schema.org validator.** Deep-links to `validator.schema.org` with your site's origin pre-filled. Use it after deploying changes.

## Coexistence with EP SEO

If you are a sole trader or single-business owner, meaning the business *is* the organisation behind the website, leave coexistence mode at the default of **Merged**. EP SEO yields its `Organization` branch and EP Local Business emits one combined node typed `["Organization", "LocalBusiness"]` at `#organization`. The combined node folds in EP SEO's name, URL, description and any other Organisation properties on top of the LocalBusiness body. This is the cleanest representation for the typical case.

If your business has a separate parent organisation distinct from this location, a franchise, a group operator or a holding company, choose **Additive**. EP SEO emits its `Organization` node at `#organization` as normal and EP Local Business adds a separate `LocalBusiness` node at `#<id_anchor>` with a `parentOrganization` reference back to `#organization`. Schema validators understand both nodes as related but distinct.

If EP SEO is not installed at all, EP Local Business emits its own LocalBusiness node either way; the coexistence setting then only affects the `@id` anchor.

The handshake itself is automatic and needs no configuration in EP SEO. EP SEO calls a static `EP_Local_Business::owns_organization_node()` check from its own structured-data emission; in merged mode that returns true and EP SEO yields its Organization branch entirely.

## EP Locations defer

When [EP Locations](/plugins/ep-locations/) is installed and active alongside EP Local Business, EP Local Business yields LocalBusiness emission entirely and EP Locations owns it. The handshake is a static class check inside EP Local Business, and needs no configuration. This is intentional: multi-location is a content-driven problem, where each branch needs its own URL, hours and address, and that is what EP Locations is built for.

Your settings page still lets you edit the data while deferred, so nothing is lost if you later deactivate EP Locations.

## Open Graph business contact data

When LocalBusiness emission is active and the address is sufficiently complete (street, locality and country all populated), EP Local Business automatically emits Facebook's Open Graph business contact-data tags:

- `og:type` set to `business.business`, overriding PageMotor's default `article` or `website`
- `og:business:contact_data:street_address`
- `og:business:contact_data:locality`
- `og:business:contact_data:region`
- `og:business:contact_data:postal_code`
- `og:business:contact_data:country_name`
- `og:business:contact_data:phone_number`, if telephone is set
- `og:business:contact_data:email`, if email is set

Useful for Facebook business page link previews, and a small but non-zero ranking signal.

## Languages

The admin UI is fully translated into German (de), Spanish (es), French (fr), Italian (it), Dutch (nl) and Portuguese (pt). Schema.org code identifiers, the literal `LocalBusiness`, `Organization` and `parentOrganization` values in the emitted JSON-LD, stay English in every language because they are code, not prose.

Switch UI language from the EP Suite language dropdown in the admin nav.

## Privacy and EP GDPR

EP Local Business is settings-driven and exposes no third-party services to public visitors. The OpenStreetMap Nominatim geocode helper is **admin-only**: it lives on the plugin's settings page, fires only on an explicit click, and is never reached by a site visitor. No consent gating is required.

The schema and Open Graph tags the plugin emits contain only data the site admin chose to publish (business name, address, telephone, opening hours), which is public information about the business rather than visitor data. It does become part of every public page, so do not put internal-only data into these fields.

If you also install [EP Locations](/plugins/ep-locations/) for the multi-location store finder, that plugin handles its own GDPR integration for the public-facing map and search.

## Action / boundary methods (for AI agents and CLI scripts)

EP Local Business follows the PageMotor action / operation pattern. Three actions are exposed as public methods that can be called directly, without simulating a POST:

| Action | Returns |
|--------|---------|
| `preview($settings)` | `['success' => true, 'json_ld' => …, 'mode' => …, 'active' => bool, …]` |
| `geocode($address)` | `['success' => bool, 'latitude' => …, 'longitude' => …, 'display_name' => …]`, or failure with `reason` |
| `validate_hours($hours)` | `['success' => bool, 'errors' => […], 'schema' => […]]` |

Each has a paired `<name>_post()` boundary method that reads `$_POST`, performs the admin-access check, and echoes JSON. Useful if you are building tooling around the plugin from outside its admin UI.

## Troubleshooting

### “I enabled the plugin but no schema appears in the page source”

Three things to check:

1. The **Enable LocalBusiness schema** box is ticked.
2. **Business Name** is filled in. Without it the schema is suppressed even when enabled.
3. EP Locations is not active. If it is, EP Local Business yields to it. The Preview tool tells you, via `ep_locations_present: yes`.

View page source and search for `application/ld+json` to confirm the node is rendering.

### “Hours grid says Open but no times show”

Add at least one interval with the **+ Add interval** button. An open day with no intervals emits as closed.

### “The geocode button doesn't find my address”

Nominatim's coverage is excellent for high-density urban addresses but can be patchy for rural or recently built ones. Try entering just street, town and country, dropping the postcode and region, then click again. If it still fails, open `https://www.openstreetmap.org/search?query=<your+address>` in a browser: if OSM cannot find it there, EP Local Business cannot either. Paste latitude and longitude from Google Maps as a fallback.

### “The geocode button does nothing at all”

Different symptom, different cause. Either your server cannot reach `nominatim.openstreetmap.org` (check egress rules), or the click is being throttled. See the next entry.

### “Geocode says 'Please wait a moment before trying again'”

Nominatim's terms of use cap requests at one per second. EP Local Business throttles client-side to one every 1.5 seconds for safety. Wait two seconds and click again.

### “Rich Results Test flags an unrecognised business type”

You used the **Other / Custom…** option with a value that is not a recognised Schema.org `LocalBusiness` subtype. Either pick from the curated list, or check the spelling against the [LocalBusiness type list](https://schema.org/LocalBusiness) on schema.org and re-enter it exactly.

### “My hours grid won't accept overnight times”

It should. Entering open `22:00` and close `02:00` is valid, and the emission code splits it automatically as described above. If you are seeing a validation error instead, that is a bug: open a ticket with the exact times and the day you entered.

### “Overnight hours look wrong in the schema preview”

That is by design. An interval like `22:00` to `02:00` splits into two `OpeningHoursSpecification` entries, today 22:00-23:59 and tomorrow 00:00-02:00, because Schema.org does not model intervals crossing midnight as a single entry. Validators accept the split form.

### “I'm seeing two Organization nodes on the page”

EP SEO and EP Local Business are both emitting an Organization. Set **Coexistence Mode** to **Merged**, save, and reload. EP SEO will yield its Organization branch.

### “I want EP SEO to keep emitting Organisation separately”

Set **Coexistence Mode** to **Additive**. EP SEO emits `Organization` at `#organization` and EP Local Business emits its `LocalBusiness` at the configured `#<id_anchor>`, with a `parentOrganization` reference back.

### “I switched on EP Local Business and lost my Person schema”

You probably had EP SEO's Schema Type set to `Person` and switched coexistence mode to Merged, which assumes Organisation-shaped semantics. Either switch coexistence mode to Additive, so EP SEO keeps emitting your Person schema separately, or change EP SEO's Schema Type to `Organization` if Person was a leftover from before the business existed.

### “EP Local Business says it's deferred to EP Locations”

EP Locations is active and has at least one live Location entry. They are mutually exclusive at runtime. If you want EP Local Business to handle schema instead, deactivate EP Locations or delete its live locations.

### “VAT ID validation flagged my number but it's correct”

The UK VAT validator checks format only, not validity, and applies only when the country is `GB`. The schema emits the value regardless of the warning. If your number is genuinely valid, check it matches one of the patterns: 9 digits, 12 digits, `GD###` for a government department, or `HA###` for a health authority. Numbers from other countries do not trigger validation.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger, a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
