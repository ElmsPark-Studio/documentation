---
title: "EP Stripe — Discount Codes"
description: "Create, list, enable and disable Stripe promotion codes from the PageMotor admin. Works with any EP plugin whose Stripe checkout has promotion codes enabled."
---

EP Stripe — Discount Codes puts Stripe promotion codes in your PageMotor admin, so you can run a discount without opening the Stripe dashboard. Create a code, watch it get used, switch it off when the promotion ends.

It does not process payments itself. It manages the codes that your existing Stripe checkouts accept.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Use cases:

- **A launch discount.** Create `LAUNCH20` at 20% off, capped at the first 50 redemptions.
- **A time-limited seasonal offer.** Set a deadline and let Stripe stop accepting the code on its own.
- **A one-off goodwill discount** for a specific customer, switched off once used.

## What it works with

Any EP plugin whose Stripe checkout has promotion codes enabled, including [EP Ecommerce Stripe](/plugins/ep-ecommerce-stripe/) and [EP Booking](/plugins/ep-booking/). The code is created in your Stripe account, so any checkout on that account that accepts promotion codes will accept it.

If a code is rejected at checkout, the usual cause is that the checkout session was not created with promotion codes enabled. That is a setting on the checkout, not on the code.

## Requirements

- **PageMotor 0.9 or later**
- **EP Suite base class** (bundled with the plugin)
- **A Stripe account**, and its secret key for whichever mode you are working in

## Installation

1. `ep-stripe-coupons.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Open **Plugin Settings → EP Stripe — Discount Codes**.

## Settings

| Setting | What it does |
| --- | --- |
| **Stripe Mode** | Test or Live. Decides which key is used and which set of codes you are managing. |
| **Test Secret Key** | Starts with `sk_test_`. The sandbox account. |
| **Live Secret Key** | Starts with `sk_live_`. Codes created here discount real money. |
| **Discount Codes** | The working panel: create a code, list existing ones, enable or disable each. |

### Test and Live are separate worlds

Codes are mode-scoped. A code created in Test only works on test payments, and a code created in Live only works on real ones. If you want the same code available in both, create it twice, once in each mode. This catches people out: the code works perfectly in testing, then does nothing on the live site, because it was only ever created in the sandbox.

## Creating a code

You give it four things:

- **Code** — letters and numbers, up to 40 characters. It is uppercased for you, so `spring24` becomes `SPRING24`.
- **Discount** — a percentage between 1 and 100.
- **Maximum redemptions** — optional. Leave it empty for unlimited.
- **Deadline** — optional. After it passes, Stripe stops accepting the code.

Behind the scenes each code is two Stripe objects: a **coupon**, which holds the discount itself, and a **promotion code**, which is the text the customer types, bound to that coupon. You only deal with the one form; both are created together.

Two deliberate limits worth knowing before you plan a promotion:

- **Percentage discounts only.** Fixed-amount discounts are not offered, because an amount is tied to a currency and a percentage is not.
- **Discounts apply once**, not to every invoice of a subscription.

If you need either of those, create the coupon directly in the Stripe dashboard.

## Enabling and disabling

Disabling a code stops it being accepted at checkout without deleting anything, so redemption history stays intact and you can switch it back on. Prefer this to deleting a code that is already out in the world.

## Troubleshooting

**"No Stripe secret key set for … mode."** You are in a mode whose key is blank. Either paste that key or switch mode.

**The code works in test but not live.** It was only created in Test. Create it again in Live.

**The code is rejected at an EP checkout.** That checkout session probably does not have promotion codes enabled. Check the paying plugin's settings, not this one.

## Changelog

### 0.1.5

- **Fixes stored keys and passwords reading as empty after a PageMotor 0.11.3 or 0.11.4 update.** After the core update, every secret this plugin had encrypted at rest came back blank, so anything that needed it failed with an authentication error until the value was typed in again. Nothing was deleted: the encrypted value was still in the settings row, but PageMotor 0.11.3 moved the site secret that opens it, and this plugin was still looking in the old place. It now finds the secret in both places, so an existing value opens again without re-entry, and a value that was re-entered in the meantime keeps working and is moved back under the site secret.
- If you updated PageMotor and then re-entered a key or password, there is nothing to do. If you updated and have not re-entered it, this release restores it on the next page load.

### 0.1.4

*Released 1 September 2026.*

- **Fixed: installing a second plugin that also takes Stripe payments could take the whole site down.** Five plugins in the suite share the same Stripe helper. With any two of them switched on, the second to load failed outright and PageMotor disabled it to protect the site, so turning on a new Stripe-capable plugin silently cost you the one you already had, with nothing obvious to explain it.
- The guard meant to prevent that had never been able to work, for reasons of when the code is read rather than when it runs. It is now written so that it does. Verified by switching two of these plugins on together: previously the site returned an error and one plugin was disabled, now both load cleanly and payment signature checking still works.

### 0.1.3

*Released 31 August 2026.*

- **Your Stripe test and live secret keys are now stored encrypted.** Until this release they sat in plain text in the plugin's settings, where anyone holding an API or MCP connection to your site with permission to configure plugins could read them straight back out. Your site's visitors were never able to see them.
- Existing sites convert themselves the next time the plugin loads, once. There is nothing to re-enter and no keys to replace.
- Reading your settings over the API now returns a placeholder rather than the value, and writing that placeholder back leaves the stored secret untouched. Clearing it by submitting an empty value still works as before.
- On hosting without encryption support the previous behaviour is kept and the reason is written to the log, because quietly discarding a working key would be worse than the exposure this closes.

### 0.1.2

Fixes "Your session has expired. Please reload to ensure your security." on PageMotor 0.11, which affected the discount codes panel in admin. The CSRF header was being attached twice — once by the plugin, as PageMotor 0.10 required for raw requests, and once by 0.11's new automatic attachment — and because attaching appends rather than overwrites, the token went out doubled and never matched. The plugin now attaches it only when the core has not already done so.
