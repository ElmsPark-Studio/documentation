---
title: "EP Booking"
description: "Online appointment scheduling for PageMotor. Timezone-correct bookings, calendar invites, self-serve rescheduling, reminder ladders, public booking pages, cross-site embeds, webhooks, an admin calendar, round-robin staff assignment and external calendar sync."
---

EP Booking is a full appointment-scheduling system. Services, staff, availability schedules, a multi-step booking form your customers fill out on your site (in their own timezone), Stripe payments, calendar invites, self-serve rescheduling, a multi-tier reminder ladder, public per-service booking pages, an embeddable widget for any website, signed webhooks, an admin calendar, and (via the companion add-on) automatic Zoom meeting creation.

This page documents EP Booking **2.4.1**. If you are on a 1.x version, take the update from your admin Updates screen; the [upgrading section](#upgrading-from-1x) covers the one setting to check first.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

What it does end-to-end:

1. You define **services** (haircut, consultation, massage) with price and duration.
2. You define **staff** with individual availability schedules, which services they offer, and optionally a personal calendar feed that blocks their slots.
3. A customer visits your site (or your public booking page, or the widget embedded on another site), picks a service, picks a staff member (optional), picks a date and a time slot, with every time shown in **their own timezone**.
4. They enter their details, optionally pay via Stripe, and confirm.
5. Automated emails go out: a confirmation carrying a **calendar invite** (.ics), then reminders on your configured ladder (up to 7 days, 24 hours and 1 hour before).
6. The customer can **reschedule or cancel themselves** from links in the confirmation email, within your configured window.
7. Your admin panel shows the booking in a filterable list and on a **month calendar**. You can confirm, cancel, reschedule or refund from the admin.
8. If you use webhooks, your CRM or automation platform is notified of every booking event, with an HMAC signature to verify.
9. If EP Booking Zoom is installed, a Zoom meeting was created automatically and the link is in the confirmation email and the invite.

What EP Booking is NOT: a calendar app, a resource scheduler for rooms, or a class-booking system for group events. It is appointment-by-appointment scheduling between one customer and one staff member.

## Requirements

- **PageMotor 0.10.3b or later** (the 2.x line relies on 0.10 core plugin APIs; 1.x supported 0.8.2b+)
- **EP Suite base class** (bundled)
- **EP Email** (required for notifications)

Optional add-ons:

- **EP Booking Zoom** for auto-created Zoom meetings
- **EP Cron** for reliable reminder delivery on quiet sites (without it, reminders piggyback on page loads)
- **EP Newsletter** to offer opt-in on the booking form
- **EP GDPR** for consent logging
- **EP Affiliate** to attribute bookings to referrers

## Installation

1. `ep-booking.zip` comes with an EP Suite licence, and ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Work through the settings sections in this order: General → Services → Staff → Categories → Booking Rules → Notifications → Form Design → Payments → Booking Form.

## Upgrading from 1.x

The 2.x line converts your bookings to be anchored in universal time (UTC), so daylight-saving changes and international customers can never shift an appointment. The conversion runs automatically on your first admin visit after updating, and it uses one setting to interpret your existing bookings:

**Before you update, check Settings → General → Business Timezone** and make sure it names your actual business timezone (for example `Europe/London`). Everything in 2.x derives from it: availability, slot generation, reminders, invites and the one-off conversion of your existing bookings.

Everything else is opt-in. Rescheduling, public pages, webhooks and round-robin assignment are all off by default, so nothing about your live booking flow changes until you switch a feature on.

## Setting up the basics

### General

- **Business name, address, phone** for notification emails.
- **Opening / closing times** are the outer envelope of when bookings are possible. Individual staff schedules can be tighter.
- **Business Timezone.** The single most important setting. All availability, booking maths and reminders derive from it.

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
- **Availability schedule**, a recurring weekly pattern (e.g. Mon-Fri 9-5, Wed off).
- **Holiday blocks**, specific date ranges to mark unavailable.
- **Services offered**, picked from your service list.
- **Busy calendar (ICS URL)**, optional. Paste a secret ICS address from their Google, Outlook or Apple calendar and events on it block their booking slots. See [external calendar sync](#external-calendar-sync-free-busy).

### Categories

Optional. Groups services for display on the booking form and the `[booking-services]` catalog shortcode.

### Booking Rules

- **Minimum advance time.** Can't book less than N hours before the slot.
- **Maximum advance time.** Can't book more than N days ahead.
- **Default duration** for services that don't override.
- **Time slot interval.** How finely slots are offered: 15, 20, 30, or 60 minutes.
- **Cancellation window.** Customer can cancel (or reschedule) themselves up to N hours before the booking.
- **Self-Serve Rescheduling.** Adds a reschedule link to confirmation emails so customers can move their own appointment. Off by default.
- **"Any Available" Assignment.** How a booking is assigned when the customer picks "Any Available": *List order (legacy)* always favours the first listed staff member; *Least recently booked (round-robin)* shares work evenly across the team. See [round-robin assignment](#round-robin-staff-assignment).
- **Auto-confirm?** If off, bookings start in Pending and you manually confirm each one.

### Notifications

Four emails are configurable with templates:

- **Confirmation**, sent immediately after booking, with the calendar invite attached.
- **Reminder**, sent on the ladder you pick in **Reminder Schedule**: *24 hours + 1 hour before* (recommended), *7 days + 24 hours + 1 hour*, or a single 24-hour or 1-hour reminder. Each tier sends once, timed from the exact appointment instant; appointments booked inside a tier's window simply skip that tier.
- **Rescheduled**, sent after a customer moves their booking, with the updated invite attached.
- **Cancellation**, sent when a booking is cancelled, with a cancellation invite that removes the event from the customer's calendar.

Templates support placeholders: `{customer_name}`, `{service_name}`, `{booking_date}`, `{booking_time}`, `{staff_name}`, `{business_name}`, `{cancel_url}`, `{reschedule_url}`, and more. The rescheduled template additionally supports `{old_booking_date}` and `{old_booking_time}`. An admin-alert toggle emails you too whenever a customer books.

The default confirmation template includes the reschedule link automatically when rescheduling is enabled; if you have written your own template, add `{reschedule_url}` where you want it.

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

## Timezones

EP Booking is timezone-correct end to end:

- **Your availability is defined in your Business Timezone.** A 9-to-5 Tuesday schedule means 9-to-5 in your local wall-clock time, on both sides of a daylight-saving change.
- **Visitors see slots in their own timezone.** The form detects the visitor's timezone and renders every slot label in it, with a note saying so, and a day marker when a slot falls on a different calendar day for them. A client in New York booking your 09:00 London slot sees 4:00 am, and both of you hold the same instant.
- **Bookings are stored as universal instants.** Reminders, invites and rescheduling all work from the exact UTC moment, so nothing drifts when the clocks change.

## Calendar invites (ICS)

Every confirmation email attaches a standards-compliant `.ics` invite that lands the appointment in Apple Calendar, Outlook or Google Calendar at the correct local time, with a built-in 1-hour alarm. When a booking is rescheduled the updated invite **moves** the existing calendar event rather than duplicating it, and a cancellation sends the matching cancellation file so the event is struck through or removed. If EP Booking Zoom is installed, the Zoom join link is the event's location.

## Self-service rescheduling

Enable **Booking Rules → Self-Serve Rescheduling** and every confirmation email carries a reschedule link. The customer lands on a plain page (no login, no JavaScript required) showing their current booking and a date picker of genuinely open slots. The move applies atomically: the slot is re-checked at the moment of submission, the updated invite goes out, the Zoom meeting is recreated, and pending reminders re-arm for the new time. The **cancellation window** doubles as the reschedule cutoff.

## Public booking pages and the embed widget

Enable **Public Pages & Embed → Public Booking Pages** and every active service gets its own shareable booking page URL, ideal for email signatures, social bios and QR codes. The settings panel lists the URL for each service.

The same panel gives you a one-line embed snippet:

```html
<script src="https://YOUR-SITE/…/ep-booking-embed.js" data-ep-booking="SERVICE-SLUG" async></script>
```

Paste it into any website (a partner's site, a landing page, anywhere) and a fully working, auto-resizing booking widget appears there, while your PageMotor site processes the booking exactly as normal. Optional `data-staff="ID"` pins the widget to one staff member. Copy the snippet from the settings panel rather than this page, as it carries your site's real URL.

## Webhooks

Set **Webhooks → Webhook URL** and EP Booking POSTs a JSON payload to it on four events: `booking.created`, `booking.confirmed`, `booking.rescheduled` and `booking.cancelled`. Delivery is best-effort with a 3-second timeout; failures are logged, never retried, and can never block or slow a customer's booking.

Set a **Signing Secret** and every delivery carries an `X-EP-Booking-Signature: sha256=…` header, the HMAC-SHA256 of the raw body. Verify it before trusting the payload. Use webhooks to wire bookings into a CRM, an automation platform, or your own dashboard.

## The admin Calendar

The **Calendar** section of the settings screen shows a month grid of every booking, colour-coded by status, with customer and service details on hover and previous/next month navigation. The bookings list remains the place to act on a booking; the calendar is the at-a-glance view of the month's shape.

## Round-robin staff assignment

By default, "Any Available" bookings go to the first listed staff member who is free (the behaviour of every earlier version). Switch **Booking Rules → "Any Available" Assignment** to *Least recently booked (round-robin)* and the work is shared: each slot is offered under the team member who was booked longest ago, with ties broken by fewest upcoming appointments, then list order. Staff-specific bookings and each person's exclusive hours are unaffected; only the choice among equally available team members changes.

## External calendar sync (free-busy)

Give any staff member a **Busy calendar (ICS URL)** in the Staff editor and events on that calendar block their booking slots. This is the provider-agnostic route: Google Calendar, Outlook and Apple Calendar all offer a secret ICS address for exactly this purpose, with no accounts to connect and no API keys.

- Timed events, all-day events and daily/weekly **recurring events** are all honoured.
- Feeds are checked at most every five minutes, so a change on the external calendar takes up to five minutes to affect the booking form.
- If a feed is temporarily unreachable, the last fetched copy is used; if there is no copy at all, slots stay **open** rather than your booking page going blank, and the failure is logged.

The ICS URL is a secret: anyone holding it can read that calendar's events. Use the calendar provider's "reset private address" if it ever leaks.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[booking-form]` | The full multi-step booking form. Can be preset: `[booking-form service=60-min-massage]` or `[booking-form staff=alice]` or `[booking-form category=wellness]`. |
| `[booking-services]` | Service catalog grid. Each service links to a prefilled booking form. |

## The customer flow

1. Customer lands on your booking page and sees the multi-step form.
2. **Step 1: service** — pick from the list (or already preset via shortcode attribute, public page, or embed).
3. **Step 2: staff** — pick a specific staff member, or "any available".
4. **Step 3: date** — calendar showing which dates have availability.
5. **Step 4: time** — slots for the chosen date, shown in the customer's own timezone, based on staff schedule, existing bookings and any external busy calendar.
6. **Step 5: details** — name, email, phone, notes. Optional newsletter opt-in and GDPR consent.
7. **Step 6: pay** (if applicable) — Stripe checkout.
8. **Confirmation** — success message plus confirmation email with the calendar invite and, if enabled, the reschedule link.

## Admin dashboards

- **Bookings.** Filterable list. Status column (Pending / Confirmed / Cancelled / Completed). Actions to change status, cancel, refund via Stripe, or add notes.
- **Calendar.** Month grid of all bookings, colour-coded by status.
- **Customers.** Contact records with booking history per customer.
- **Services, Staff, Categories.** CRUD interfaces for each.
- **Import / Export.** JSON and CSV for bulk moves between sites.

## Integrations

- **EP Booking Zoom.** Install alongside. Every confirmed booking auto-creates a Zoom meeting; the link lands in the confirmation email and the calendar invite, and the meeting is recreated when a booking is rescheduled.
- **EP Cron.** When present, reminders ride its heartbeat instead of waiting for a page load, which matters on quiet sites.
- **EP Newsletter.** Optional opt-in checkbox on the booking form with list selection.
- **EP GDPR.** Consent logging on booking submissions.
- **EP Affiliate.** Confirmed bookings fire an affiliate conversion, so referred bookings earn commission.
- **Stripe.** Payment, webhook verification, and admin-initiated refunds from the bookings list.

## Self-service cancellation

Every confirmation email includes a tokenised cancel link. The customer clicks it, confirms, and the booking is cancelled with a cancellation invite removing the event from their calendar — no login required. The cancellation window setting controls how close to the appointment they can still cancel (or reschedule) themselves.

## Security

- Honeypot spam protection on the booking form.
- CSRF tokens on every endpoint.
- Rate limiting per IP so the form can't be scraped.
- Stripe webhook verification so fake payment confirmations can't mark bookings as paid.
- Outbound webhook deliveries are HMAC-signed when a secret is set.
- Reschedule and cancel links use one unguessable token per booking, checked together with the booking's email address.

## Troubleshooting

### “The form shows no available slots”

Check:
1. A staff member has been assigned to the service.
2. That staff member's availability schedule covers the date range customers are trying to book.
3. No holiday block is covering the date.
4. Existing bookings haven't filled every slot.
5. If the staff member has a busy calendar URL, events on that external calendar may be blocking the slots. Remember all-day events block the whole day.

### “Slot times look wrong to a customer”

Almost always the Business Timezone. The form deliberately shows each visitor their own local time, so a customer abroad seeing a different clock time than you is correct behaviour, and the form says "times shown in your timezone". But if times are wrong for local customers too, check **Settings → General → Business Timezone** names your real timezone.

### “Confirmation emails aren't sending”

EP Email handles delivery. Check EP Email's delivery log. Common causes: SMTP config is wrong, from-address is unverified, or the email queue is stalled.

### “Reminders aren't going out”

The ladder needs something to wake it. On busy sites page loads are enough; on quiet sites install EP Cron so reminders ride its heartbeat. Also remember each tier sends once, and an appointment booked inside a tier's window (e.g. booked 3 hours ahead, 24-hour tier) skips that tier by design.

### “My webhook endpoint isn't receiving events”

Deliveries are fire-and-forget with a 3-second timeout, and failures are logged to the PHP error log rather than retried. Check the endpoint responds within 3 seconds, and if you set a signing secret, make sure you are verifying `X-EP-Booking-Signature` against the raw request body, not a re-serialised copy.

### “Stripe webhook says signature invalid”

The webhook secret in your EP Booking settings does not match the webhook endpoint secret in your Stripe dashboard. Rotate the secret on both sides.

### “I can't refund a booking from admin”

Stripe refunds require the original charge to exist on the Stripe side. If the booking was imported from a prior system or paid outside Stripe, the refund button is inactive. Refund through Stripe directly.

### “Customers are booking impossible slots”

Check the time slot interval and the staff duration. If a service is 45 minutes and your slot interval is 60 minutes, customers can still book at :00 and :15 adjacent slots. Tighten the interval to 15 minutes, or align durations to your interval.

### “The booking form submits but nothing appears in the admin”

Check for CSRF or rate-limiting errors in your browser's network tab. Both return a 403 that shows as a generic error in the form.

### “The embedded widget doesn't appear on the other site”

The snippet must be pasted as-is from the settings panel (it carries your site's URL), and **Public Booking Pages** must be enabled: the widget loads the public page in an iframe, so turning public pages off turns the widget off too.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
