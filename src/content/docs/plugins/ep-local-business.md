---
title: "EP Local Business"
description: "Schema.org LocalBusiness emission for any single-location PageMotor site. Address, opening hours, geo coordinates, payment methods, service area, tax identifiers."
sidebar:
  order: 51
---

EP Local Business adds full Schema.org LocalBusiness emission to any PageMotor site. Address, opening hours (with overnight splitting), geo coordinates, service area, payment methods, currencies, tax identifiers, and 30 curated business subtypes from `Restaurant` to `Veterinary`. Settings-driven, sitewide, and built to coexist cleanly with EP SEO.

For multi-location operators, install [EP Locations](/plugins/ep-locations/) instead — EP Local Business defers to it automatically.

Published by [ElmsPark Studio](https://elmspark.com).

## What EP Local Business does

- **30 curated LocalBusiness subtypes** plus an "Other / Custom…" override for any Schema.org `LocalBusiness` child type.
- **Full address** with ISO 3166-1 country code, optional one-click geocoding via OpenStreetMap Nominatim.
- **Weekly opening hours grid** with multi-interval days (lunch closures, split shifts), copy-to-all helpers, and automatic splitting of overnight intervals on emission (e.g. 22:00–02:00 emits as Mon 22:00–23:59 + Tue 00:00–02:00).
- **Service area:** at-address only, radius around your address (emitted as `GeoCircle`), or a list of named areas (`AdministrativeArea`).
- **Price range, payment methods, accepted currencies** (ISO 4217).
- **Profile URLs** (sameAs) for social, augmenting any Organisation-level sameAs.
- **VAT, tax, and ISIC v4 identifiers**, with advisory UK VAT format validation.
- **Open Graph business contact-data tags** (`og:type=business.business`, `og:business:contact_data:*`) emitted automatically when the address is sufficiently complete.
- **JSON-LD preview tool** that renders the live schema against the current form state, before you save.
- **Schema.org validator deep-link** for instant external validation.
- **Coexistence with EP SEO** in two modes (merged or additive — see below).

## What EP Local Business doesn't do

- **Multiple locations.** That's [EP Locations](/plugins/ep-locations/), which is what you want for chains, franchises, or any business with more than one branch.
- **Holiday or special hours overrides.** Planned for a future release.
- **`hasOfferCatalog` (structured services with prices).** Planned.
- **`aggregateRating` or review CRUD.** Use EP Reviews when it ships.
- **Per-page LocalBusiness overrides.** Settings-driven sitewide only.

## Requirements

- **PageMotor 0.8.3 or later.** Required because EP Local Business uses PM 0.8.3b's framework-level CSRF (auto-injected `X-CSRF-Token` header on authenticated AJAX). Earlier PageMotor versions will reject the preview, geocode, and hours-validation requests.
- **EP SEO 1.3 or later** — optional. Needed only for the merged-mode handshake that produces a single combined `Organization` + `LocalBusiness` node. Additive mode and standalone operation work fine without EP SEO.

## Installation

1. Download `ep-local-business.zip` from your EP Suite distribution.
2. Upload via **Plugins → Manage Plugins**.
3. Activate.
4. Open the plugin's settings page and tick **Enable LocalBusiness schema** in the Business section. Without this gate, no LocalBusiness JSON-LD is emitted.
5. Fill in at least the business name, address, and country code. Add hours and geo coordinates for a richer schema.

## Settings

The settings page has nine sections, each rendered as a collapsible card.

### Business

Identity, type, and description.

- **Enable LocalBusiness schema.** Master gate. Required for any emission.
- **Business Type.** Pick the most specific match from the curated list (AutoRepair, Bakery, Restaurant, Dentist, etc.) or choose **Other / Custom…** to enter any Schema.org `LocalBusiness` subtype by hand. Custom values that aren't in the recognised allowlist still emit; you'll just see an advisory warning.
- **Business Name.** The trading name. **Required** — the schema does not emit without it, even when the master gate is on.
- **Legal Name.** Registered legal entity, if different from the trading name.
- **Description.** One or two sentences. Keep it under 200 characters.
- **Founding Date.** ISO 8601 date (`YYYY-MM-DD`).
- **Slogan.** Tagline or catchphrase, if you use one.

### Contact

Phone, email, logo, and photos.

- **Telephone.** Use E.164 format where possible (e.g. `+44 1234 567890`). Stored and emitted as entered.
- **Email.** Public-facing business email. Optional.
- **Logo URL.** Full URL to the business logo. Recommended: 600×600 PNG with transparent background.
- **Photo URLs.** One image URL per line. These become the LocalBusiness `image` property. Storefront and interior shots work well.

### Location

Address and coordinates.

- **Street Address, Town/City, County/Region, Postcode** — standard postal address fields.
- **Country (ISO 3166-1).** Two-letter alpha-2 code (e.g. `GB`, `IE`, `US`, `DE`).
- **Latitude / Longitude.** Decimal degrees, range −90 to 90 / −180 to 180. Out-of-range values are silently dropped from the emitted schema.
- **Look up coordinates from address.** One-click geocoding via OpenStreetMap Nominatim. The button sends the assembled address fields to `nominatim.openstreetmap.org` on click and populates latitude and longitude with the first match. Throttled client-side to one request every 1.5 seconds in line with Nominatim's terms of use. If you'd rather paste coordinates from Google Maps or Apple Maps, you can — geocoding is opt-in only.
- **Map URL.** Optional Google Maps, OpenStreetMap, or Apple Maps URL pointing to the location. Emitted as `hasMap`.

### Opening Hours

The trickiest UI in the plugin and the one most worth exploring.

- Each day (Mon–Sun) has an **Open / Closed** toggle.
- Open days take **one or more time intervals** — useful for businesses that close for lunch (e.g. 08:00–12:00 + 13:00–17:30) or split shifts.
- The **+ Add interval** button on each day lets you stack multiple opens/closes per day.
- The **Copy to all** button on each row copies that day's status and intervals to every other day. Set Monday once, click Copy to all, then tweak weekends.
- 24 hours/day is representable as a single `00:00`–`23:59` interval.
- **Overnight intervals are handled automatically.** If you enter `22:00`–`02:00` on Monday (a typical bar/late-restaurant pattern), the schema emits two `OpeningHoursSpecification` entries: Monday 22:00–23:59 and Tuesday 00:00–02:00. You don't have to think about the split — enter the natural interval on the day it starts.
- Stored as JSON in a single hidden field; emitted as a Schema.org `openingHoursSpecification` array.

### Service

Area, pricing, payment.

- **Service Area.** Three modes:
  - **At our address only.** Suits walk-in businesses.
  - **Radius around our address.** Combines with latitude/longitude to emit a `GeoCircle` with `geoMidpoint` + `geoRadius` in metres.
  - **List of named areas.** One area per line (e.g. "County Wexford", "Greater London"). Each line emits as an `AdministrativeArea` entry.
- **Service Radius (km).** Used by radius mode. Converted to metres for Schema.org.
- **Areas Served.** Used by list mode. One area per line.
- **Price Range.** £ inexpensive through ££££ premium.
- **Payment Methods Accepted.** Tick boxes for Cash, Credit Card, Debit Card, Cheque, Bank Transfer, Invoice, PayPal, Apple Pay, Google Pay, Cryptocurrency. Joined into a comma-separated `paymentAccepted` string.
- **Currencies Accepted.** Comma-separated ISO 4217 codes (e.g. `GBP, EUR`). Whitespace stripped, codes uppercased.

### Social Profiles

- **Profile URLs.** One URL per line. Facebook page, LinkedIn company page, X/Twitter profile, Instagram, etc. Emitted as the `sameAs` array on the LocalBusiness node.

### Tax & Identifiers

- **VAT ID.** When the country code is `GB`, the value is format-checked against UK VAT patterns (9-digit, 12-digit, government-department `GD###`, health-authority `HA###`). Advisory only — the schema emits regardless.
- **Tax ID.** Other tax registration number (CRO, EIN, etc.).
- **ISIC v4 Code.** International Standard Industrial Classification. Optional.

### Integration

Coexistence with EP SEO.

- **Coexistence Mode** — see the next section.
- **Schema ID Anchor.** The fragment used in `@id` for additive mode (e.g. `localbusiness` yields `https://example.com/#localbusiness`). Letters, numbers, hyphens, and underscores only. Default: `localbusiness`. Ignored in merged mode (which always uses `#organization`).

### Tools

- **Preview JSON-LD.** Sends the current form state to the plugin and renders the resulting `@graph` in a modal — no need to save first. Shows the current coexistence mode, whether emission is active, whether EP SEO is present, and whether EP Locations has taken over.
- **Open in Schema.org validator.** Deep-links to `validator.schema.org` with your site's origin pre-filled. Use after deploying changes.

## Coexistence with EP SEO

If you're a sole trader or single-business owner — meaning the business *is* the organisation behind the website — leave coexistence mode at the default of **Merged**. EP SEO yields its `Organization` branch and EP Local Business emits one combined node typed `["Organization", "LocalBusiness"]` at `#organization`. The combined node folds in EP SEO's name, URL, description, and any other Organisation properties on top of the LocalBusiness body. This is the cleanest representation for the typical case.

If your business has a separate parent organisation distinct from this location — a franchise, a group operator, a holding company — choose **Additive**. EP SEO emits its `Organization` node at `#organization` as normal and EP Local Business adds a separate `LocalBusiness` node at `#<id_anchor>` with a `parentOrganization` reference back to `#organization`. Schema validators understand both nodes as related but distinct.

If EP SEO is not installed at all, EP Local Business emits its own LocalBusiness node either way; the coexistence setting only affects the `@id` anchor.

## EP Locations defer

When [EP Locations](/plugins/ep-locations/) is installed and active alongside EP Local Business, EP Local Business yields LocalBusiness emission entirely — EP Locations owns it. The handshake is a static class check inside EP Local Business; no configuration required. This is intentional: multi-location is a content-driven problem (each branch needs its own URL, hours, address) which EP Locations is built for.

## Open Graph business contact data

When LocalBusiness emission is active and the address is sufficiently complete (street + locality + country populated), EP Local Business automatically emits Facebook's Open Graph business contact-data tags:

- `og:type` = `business.business` (overrides PageMotor's default `article` or `website`)
- `og:business:contact_data:street_address`
- `og:business:contact_data:locality`
- `og:business:contact_data:region`
- `og:business:contact_data:postal_code`
- `og:business:contact_data:country_name`
- `og:business:contact_data:phone_number` (if telephone is set)
- `og:business:contact_data:email` (if email is set)

Useful for Facebook business page link previews and a small but non-zero ranking signal.

## Privacy and EP GDPR

EP Local Business is settings-driven and does not expose third-party services to public visitors. The OSM Nominatim geocode helper is **admin-only** — it lives on the plugin's settings page where only logged-in admins use it. No consent gating is required.

The schema and Open Graph tags emitted by the plugin contain only data the site admin chose to publish (business name, address, telephone, opening hours, etc.) — public information about the business, not visitor data.

If you also install [EP Locations](/plugins/ep-locations/) for the multi-location store finder, that plugin handles its own GDPR integration for the public-facing map and search.

## Action / boundary methods (for AI agents and CLI scripts)

EP Local Business follows the PM 0.8.3b action / operation pattern. Three actions are exposed as public methods that can be called directly without simulating a POST:

| Action | Returns |
|--------|---------|
| `preview($settings)` | `['success' => true, 'json_ld' => …, 'mode' => …, 'active' => bool, …]` |
| `geocode($address)` | `['success' => bool, 'latitude' => …, 'longitude' => …, 'display_name' => …]` or failure with `reason` |
| `validate_hours($hours)` | `['success' => bool, 'errors' => […], 'schema' => […]]` |

Each has a paired `<name>_post()` boundary method that reads `$_POST`, performs the admin-access check, and echoes JSON. Useful if you're building tooling around the plugin from outside its admin UI.

## Troubleshooting

### "I enabled the plugin but no schema appears in the page source"

Three things to check:

1. The **Enable LocalBusiness schema** box is ticked.
2. **Business Name** is filled in. Without it, the schema is suppressed even when enabled.
3. EP Locations isn't active. If it is, EP Local Business yields to it. The Preview tool will tell you (`ep_locations_present: yes`).

### "Hours grid says 'Open' but no times show"

Add at least one interval with the **+ Add interval** button. An open day with no intervals emits as closed.

### "The geocode button doesn't find my address"

Nominatim's coverage is excellent for high-density urban addresses but can be patchy for rural or recently built addresses. Try entering just the street + town + country (drop the postcode and region) and click again. If it still fails, open `https://www.openstreetmap.org/search?query=<your+address>` in the browser — if OSM can't find it there, EP Local Business can't either. Paste latitude/longitude from Google Maps as a fallback.

### "Geocode says 'Please wait a moment before trying again'"

Nominatim's terms of use cap requests at one per second. EP Local Business throttles client-side to one every 1.5 seconds for safety. Wait two seconds and click again.

### "Rich Results Test flags an unrecognised business type"

You used the **Other / Custom…** option with a value that isn't a recognised Schema.org `LocalBusiness` subtype. Either pick from the curated list, or check the spelling against the [LocalBusiness type list](https://schema.org/LocalBusiness) on schema.org and re-enter exactly.

### "Overnight hours look wrong in the schema preview"

That's by design. An interval like `22:00`–`02:00` splits into two `OpeningHoursSpecification` entries (today 22:00–23:59 and tomorrow 00:00–02:00) because Schema.org's spec doesn't model intervals that cross midnight as a single entry. Validators accept the split form.

### "I want EP SEO to keep emitting Organisation separately"

Set **Coexistence Mode** to **Additive**. EP SEO will emit `Organization` at `#organization` and EP Local Business will emit its `LocalBusiness` at the configured `#<id_anchor>` with a `parentOrganization` reference back.

### "I switched on EP Local Business and lost my Person schema"

You probably had EP SEO's Schema Type set to `Person` and switched coexistence mode to Merged. Merged mode assumes Organisation-shaped semantics. Switch coexistence mode to Additive (so EP SEO keeps emitting your Person schema separately), or change EP SEO's Schema Type to `Organization` if Person was a leftover from before the business existed.

### "VAT ID validation flagged my number but it's correct"

The UK VAT validator only checks format, not validity, and only applies when country is `GB`. The schema emits the value regardless of the warning. If your number is genuinely valid and the warning bothers you, double-check it matches one of the patterns: 9 digits, 12 digits, `GD###` (government department), or `HA###` (health authority). Numbers from other countries don't trigger validation.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
