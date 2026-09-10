---
title: "EP Class Passes"
description: "Pre-paid class credit packs for a studio. Credits tracked in an append-only ledger, with shelf-life expiry, auto-deduct at booking, and reinstatement on an in-policy cancel."
---

EP Class Passes adds pre-paid class credit packs to a studio, the classic 10-class pass. A pass is sold as an EP Ecommerce product, and its credits are tracked in an append-only ledger so the balance is always a sum, never a stored number that can drift.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Sold as a product.** A class pass is a new EP Ecommerce product type. Buying it issues a pass to the customer.
- **Append-only ledger.** Every change (purchase, redeem, reinstate, forfeit, expire, refund, admin adjust) is a ledger row. The balance is always computed.
- **Shelf-life expiry.** Passes can expire a fixed number of days from purchase, or from first use.
- **Eligibility.** A pass can be limited to specific class types.
- **Auto-deduct at booking.** When a member books a single class at the EP Events register, one credit is deducted automatically and the card is skipped entirely.
- **Fair cancellation.** An in-policy cancel reinstates the credit; a late cancel or no-show forfeits it.
- **Owner tools.** A member balance and history view, admin comp-grant and adjust, and a nightly expiry sweep with nudges.

## Requirements

- **PageMotor 0.8.3b or later**
- **EP Ecommerce 0.1.25 or later**
- **EP Events** for the booking auto-deduct

## Installation

1. `ep-class-passes.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
2. Upload via **Plugins → Manage Plugins**. Activate.
3. Create a class-pass product in EP Ecommerce, set its credits, validity and eligible class types, and sell it like any other product.

## Changelog

### 1.2.12

- **Corrects the PageMotor 0.11.3 preparation shipped in 1.2.11.** That release grouped this plugin's API and MCP actions into families, but in a shape PageMotor 0.11.3 does not accept. On 0.11.3 the plugin would have registered none of its actions, and nothing on screen would have said so.
- This version uses the shape 0.11.3 expects, and keeps the earlier shape for sites still on an older PageMotor. One build serves both, so there is no order you have to update things in.
- Safe to install now. Nothing you can see changes.

### Fixed

- **"on first use" was shown for passes that never start a clock.** A `from_first_use` pass with no day limit (`valid_days = 0`) never starts an expiry clock (the clock is only stamped on first redemption when `valid_days > 0`), so "on first use" implied a countdown that will never happen. Both the admin member table and the member-facing balance card now read **"never expires"** for any pass with no day limit (covers `from_first_use` and `from_purchase` with `valid_days = 0`). Passes that genuinely start a clock on first use still read "on first use" / "clock starts on first class".

### Fixed

- **Version badge missing from the admin header.** Two causes, both fixed: the plugin never defined its `EP_CLASS_PASSES` root constant (so `ep_version()` could not locate the plugin file), and the header `Version:` line sat past byte 500 behind a very long `Description:` line, beyond the window `ep_version()` reads. The constant is now defined and the header fields are reordered so `Version:` comes first.
- **No way to set up the nightly expiry cron.** `maybe_handle_cron()` read a `cron_secret` setting that the admin page never exposed, so there was nothing to set. A new "Nightly maintenance" section now generates the secret automatically and shows the ready-to-use daily cron URL (with an example crontab line), plus a "Run expiry sweep now" button for manual runs. Nothing to set or save.
- **Admin buttons could submit PageMotor's settings form.** The comp-grant and per-pass +/- buttons had no `type` attribute, so they defaulted to `type="submit"`; a click before the async admin JS attached its handler could submit the whole settings form ("Settings NOT saved!"). All admin buttons are now `type="button"`.
### 1.2.1

`member_pass_history` now surfaces as a native MCP tool, so an LLM connected to the site lists it directly.

### 1.2.0

Member balance and history surface, the booking pre-payment hook for auto-deduct and reinstatement, and read-only API actions for an LLM.
