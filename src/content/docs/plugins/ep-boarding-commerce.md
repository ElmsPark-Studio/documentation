---
title: "EP Boarding — Ecommerce"
description: "Companion plugin that confirms an EP Boarding booking when its Stripe payment completes, and emails the customer. Required if you take card payment at the point of booking."
---

EP Boarding — Ecommerce is a small bridge between [EP Boarding](/plugins/ep-boarding/) and [EP Ecommerce](/plugins/ep-ecommerce/). It does one job: when a customer pays for a boarding booking, it marks that booking confirmed and sends the confirmation email.

This page documents EP Boarding — Ecommerce **1.0.1**.

Published by [ElmsPark Studio](https://elmspark.com).

## Why you need it

If you have turned on card payment in EP Boarding, the booking is created with a status of `awaiting_payment` and the customer is sent to checkout. Something has to notice when the money arrives and move the booking on. That is this plugin.

Without it, paid bookings sit in `awaiting_payment` for ever and nobody is told. **If you take payment at the point of booking, this plugin is not optional.**

If you do not take card payment, you do not need it.

## Requirements

- **PageMotor 0.9b or later**
- **[EP Boarding](/plugins/ep-boarding/)**, with payment enabled
- **[EP Ecommerce](/plugins/ep-ecommerce/) 0.1.25 or later**, with a payment provider configured, normally [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/)
- **[EP Email](/plugins/ep-email/)** for the confirmation email. If EP Email is not active it falls back to PHP `mail()`, which is far less reliable

## Installation

1. `ep-boarding-commerce.zip` comes with an EP Suite commerce-tier licence and ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. There is nothing to configure. It has no settings screen.

## What it does, step by step

1. It registers a `boarding_booking` product type with EP Ecommerce, so a booking order is recognised as its own kind of thing rather than falling through generic fulfilment.
2. When any order is fulfilled, it checks whether that order carries a `booking_id` in its metadata. If not, it does nothing.
3. If it does, the linked booking is moved from `awaiting_payment` or `pending` to **confirmed**.
4. The customer is emailed a confirmation listing every stay on the booking, with check-in and check-out dates, the Morning or Evening slot at each end, and the total paid.
5. If EP Boarding has an **admin email** configured, you are emailed too, with the booking reference, the owner's name and email, and the total.

## Things worth knowing

**It is idempotent.** The status update only applies to bookings currently sitting in `awaiting_payment` or `pending`, so if a payment webhook arrives twice the booking is not confirmed twice and the customer is not emailed twice.

**It carries a `Model: EP_Ecommerce` header.** That is what makes PageMotor load it during the Stripe confirmation request rather than only on normal page loads. Without that header the fulfilment hook would never fire at the moment it is needed.

**It confirms, it does not price.** All rates, availability and capacity logic stay in EP Boarding. This plugin never touches them.

**Emails go through EP Email when it is active.** It looks for an active EP Email plugin in either the theme or admin context and uses its `send()` method, falling back to PHP `mail()` only if EP Email is genuinely absent.

## Troubleshooting

**Bookings stay in "awaiting payment" after a successful card payment.** Check this plugin is active. Then check that EP Ecommerce is 0.1.25 or later, because the extension seam this relies on was added in that release.

**The booking confirms but no email arrives.** Check EP Email is active and its transport is configured. Test with EP Email's own delivery log, which records every send attempt.

**You get the customer email but not the admin copy.** The admin notification only sends when EP Boarding's **admin email** setting holds a valid address. Set it in EP Boarding's settings.

## Related plugins

- [EP Boarding](/plugins/ep-boarding/), the plugin this extends
- [EP Boarding — Services](/plugins/ep-boarding-services/), which adds EP Booking appointment services to the same booking widget
- [EP Ecommerce](/plugins/ep-ecommerce/) and [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/)

## Changelog

### 1.0.1

*Released 23 August 2026.*

- Adds the missing `Docs:` header, so the Updates screen now offers a documentation link. It had none before, which was found by sweeping every plugin in the suite for missing or dead documentation links rather than from a report.
- No other behaviour changed.

### 1.0.0

*Released 19 June 2026.*

- Initial release. Bridges EP Boarding and EP Ecommerce: when a boarding booking's payment completes, the booking is confirmed and the customer is emailed. Declares the `boarding_booking` product type, and carries the `Model: EP_Ecommerce` header so the fulfilment hook fires on the payment confirmation request.
