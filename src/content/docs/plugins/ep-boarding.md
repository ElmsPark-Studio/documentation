---
title: "EP Boarding"
description: "Date-range accommodation booking for PageMotor. Check-in and check-out with Morning and Evening slots, per-night rates, time-aware capacity, multiple stays per booking, a live availability calendar, Stripe payment and a client portal. Suits hotels, B&Bs, holiday lets and pet boarding."
---

EP Boarding is date-range booking: the hotel model rather than the appointment model. A customer picks a check-in day and a check-out day on a live availability calendar, chooses a Morning or Evening slot at each end, and is priced per night. One booking can hold several separate stays. Capacity is shared and checked per half-day, so a guest leaving in the morning frees that space for an arrival the same evening.

It suits hotels, B&Bs, holiday lets, and pet boarding and kennels.

This page documents EP Boarding **1.9.2**.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

What it does end-to-end:

1. You define **options** (a room type, a kennel grade, a training package) with a per-night rate, minimum and maximum nights, and the weekdays each option can be booked on.
2. You set **capacity**, which is the number of guests you can hold at once, and mark any **blocked dates** and **closed weekdays**.
3. A signed-in customer visits your booking page, picks an option, and picks their dates directly on a month calendar that shows how many spaces are free each day.
4. They choose a **Morning or Evening** slot for arrival and for departure. The price updates automatically as they change anything.
5. They can add **another stay** to the same booking, for a different set of dates, and the whole booking is checked for availability together.
6. They submit. Depending on your settings the booking is left pending for you to confirm, confirmed automatically, or held while they pay by card.
7. Confirmation emails go to the customer and to you, via EP Email.
8. The customer sees the booking in their **client portal**, with a printable receipt they can email to themselves.
9. You manage everything from the admin: confirm or cancel bookings, edit options and rates, and block dates on a calendar grid.

What EP Boarding is NOT: an appointment scheduler (that is [EP Booking](/plugins/ep-booking/), which handles staff, durations and time slots), a holiday-package or enquiry-first system (that is [EP Holiday Bookings](/plugins/ep-holiday-bookings/)), or a per-room inventory system. Capacity is a single shared pool, not a set of individually named and separately bookable rooms.

## Requirements

- **PageMotor 0.9b or later**
- **EP Suite base class** (bundled)
- **EP Email** for confirmation emails
- Customers must be able to **sign in**, because booking is login-gated. In practice that means [EP Membership](/plugins/ep-membership/) or another route that creates site accounts.

Optional:

- **EP Ecommerce** with Stripe configured, if you want to take payment at the point of booking
- **EP Boarding — Ecommerce**, the companion that confirms a booking when its payment completes. This is required for card payment to work correctly, see [Taking payment](#taking-payment)
- **EP Boarding — Services**, an add-on that puts EP Booking appointment services in the same dropdown as your stays
- **EP Courses**, whose courses then appear in the client portal

## Installation

1. `ep-boarding.zip` comes with an EP Suite commerce-tier licence and ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Work through the settings sections in this order: Settings (capacity and currency first) → Options & Rates → Unavailable Weekdays → Blocked Dates → Booking Page.
4. Create a page containing `[ep-boarding-booking]` and another containing `[ep-client-portal]`, then point the **Client portal page URL** setting at the second one.

## How availability works

This is the part worth understanding before you configure anything, because every other setting sits on top of it.

A day is split into two half-day **cells**, Morning and Evening. A stay occupies cells from its check-in cell up to, but not including, its check-out cell. A guest arriving Monday evening and leaving Wednesday morning occupies Monday evening and Tuesday (both cells), and does not occupy Wednesday.

The practical consequence: a departure frees space for an arrival on the same day. A guest collected on Saturday morning and a guest arriving on Saturday evening do not collide, and both fit within a capacity of one. Whole-day blocking, which is what most simple booking systems do, would wrongly reject the second booking.

**Capacity** is the number of stays that may occupy any one cell. Set it to 0 for unlimited. It is a single shared pool across every option, so an option is not a separate room with its own capacity.

A cell is bookable when it is below capacity, its date is not blocked, and its weekday is not closed. Closed weekdays are only checked for the days a guest is actually present, so a closed Sunday still allows a Saturday evening arrival with a Sunday morning departure.

## Setting up the basics

### Options and rates

Under **Options & Rates**, each option has:

- **Name**, used in the admin and in emails.
- **Frontend display label** (optional). Type exactly what customers should see, for example `Residential Recall Training, £850.00 five nights min.` Leave it blank and the booking form shows the name and the per-night price automatically.
- **Price per night**.
- **Extra-night rate (beyond min nights)**. Nights above the minimum bill at this rate instead. This exists for package options: a five-night package charges the package rate for five nights, and your standard nightly rate for any night beyond that. Leave it at 0 to charge every night at the per-night price.
- **Min nights (1 = 24h minimum)** and **Max nights (0 = no max)**. If you want a package to be extendable, its maximum must be higher than its minimum.
- **Available on these days**. Untick a weekday to stop this one option being booked on it.
- **Description**.

Options can be deactivated rather than deleted, which removes them from the booking form and keeps their history intact.

### How a stay is priced

The base price is the number of nights multiplied by the per-night rate, or the package split described above when an extra-night rate is set.

The arrival and departure slots then adjust it:

| Arrival → departure | Adjustment | Why |
|---|---|---|
| Morning → Morning | none | a clean 24-hour cycle |
| Evening → Evening | none | a clean 24-hour cycle |
| Morning → Evening | **plus** the daycare add-on | the guest is present for an extra daytime |
| Evening → Morning | **minus** the short-stay discount | the stay is under 24 hours |

Both amounts are global, under **Settings**, and default to 70 and 20 in your chosen currency. The breakdown shown to the customer names the reason for any adjustment.

Pricing is always calculated on the server, so the figure cannot be altered from the browser.

### Unavailable weekdays

A Monday to Sunday panel of days you are closed. These override everything else and apply to every option. Use the per-option **Available on these days** for a restriction that applies to one option only.

### Blocked dates

Individual dates that cannot be booked at all, managed on a month grid.

### Booking page

- **Intro text** shown above the booking form. Leave blank for none.
- **Night count**, a checkbox that hides the number of nights from the price breakdown. Nights are shown by default.
- **Client portal page URL**, the page holding the `[ep-client-portal]` shortcode. Defaults to `/account/`.
- **Login page URL**, where visitors who are not signed in are sent. Defaults to `/login/`.

### Settings

- **Total capacity (0 = unlimited)**, described above.
- **Currency**: GBP, USD, EUR, AUD, CAD or NZD.
- **Minimum advance notice (days)**, how far ahead a check-in must be.
- **Daycare add-on** and **Short-stay discount**, the two slot adjustments.
- **Notify this email of new requests**.
- **Auto-confirm**, which confirms bookings as they arrive instead of leaving them pending. It is ignored when payment is required, because paying is what confirms.

### Taking payment

**Require payment to book** takes card payment for the booking at the moment of booking, and **Amount to charge (% of total)** sets how much (100 is payment in full, lower takes a deposit and you arrange the balance separately).

This reuses your existing [EP Ecommerce](/plugins/ep-ecommerce/) Stripe configuration, so there are no new card keys to set up.

Two things to know before you switch it on:

**You also need the EP Boarding — Ecommerce companion.** EP Boarding itself has no path from "awaiting payment" to "confirmed"; the companion is what marks a booking confirmed when its Stripe payment completes. Without it a customer can pay and still have the booking released, because a booking awaiting payment is automatically cancelled after 30 minutes to stop abandoned checkouts holding space. Ask ElmsPark for the companion before enabling payment.

**A booking awaiting payment holds its space** for those 30 minutes, so the customer cannot lose the dates while they are entering their card.

## Shortcodes

| Shortcode | What it renders |
|---|---|
| `[ep-boarding-booking]` | the booking widget: option, availability calendar, slots, price breakdown |
| `[ep-client-portal]` | the customer's own area: bookings, purchases, courses, receipts |

The older forms `[boarding-booking]`, `[boarding_booking]`, `[client-portal]` and `[client_portal]` still work, so existing pages keep rendering, but they are deprecated. Use the `ep-` prefixed versions on new pages. PageMotor's shortcode registry is first-wins and core plugins load before yours, so an unprefixed name can be silently taken over by a core shortcode of the same name.

## The customer flow

Booking requires a signed-in account. A visitor who is not signed in sees a short prompt with a link to your login page instead of the form, and the booking action itself is gated too, not just the form.

Once signed in, their name and email are filled in from the account. The email is read-only, so a booking is always tied to the right person.

They then pick an option, click their check-in day on the calendar and then their check-out day. If the option has a minimum stay, the minimum is selected for them, they can extend it by clicking a later day, and only start dates with enough consecutive free nights are selectable. Choosing the slots and adding any notes completes a stay.

**Add another stay** keeps what they have built and starts a fresh one, so a single booking can hold several separate date ranges. Each saved stay can be removed again. Prices and availability update automatically as they go, roughly half a second after they stop changing things.

## The client portal and receipts

`[ep-client-portal]` gives a customer one page showing their bookings with nights, status and total, anything they have bought through EP Ecommerce, and their EP Courses courses. The purchase and course sections only appear when those plugins are present.

Each booking has a **View receipt** link to a clean printable confirmation with a Print button and an "Email me a copy" action. Receipts are restricted to the account that owns the booking.

## Admin dashboards

Three sections, all inside the plugin's settings screen:

- **Bookings**, the list of requests and confirmed stays, where you confirm, cancel or delete.
- **Options & Rates**, covered above.
- **Blocked Dates**, a month grid for closing individual dates.

A booking has one of four statuses: **pending** (submitted, waiting for you), **confirmed**, **awaiting payment** (in checkout, held for 30 minutes) and **cancelled**.

## The private calendar feed

EP Boarding can publish every confirmed and pending stay as an iCalendar feed, so you can subscribe to your bookings in Google Calendar or Apple Calendar and see them alongside everything else. Each stay becomes an all-day event carrying the option, the arrival and departure slots, and the owner's contact details and notes.

The feed is protected by a secret token in its URL rather than a password, so treat the URL as confidential and do not publish it.

The subscribe URL is not currently shown anywhere in the admin screens, so ask ElmsPark for your site's feed URL.

## Add-ons and the extension seam

Another plugin can add its own entries to the booking dropdown and take over the widget body when one of them is chosen. This is how **EP Boarding — Services** offers a single booking page covering both overnight stays and [EP Booking](/plugins/ep-booking/) appointment services.

For developers: an add-on implements `boarding_dropdown_options()` to contribute entries, and optionally `boarding_ext_config()` to pass a JSON config to its own frontend script. When one of its entries is selected the native stays flow hides and the add-on renders into `.ep-boarding-ext-body`, with `epb:ext-enter` and `epb:ext-exit` events fired on the widget. With no add-on installed, nothing about the stays flow changes.

## Integrations

- **EP Email** sends the confirmations.
- **EP Ecommerce** provides the Stripe configuration for card payment, and its orders appear in the client portal.
- **EP Courses** courses appear in the client portal.
- **EP Membership** (or equivalent) provides the accounts that booking requires.

## Security

Booking is login-gated at both the form and the action. Prices and availability are always recalculated on the server, so a tampered browser request cannot change what is charged or book a full date. Admin actions are CSRF-protected, and the frontend sets its own CSRF cookie. Receipts are readable only by the account that owns them, and the calendar feed is gated by a secret token compared in constant time.

## Troubleshooting

### "Please log in to make a booking" is showing to everyone

Booking requires an account, by design. Check the **Login page URL** setting points at a real login page, and that visitors have a way to register.

### The booking form has no styling

Confirm the plugin activated cleanly. The frontend stylesheet loads through PageMotor's sitewide CSS valet, so a plugin that failed to load will render the form as unstyled markup.

### A customer paid but the booking was cancelled

The **EP Boarding — Ecommerce** companion is missing. Without it nothing marks a paid booking as confirmed, so the 30-minute sweep for abandoned checkouts cancels it. See [Taking payment](#taking-payment).

### Nobody can book a date that looks free

Work through the three gates in order: the weekday may be closed under **Unavailable Weekdays** or unticked on that option, the date may be in **Blocked Dates**, or the cell may be at capacity. Also check **Minimum advance notice**, which silently rules out dates that are too soon.

### A package option cannot be extended

Its **Max nights** is not higher than its **Min nights**, so there is no room to add a night. Raise the maximum, or set it to 0 for no limit.

### Two stays that should fit are colliding

Check the slots. Availability is per half-day, so a Morning departure and an Evening arrival on the same date do fit, but two Morning arrivals do not when capacity is one.

### Confirmation emails are not arriving

EP Email handles delivery. Check its delivery log first: the usual causes are an unverified from-address, wrong SMTP settings, or a stalled queue.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger, a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
