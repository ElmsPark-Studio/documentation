---
title: "EP Boarding — Services"
description: "Add-on that puts EP Booking appointment services, such as a Meet and Greet, inside the EP Boarding booking widget, so customers book a stay and an appointment from one page."
---

EP Boarding — Services lets one booking page offer two different kinds of booking. Your overnight stays come from [EP Boarding](/plugins/ep-boarding/). Your appointments, a Meet and Greet or an assessment visit, come from [EP Booking](/plugins/ep-booking/). This add-on puts both in the same dropdown.

This page documents EP Boarding — Services **1.1.1**.

Published by [ElmsPark Studio](https://elmspark.com).

## The problem it solves

Boarding and appointments are genuinely different models. A stay is priced per night across a date range with a Morning or Evening slot at each end. An appointment is a fixed-duration slot on one day with a named member of staff.

Running them as two separate systems is correct engineering and poor customer experience: the customer has to know which page to visit before they know what they want. This add-on keeps the two engines separate and joins them at the front.

## Requirements

- **PageMotor 0.9b or later**
- **[EP Boarding](/plugins/ep-boarding/) 1.9.0 or later**, which is the release that added the extension seam this hooks into
- **[EP Booking](/plugins/ep-booking/)**, active and configured, with at least one active service that has an active member of staff assigned to it

If EP Booking is not active, or its services table is missing, the add-on quietly contributes nothing and your boarding widget behaves exactly as it did before.

## Installation

1. `ep-boarding-services.zip` comes with an EP Suite commerce-tier licence and ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. There is nothing to configure. It has no settings screen. Your existing EP Booking services appear in the boarding widget straight away.

## How it behaves

**Which services appear.** Every EP Booking service with a status of `active` that has at least one active member of staff assigned to it. Services with no staff are left out, because they cannot be booked.

**How they are labelled.** The service name, followed by its duration in minutes in brackets, for example `Meet and Greet (30 min)`. Ordering follows EP Booking's own sort order, then name.

**What the customer sees.** Selecting a service swaps the widget body from the stay calendar to a date picker and a time-slot picker, styled to match the rest of the booking page. Days with no availability are greyed out, whether that is a day off, a fully booked day, or a day outside your booking window, so a customer can only pick a day that actually has times. Split-shift gaps in EP Booking's schedule are respected automatically.

**Who does the work.** Availability and the booking itself are handled entirely by EP Booking's own endpoints. This add-on duplicates no scheduling logic, so it cannot drift out of step with EP Booking's rules.

**Which settings it respects.** It reads EP Booking's own configuration and passes it through: whether a phone number is required, the minimum advance notice in hours, and the maximum booking window in days. Change them in EP Booking and the widget follows.

## Installing and removing safely

This is an add-on in the true sense. It adds entries to a dropdown and renders a picker. It creates no database tables and stores no settings of its own.

Deactivating it reverts the booking page to stays only. Nothing is lost, and appointments already made through it remain in EP Booking exactly as if they had been booked on EP Booking's own page.

## Things worth knowing

**Assets are cache-busted by file modification time.** CSS and JavaScript URLs carry a `?v=` stamp taken from the file's mtime, so a plugin update reaches browsers without anyone needing a hard refresh.

**It does not pull in the EP Suite base class.** It is deliberately lightweight and resolves its own asset URLs from PageMotor's user-plugins constant, which keeps it independent of the shared trait.

## Troubleshooting

**No services appear in the dropdown.** Check EP Booking is active. Then check the service's status is `active` and that it has at least one active member of staff assigned. A service with no staff is filtered out by design.

**The picker appears but no slots are offered.** That is EP Booking's availability answering, not this add-on. Check the staff schedule, the minimum advance notice, and the maximum advance window in EP Booking.

**The picker looks unstyled.** Confirm the plugin's CSS is loading, and that no site-wide CSS is overriding it. The stylesheet is registered site-wide.

## Related plugins

- [EP Boarding](/plugins/ep-boarding/), the plugin this extends
- [EP Booking](/plugins/ep-booking/), which owns the appointment side
- [EP Boarding — Ecommerce](/plugins/ep-boarding-commerce/), required if you take card payment for stays

## Changelog

### 1.1.1

*Released 23 August 2026.*

- Adds the missing `Docs:` header, so the Updates screen now offers a documentation link. It had none before, which was found by sweeping every plugin in the suite for missing or dead documentation links rather than from a report.
- No other behaviour changed.

### 1.1.0

*Released 19 June 2026.*

- The service date picker now greys out days with no availability, whether a day off, a fully booked day, or a day outside the booking window, so customers can only pick a day that has times. Split-shift gaps in EP Booking are respected automatically. Requires EP Booking 1.1.0 or later, which added the available-days endpoint.

### 1.0.0

*Released 19 June 2026.*

- Initial release. Surfaces EP Booking appointment services inside the EP Boarding booking widget as one unified dropdown. Selecting a service shows a date picker and time slots styled to match the widget, and books through EP Booking's own endpoints so availability and booking logic are never duplicated. Only services that are active and assigned to active staff appear.
