---
title: "EP Booking"
description: "Online appointment scheduling for PageMotor. Services, staff, availability, payments via Stripe, automated notifications via EP Email, Zoom integration."
sidebar:
  order: 9
---

EP Booking is a full appointment-scheduling system. Services, staff, availability schedules, a multi-step booking form your customers fill out on your site, Stripe payments, automated email confirmations and reminders, and (via the companion add-on) automatic Zoom meeting creation.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

What it does end-to-end:

1. You define **services** (haircut, consultation, massage) with price and duration.
2. You define **staff** with individual availability schedules and which services they offer.
3. A customer visits your site, picks a service, picks a staff member (optional), picks a date and a time slot.
4. They enter their details, optionally pay via Stripe, and confirm.
5. Automated emails go out: confirmation now, reminder 24 hours before (or your configured window).
6. Your admin panel shows the booking. You can cancel, reschedule, or refund from the admin.
7. If EP Booking Zoom is installed, a Zoom meeting was created automatically and the link is in the confirmation email.

What EP Booking is NOT: a calendar app, a resource scheduler for rooms, or a class-booking system for group events. It is appointment-by-appointment scheduling between one customer and one staff member.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class** (bundled)
- **EP Email** (required for notifications)

Optional add-ons:

- **EP Booking Zoom** for auto-created Zoom meetings
- **EP Newsletter** to offer opt-in on the booking form
- **EP GDPR** for consent logging
- **EP Affiliate** to attribute bookings to referrers

## Installation

1. Download `ep-booking.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Work through the settings sections in this order: General → Services → Staff → Categories → Booking Rules → Notifications → Form Design → Payments → Booking Form.

## Setting up the basics

### General

- **Business name, address, phone** for notification emails.
- **Opening / closing times** are the outer envelope of when bookings are possible. Individual staff schedules can be tighter.
- **Timezone** matters. Set this correctly, everything else derives from it.

### Services

Create each bookable service with:

- **Name** (e.g. "60-minute massage").
- **Category** (optional grouping).
- **Duration** in minutes.
- **Price.** Set to 0 for free bookings.
- **Require payment?** Per-service toggle. Off for free or pay-on-arrival services.
- **Active?** Inactive services don't appear on the booking form.

### Staff

Create each staff member with:

- **Name and photo** (optional).
- **Availability schedule** — recurring weekly pattern (e.g. Mon-Fri 9-5, Wed off).
- **Holiday blocks** — specific date ranges to mark unavailable.
- **Services offered** — pick from your service list.

### Categories

Optional. Groups services for display on the booking form and the `[booking-services]` catalog shortcode.

### Booking Rules

- **Minimum advance time.** Can't book less than N hours before the slot.
- **Maximum advance time.** Can't book more than N days ahead.
- **Default duration** for services that don't override.
- **Time slot interval.** How finely slots are offered: 15, 20, 30, or 60 minutes.
- **Cancellation window.** Customer can cancel themselves up to N hours before the booking.
- **Auto-confirm?** If off, bookings start in Pending and you manually confirm each one.

### Notifications

Five emails go out automatically. Three are templated and editable. Two are sent to you and your assigned staff member with a built-in layout.

**Customer emails (templated):**

- **Confirmation:** sent immediately after booking.
- **Reminder:** sent N hours before (configurable, typical 24).
- **Cancellation:** sent when a booking is cancelled.

For each one you can set a **Subject** and a **Message**. If you leave the Message field empty, the rich built-in version is sent (greeting, full booking details table, cancel link). If you put text in the Message field, that exact text is what gets sent (escaped, line breaks preserved). A common trap is typing something brief like "Confirmed" into the Message field, which then replaces the rich default with the literal word "Confirmed". Either keep the Message field empty, or write a proper message using placeholders.

**Internal emails (built-in layout):**

- **Admin Notification:** sent to the address in your General settings whenever a new booking comes in. Toggled by the Admin Notification checkbox.
- **Staff Notification:** sent to the assigned staff member. Always sent when the staff record has an email address.

These two have hardcoded HTML bodies that already include the full booking details table. You can't edit the body or subject directly, but you can change how they're wrapped (see Email Template below).

**Email Template (the wrapper):**

The dropdown at the bottom of the Notifications section controls the HTML wrapper used for every booking email above (customer, admin, and staff).

- "Plain text — no HTML wrapper" (default). Emails arrive bare. Even when the body contains HTML, no styling, header, or footer is added around it.
- "Default — clean transactional layout".
- "Notification — admin-style alerts".
- "Minimal — light branding".
- "Branded — full logo and colours" pulled from your EP Email branding settings.

If your booking emails are arriving looking unstyled, this dropdown is almost always the cause. Pick anything other than Plain text.

**Available placeholders for Subject and Message fields:**

`{customer_name}`, `{customer_email}`, `{service_name}`, `{staff_name}`, `{booking_date}`, `{booking_time}`, `{duration}`, `{price}`, `{amount_paid}`, `{payment_status}`, `{cancel_url}`, `{site_name}`, `{business_name}`, `{business_phone}`, `{business_address}`, `{zoom_url}`, `{zoom_host_url}`.

### Form Design

Visual controls so the booking form matches your site's look:

- **Primary colour, Accent colour, Text colour.** Hex colours used by the form's buttons, links, and copy.
- **Corner rounding** on buttons and cards (none, small, medium, large, pill).
- **Max width** of the form container in pixels (e.g. `720`).
- **Card shadow** strength (none, soft, medium, strong).
- **Show prices** toggle. If off, prices appear nowhere on the customer-facing form.
- **Show staff selection** toggle. If off, customers don't pick a staff member; the system assigns the first available.
- **Require phone** toggle. Phone field becomes required at the details step.
- **Success message** shown after a confirmed booking.
- **Pending message** shown after a booking that's awaiting admin approval (relevant only when Auto-confirm is off; without this set, customers see the success message and may think the booking is confirmed when it isn't).
- **Form rate limit (minutes).** Same-IP submissions inside this window are silently rejected. Default 2 minutes. Set to `0` to disable.

### Group classes (capacity > 1)

EP Booking is not just one-to-one appointments. Set a service's **Capacity** above 1 and that slot accepts that many concurrent bookings. Set the **Price label** to something like `"per person"` and the price displays as `£12 per person`. Use this for yoga classes, group workshops, fitness sessions. Buffer times still apply between the slot and the next.

### Buffer times

Each service has a **buffer before** and **buffer after** in minutes. These block the slots immediately adjacent to a booking so staff have time for cleanup or prep. They do NOT block whole days off. For days off, use staff exceptions.

### Booking statuses

Bookings move through these states:

| Status | Set by | What happens |
|---|---|---|
| **Pending** | New booking when Auto-confirm is off | No confirmation email yet. Waits for admin approval. |
| **Confirmed** | Auto-confirm on, or admin clicks Confirm | Confirmation email sent. Reminder will fire later. Zoom meeting created (if EP Booking Zoom is installed). |
| **Completed** | Admin marks after the appointment | Closes the booking. Used for reporting. |
| **Cancelled** | Customer cancellation link, or admin Cancel | Cancellation email sent. Stripe refund attempted if Auto-refund is on. |
| **No-Show** | Admin marks after a no-show | Booking closes without refund. Used for reporting. |

### Stripe Payments

- **API keys** for test and live modes (kept separate so you can switch without losing keys).
- **Currency**: GBP, USD, EUR, AUD, CAD, NZD, CHF, JPY.
- **Webhook secret** so Stripe can notify the plugin when payments settle.
- **Per-service Require Payment toggle** lets you mix paid and unpaid services in the same booking system.

#### Stripe webhook URL

Add this URL to your Stripe dashboard (Developers, Webhooks, Add endpoint):

```
https://YOUR-SITE.com/?ep_booking_stripe_webhook=1
```

Subscribe to `payment_intent.succeeded` and `payment_intent.payment_failed`. Copy the signing secret Stripe gives you back into EP Booking's Stripe Webhook Secret field. Without this, payments capture but the booking will not be marked paid.

#### Refunds

From the Bookings dashboard, the action menu on a paid booking includes Refund. The plugin calls Stripe and updates the booking. If the original charge does not exist on Stripe (e.g. imported from another system, or paid offline), the Refund button is inactive. There is also an Auto-refund-on-cancel toggle: when on, cancelling a paid booking triggers a Stripe refund automatically.

## Shortcodes

| Shortcode | Attributes | Purpose |
|---|---|---|
| `[booking-form]` | `title`, `service` (ID), `category` (name), `staff` (ID) | The full multi-step booking form. Pre-fill any step by passing the relevant attribute. Example: `[booking-form service=60-min-massage]`. |
| `[booking-services]` | `columns` (1, 2, 3), `show_prices`, `book_button`, `booking_page` (URL of the page hosting `[booking-form]`), `category` (ID) | Service catalogue grid. Each card optionally links to a prefilled booking form. |

`[booking_form]` and `[booking_services]` (underscore variants) are accepted as aliases.

## The customer flow

1. Customer lands on your booking page and sees the multi-step form.
2. **Step 1: service** — pick from the list (or already preset via shortcode attribute).
3. **Step 2: staff** — pick a specific staff member, or "Any available" (the form picks the first staff member with a free slot at the chosen time).
4. **Step 3: date** — calendar showing which dates have availability.
5. **Step 4: time** — slots for the chosen date based on staff schedule + existing bookings + capacity + buffers.
6. **Step 5: details** — name, email, phone, notes. Optional newsletter opt-in and GDPR consent.
7. **Step 6: pay** (if applicable) — Stripe checkout.
8. **Confirmation** — success message plus confirmation email (or pending message if Auto-confirm is off).

## Admin dashboards

- **Bookings.** Filterable list. Status column (Pending / Confirmed / Completed / Cancelled / No-Show). Per-booking actions: change status, cancel, refund via Stripe, add a timestamped admin note. The notes log is per-booking and visible only in the admin.
- **Calendar view.** Visual overview of bookings by date. Useful for spotting clashes and gaps.
- **Customers.** Contact records with booking history per customer. Search by name or email. Export to CSV.
- **Services, Staff, Categories.** CRUD interfaces for each.
- **Manual booking creation.** From the Bookings dashboard, create a booking on behalf of a customer (phone bookings, walk-ins). Select the service, staff, date, time and customer details. The booking goes straight in and the normal emails fire.
- **Staff Availability.** Per-staff weekly schedule (set start/end times per day of week). Per-staff Exceptions for date-specific overrides (holidays, days off, custom hours for one date).
- **Import / Export.** JSON and CSV for bulk moves between sites. See "Import / Export" below.

## Import / Export

Round-trips your full configuration between sites. Use it to migrate from a sandbox to live, back up before changes, or generate a fresh config from scratch with an AI assistant.

### What's exported

- **Settings:** business name and contact, timezone, opening hours, booking rules, form design, notification copy, integration toggles, currency. Stripe API keys and the webhook secret are deliberately NOT exported, so the JSON is safe to share or commit.
- **Categories, Services, Staff, Staff-Service assignments, Weekly Availability.**
- **Exceptions:** every per-staff date override (holidays, days off, custom hours).

Bookings themselves and customer records are not exported by Import/Export. They live on the site they were made.

### Duplicate handling on import

- **Add to existing records (default).** Existing entries are kept untouched; only new entries are inserted. Settings are NOT applied in this mode.
- **Replace existing records.** Existing entries with the same name (or email for staff, or date for exceptions) are overwritten with the imported version. Settings ARE applied.
- **Delete all existing records and import fresh.** Wipes categories, services, staff, availability, and exceptions before importing. Settings ARE applied. Bookings and customers are NOT deleted by this mode.

### Generate with AI

Inside the Import/Export dashboard, the **Generate with AI** panel exposes a copy-pastable prompt. Paste it into ChatGPT, Claude, or Gemini, answer the interview questions about your business, and the AI returns a valid JSON file you can drop straight into the importer. The prompt covers categories, services with capacity and buffers, staff with availability, holidays/exceptions, and basic settings.

### File formats

JSON and CSV both round-trip. JSON is easier to edit by hand or with an LLM. CSV is easier to spot-check in a spreadsheet. The CSV format uses `## Section` headers for each section.

## Integrations

- **EP Booking Zoom.** Install alongside. Every confirmed booking auto-creates a Zoom meeting; the join link lands in the customer's confirmation email via the `{zoom_url}` placeholder, and the staff host link via `{zoom_host_url}`.
- **EP Newsletter.** Optional opt-in checkbox on the booking form with list selection.
- **EP GDPR.** Consent logging on booking submissions, plus inclusion of booking data in DSR exports and erasures.
- **EP Affiliate.** Confirmed bookings fire an affiliate conversion, so referred bookings earn commission.
- **EP Connect (developer integration).** Each booking emits an inline event `booking.confirmed` with the full booking row, available to any plugin listening for it.
- **Stripe.** Payment capture, webhook verification, and admin-initiated refunds from the bookings list.

## Self-service cancellation

Every confirmation email includes a tokenised cancel link (`{cancel_url}`). The customer clicks it, confirms, and the booking is cancelled with no login required. The cancellation window setting controls how close to the appointment they can still cancel themselves. The token is single-use per booking and does not expire on its own; it stays valid until the booking is cancelled or deleted.

## How reminders are sent

The reminder email is fired by an in-process check that runs at most once every 60 seconds (so a high-traffic site sends them within a minute of the right time, and a low-traffic site within the next visit after that time). There is no separate external cron. If your site sees almost no traffic for hours, reminders may go out late by the same number of hours. For most sites this is invisible.

## Security

- Honeypot spam protection on the booking form.
- CSRF tokens on every endpoint.
- Rate limiting per IP so the form can't be scraped.
- Stripe webhook verification so fake payment confirmations can't mark bookings as paid.

## Troubleshooting

### "The form shows no available slots"

Check:
1. A staff member has been assigned to the service.
2. That staff member's availability schedule covers the date range customers are trying to book.
3. No holiday block is covering the date.
4. Existing bookings haven't filled every slot.

### "Confirmation emails aren't sending"

EP Email handles delivery. Check EP Email's delivery log. Common causes: SMTP config is wrong, from-address is unverified, or the email queue is stalled.

### "Stripe webhook says signature invalid"

The webhook secret in your EP Booking settings does not match the webhook endpoint secret in your Stripe dashboard. Rotate the secret on both sides.

### "I can't refund a booking from admin"

Stripe refunds require the original charge to exist on the Stripe side. If the booking was imported from a prior system or paid outside Stripe, the refund button is inactive. Refund through Stripe directly.

### "Customers are booking impossible slots"

Check the time slot interval and the staff duration. If a service is 45 minutes and your slot interval is 60 minutes, customers can still book at :00 and :15 adjacent slots. Tighten the interval to 15 minutes, or align durations to your interval.

### "The booking form submits but nothing appears in the admin"

Check for CSRF or rate-limiting errors in your browser's network tab. Both return a 403 that shows as a generic error in the form. The form rate limit silently rejects same-IP submissions inside the configured window (Form Design > Form rate limit).

### "I deleted a category but the services still exist"

Deleting a category does not cascade to its services. They keep their data and end up uncategorised. Either reassign them to a different category from the Services dashboard, or delete them individually.

### "Reminders are arriving late"

Reminders fire from an in-process check throttled to once per 60 seconds. The check runs on normal page requests, so on a low-traffic site reminders only fire when someone visits the site. If reliable timing matters, point a real cron job at any page on the site (e.g. `curl -s https://your-site.com/ > /dev/null` every minute) so the check runs even when no humans are browsing.

### "I imported a JSON but my settings didn't change"

Check the Duplicate Handling dropdown when you imported. The default "Add to existing records" mode preserves existing settings and only inserts new categories/services/staff. Pick "Replace existing records" or "Delete all and import fresh" if you want the imported settings to apply.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
