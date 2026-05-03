---
title: "EP Ecommerce Stripe"
description: "Stripe payment provider for EP Ecommerce. Full PaymentIntent lifecycle, webhook verification, admin refunds, test/live mode switching."
sidebar:
  order: 20
---

EP Ecommerce Stripe handles Stripe payments for [EP Ecommerce](/plugins/ep-ecommerce/). It uses raw cURL against the Stripe API, so no Composer dependencies, and implements the full payment lifecycle: PaymentIntent creation with idempotency keys, webhook signature verification, payment confirmation fallback for delayed webhooks, and admin-initiated refunds.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **PaymentIntents, not Charges.** The modern Stripe approach, compatible with SCA and 3D Secure out of the box.
- **Stripe Payment Element** on the frontend (Stripe.js v3) with the default styled UI.
- **Webhook-driven fulfilment** with HMAC-SHA256 signature verification (timing-safe) for `payment_intent.succeeded` and `payment_intent.payment_failed`.
- **Confirmation fallback** for cases where the webhook is delayed — prevents a visible "waiting" state for the customer.
- **Atomic order claiming** so a webhook and a confirmation cannot double-fulfil.
- **Admin refunds** from the orders list via the Stripe Refunds API.
- **Zero-decimal currency handling** (JPY, KRW, etc. — no implicit cents).
- **Idempotency keys** on every request so network retries never double-charge.
- **Customisable statement descriptor** with `{product_name}` placeholder for bank statement clarity.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Ecommerce** (base plugin)
- **EP Suite base class**
- **EP Ecommerce Products** for the checkout UI
- **A Stripe account** with API keys

## Installation

1. Install **EP Ecommerce** and **EP Ecommerce Products** first.
2. Download `ep-ecommerce-stripe.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

## Setting up Stripe

### Step 1 — Get your API keys

1. Log in to your [Stripe dashboard](https://dashboard.stripe.com/).
2. Under **Developers → API keys**, copy your **publishable key** and **secret key**.
3. Stripe gives you two sets: one for test mode (prefixed `pk_test_` / `sk_test_`) and one for live mode (`pk_live_` / `sk_live_`).

### Step 2 — Configure the plugin

Open **Plugin Settings → EP Ecommerce Stripe**.

- **Enable Stripe payments.** Toggle on.
- **Mode.** Test (for development) or Live (for production).
- **Test API keys.** Paste both.
- **Live API keys.** Paste both when ready to go live.

### Step 3 — Set up the webhook

Stripe pushes payment status to your server via a webhook. Without it, orders can stall.

1. In your Stripe dashboard, go to **Developers → Webhooks**.
2. Click **Add endpoint**.
3. Endpoint URL: `https://yoursite.com/?ep_ecommerce_stripe_webhook=1`
4. Events to send:
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Click **Add endpoint**.
6. On the endpoint detail page, reveal the **Signing secret** (starts `whsec_`).
7. Back in the plugin settings, paste it into **Webhook signing secret**.

Test the webhook from Stripe's dashboard by sending a test event.

## How the payment flow works

1. Customer clicks the checkout button on your site.
2. Plugin creates a Stripe **Customer** (or looks up an existing one by email).
3. Plugin creates a **PaymentIntent** for the product amount with idempotency key.
4. Frontend renders the **Payment Element** from Stripe.js using the PaymentIntent's client secret.
5. Customer enters card details. Stripe handles 3D Secure if required.
6. On success, Stripe fires `payment_intent.succeeded` to your webhook.
7. Plugin atomically claims the order, marks it paid, triggers fulfilment (grant membership, generate license, etc.).
8. As a fallback, the frontend also calls a confirmation endpoint — if the webhook is delayed, the confirmation completes the flow.
9. Customer sees success message, receives EP Email confirmation.

## Refunds

From the EP Ecommerce orders list, any paid Stripe order has a **Refund** button:

- **Full refund.** Refunds the entire charge.
- **Partial refund.** Enter an amount less than or equal to the charge.
- The order status updates to Refunded / Partially Refunded.
- Fulfilment reversal (revoking memberships, voiding licenses) is on you, because business rules vary — by default the refund only handles the money.

## Statement descriptor

What appears on the customer's bank statement. Defaults to your business name (as configured in Stripe), but can be overridden per-product:

- `{product_name}` is substituted with the actual product name at charge time.
- Stripe limits descriptors to 22 characters. Anything longer gets truncated.

## Security

- **Webhook verification** uses Stripe's timing-safe HMAC comparison, so a timing-attack cannot reveal your signing secret.
- **CSRF verification** on frontend AJAX requests.
- **IDOR protection** on the confirmation endpoint — customer A cannot confirm customer B's order.
- **Keys never in the database unencrypted.** Secret keys are stored as settings, admin-only readable.

## Troubleshooting

### "Webhook signature verification fails"

The webhook signing secret you pasted doesn't match the one in your Stripe dashboard. Rotate the secret in Stripe, paste the new one, test again.

### "Orders are showing as Paid but memberships aren't being granted"

Fulfilment happens after webhook verification. If webhook verification passed but fulfilment didn't, check error logs — commonly a database constraint error or a missing product reference. Paste the order ID into the review queue.

### "Test mode works, live mode fails"

Live-mode keys must be from the same Stripe account as your test keys. Mixing up accounts is a common cause. Also check that live mode is enabled in your Stripe account (some new accounts start with a hold).

### "The Payment Element shows an error about invalid publishable key"

The publishable key in the settings doesn't match the mode. If mode is Live but you pasted a test key, Stripe rejects. Check the prefix: `pk_live_` for live, `pk_test_` for test.

### "Customers complain about 3D Secure prompts"

3DS is triggered by Stripe based on risk and issuer rules. The Payment Element handles it automatically. If customers can't complete 3DS, it's usually their issuer or a network issue, not your site.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
