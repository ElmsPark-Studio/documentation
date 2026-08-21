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

### 0.1.2

Fixes "Your session has expired. Please reload to ensure your security." on PageMotor 0.11, which affected the discount codes panel in admin. The CSRF header was being attached twice — once by the plugin, as PageMotor 0.10 required for raw requests, and once by 0.11's new automatic attachment — and because attaching appends rather than overwrites, the token went out doubled and never matched. The plugin now attaches it only when the core has not already done so.
