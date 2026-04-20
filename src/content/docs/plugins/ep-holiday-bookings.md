---
title: "EP Holiday Bookings"
description: "Holiday package management for independent travel agents. Package listings, enquiry-driven booking flow, deposit and balance payments via Stripe, traveller management with encrypted passport storage."
sidebar:
  order: 35
---

EP Holiday Bookings is a purpose-built plugin for independent travel agents. Not a DIY booking engine — an enquiry-first workflow that matches how small agents actually work. Package listings attract interest, enquiries land in a pipeline, the agent quotes, collects deposits, then balances, and tracks traveller details securely.

Published by [ElmsPark Studio](https://elmspark.com).

## Who this is for

Independent travel agents who:

- Curate a catalogue of packages rather than selling from live inventory.
- Talk to every customer before confirming a booking (enquiry-first, not self-checkout).
- Take deposits upfront and balances closer to travel.
- Need to hold traveller details (passport numbers, dietary requirements, emergency contacts) securely.

Not for online travel agents with API-based inventory. Not for ATOL-bonded trust-account operations — that's a compliance domain this plugin doesn't touch.

## Features

### Destination and package catalogue

- **Destinations** with name, region, country, hero image, description.
- **Packages** tied to a destination with dates, pricing, capacity, itinerary, inclusions, exclusions.

### Enquiry-first flow

A customer browses packages, finds one they like, submits an enquiry form. The agent replies, discusses, quotes. When the customer commits, the agent turns the enquiry into a booking.

### Pipeline

Enquiry statuses: New → Contacted → Quoted → Booked → Cancelled. Visible on the admin dashboard so the agent always knows what needs attention.

### Deposits and balances

Stripe-integrated payment collection:

- **Deposit** when the booking is confirmed.
- **Balance** closer to travel (typically 6 to 8 weeks before).
- **Payment links** sent to the customer, not self-checkout on the site.

### Travellers

Per-booking traveller records:

- Name, date of birth, passport number, nationality.
- **Passport numbers encrypted at rest** using AES-256.
- Dietary requirements, emergency contact.

### GDPR

Encrypted sensitive fields, consent logging via EP GDPR, full-record deletion on data subject erasure request.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[holiday-packages]` | Full package catalogue with filtering. |
| `[holiday-package slug=spain-villa-week]` | Single package page. |
| `[holiday-destinations]` | Destination catalogue. |
| `[holiday-enquiry package=spain-villa-week]` | Enquiry form for a specific package. |
| `[holiday-search]` | Search interface across packages. |

## Requirements

- **PageMotor 0.7 or later**
- **EP Email** (required for notifications)
- **EP Suite base class**
- **Stripe account** (for deposit / balance collection)

Optional:

- **EP GDPR** for consent logging.
- **EP Newsletter** for opt-in at enquiry time.

## Status

**Version 0.3.0** — the core pipeline and catalogue are stable. Some UX polish items are still pending. Details in the plugin's own CHANGELOG.

## Installation

1. Install EP Email.
2. Download `ep-holiday-bookings.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Configure Stripe keys in the settings.
5. Work through Destinations → Packages → Test enquiry form.

## Database tables

All prefixed `{prefix}ep_holiday_`:

- `destinations` — destination catalogue.
- `packages` — holiday listings.
- `enquiries` — customer enquiries with pipeline status.
- `bookings` — confirmed bookings with deposit/balance tracking, Stripe payment intent IDs.
- `travellers` — per-booking traveller details, passport encrypted.
- `customers` — customer database.

## Compliance notes

### ATOL and ABTA

This plugin does NOT handle ATOL bonding, client-money trust accounts, or ABTA-specific compliance. If your regulatory context requires those, use accounting and compliance tools designed for that purpose. EP Holiday Bookings is operational CRM, not financial infrastructure.

### Passport storage

Passport numbers are encrypted at rest using AES-256 with a key stored outside the database. Decryption happens only server-side, only when the agent explicitly views a traveller record. The key itself should be:

- Stored in a PHP environment variable (`EP_HOLIDAY_ENCRYPTION_KEY`).
- Backed up separately from database backups.
- Rotated periodically.

If you lose the key, stored passport numbers become unrecoverable. This is by design.

### GDPR erasure

On a data subject erasure request, the plugin:

- Deletes the customer record.
- Deletes all associated enquiries and bookings.
- Deletes traveller records with encrypted passport numbers.
- Retains a minimal audit row noting the erasure happened.

## Troubleshooting

### "Enquiry form submitted but I didn't get notified"

Check EP Email config. Enquiry notifications go through EP Email's queue.

### "Deposit payment link is generated but the customer can't pay"

Check Stripe keys are for the correct mode (test vs live). Check the payment link hasn't expired — Stripe links have configurable lifetimes.

### "Passport number shows 'decryption failed'"

The encryption key has changed since the record was encrypted. Either restore the old key, or re-collect the passport from the customer.

### "Package isn't appearing in the catalogue"

Check status is Active and dates haven't expired. Packages past their end date are auto-hidden by default.

### "Enquiry pipeline status doesn't update when I mark an enquiry as Booked"

Creating a booking from an enquiry should auto-advance the enquiry to Booked. If it doesn't, there's a likely bug — log in the review queue with an enquiry ID.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
