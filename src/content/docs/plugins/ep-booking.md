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

- **PageMotor 0.6 or later**
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

Three emails are configurable with templates:

- **Confirmation** — sent immediately after booking.
- **Reminder** — sent N hours before (configurable, typical 24).
- **Cancellation** — sent when a booking is cancelled.

Templates support placeholders: `{customer_name}`, `{service_name}`, `{booking_date}`, `{booking_time}`, `{staff_name}`, `{business_name}`, `{cancel_link}`, and more. An admin-alert toggle emails you too whenever a customer books.

### Form Design

Visual controls so the booking form matches your site's look:

- **Primary colour, accent colour, text colour.**
- **Corner rounding** on buttons and cards.
- **Max width** of the form container.
- **Card shadow** strength.

### Stripe Payments

- **API keys** for test and live modes.
- **Currency**: GBP, USD, EUR, AUD, CAD, NZD, CHF, JPY.
- **Webhook secret** so Stripe can notify the plugin when payments settle.
- **Per-service payment toggle** lets you mix paid and unpaid services in the same booking system.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[booking-form]` | The full multi-step booking form. Can be preset: `[booking-form service=60-min-massage]` or `[booking-form staff=alice]` or `[booking-form category=wellness]`. |
| `[booking-services]` | Service catalog grid. Each service links to a prefilled booking form. |

## The customer flow

1. Customer lands on your booking page and sees the multi-step form.
2. **Step 1: service** — pick from the list (or already preset via shortcode attribute).
3. **Step 2: staff** — pick a specific staff member, or "any available".
4. **Step 3: date** — calendar showing which dates have availability.
5. **Step 4: time** — slots for the chosen date based on staff schedule + existing bookings.
6. **Step 5: details** — name, email, phone, notes. Optional newsletter opt-in and GDPR consent.
7. **Step 6: pay** (if applicable) — Stripe checkout.
8. **Confirmation** — success message plus confirmation email.

## Admin dashboards

- **Bookings.** Filterable list. Status column (Pending / Confirmed / Cancelled / Completed). Actions to change status, cancel, refund via Stripe, or add notes.
- **Customers.** Contact records with booking history per customer.
- **Services, Staff, Categories.** CRUD interfaces for each.
- **Import / Export.** JSON and CSV for bulk moves between sites.

## Integrations

- **EP Booking Zoom.** Install alongside. Every confirmed booking auto-creates a Zoom meeting; the link lands in the confirmation email.
- **EP Newsletter.** Optional opt-in checkbox on the booking form with list selection.
- **EP GDPR.** Consent logging on booking submissions.
- **EP Affiliate.** Confirmed bookings fire an affiliate conversion, so referred bookings earn commission.
- **Stripe.** Payment, webhook verification, and admin-initiated refunds from the bookings list.

## Self-service cancellation

Every confirmation email includes a tokenised cancel link. The customer clicks it, confirms, and the booking is cancelled — no login required. The cancellation window setting controls how close to the appointment they can still cancel themselves.

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

Check for CSRF or rate-limiting errors in your browser's network tab. Both return a 403 that shows as a generic error in the form.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
