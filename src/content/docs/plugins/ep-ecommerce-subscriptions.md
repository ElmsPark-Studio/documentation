---
title: "EP Ecommerce Subscriptions"
description: "Recurring billing for EP Ecommerce. Provider-agnostic subscription lifecycle, automatic membership grants, UK/EU compliance, dunning and grace periods, self-service portal."
sidebar:
  order: 22
---

EP Ecommerce Subscriptions adds recurring billing to [EP Ecommerce](/plugins/ep-ecommerce/). Works with Stripe and PayPal as payment providers, handles the full subscription lifecycle from activation through renewal, cancellation, and expiration, and automatically grants and revokes membership access as payments succeed or fail.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Features at a glance:

- **Provider-agnostic subscriptions table** with billing cycle tracking.
- **Stripe integration** creates Stripe Subscriptions (not one-off PaymentIntents) with proper Customer creation and lookup.
- **Stripe webhook handling** for `invoice.paid`, `invoice.payment_failed`, `customer.subscription.deleted`, `customer.subscription.updated`.
- **PayPal integration** with server-driven subscription create and webhook handlers for activation, cancellation, and renewal.
- **Automatic membership grants** on subscription activation.
- **Automatic revocation** on cancellation or expiration (per your cancellation-policy setting).
- **Cancellation policy**: end-of-period (access remains until paid-through date) or immediate (access revoked on cancel).
- **Dunning and grace periods** for failed payments: 0, 3, 7, or 14 days before access is revoked.
- **UK/EU compliance**: VAT display (inclusive or exclusive), cancellation rights notice, 14-day cooling-off period text.
- **GDPR consent text** on checkout (integrates with EP GDPR for consent logging).
- **Newsletter opt-in** on subscription checkout (integrates with EP Newsletter).
- **EP Affiliate recurring commissions** on every renewal.
- **Auth-gated self-service** via EP Passkeys.

## The subscription lifecycle

1. **Checkout.** Customer picks a subscription product, enters card details, approves any GDPR consent or newsletter opt-in.
2. **Activation.** Payment provider creates a subscription. The plugin stores a row with status = Active, billing cycle, and next renewal date.
3. **Access granted.** A membership is created on the EP Ecommerce base (or equivalent), giving the customer access to gated content.
4. **Renewals.** On every billing cycle, the provider charges. If successful, the plugin extends the membership paid-through date.
5. **Failed payments.** If a renewal fails, the plugin enters **dunning**. The customer gets an email to update their payment method. During the grace period, access remains.
6. **Grace expires.** If dunning doesn't resolve within the grace period, access is revoked.
7. **Cancellation.** Customer or admin cancels. Per your policy, access ends at the end of the current paid period (default) or immediately.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Ecommerce** (base plugin)
- **EP Suite base class**
- **EP Ecommerce Stripe** (for Stripe subscription processing)
- **EP Ecommerce PayPal** (optional, for PayPal subscriptions)

Optional but commonly paired:

- **EP Email** for lifecycle emails (activation, renewal receipt, dunning, cancellation confirmation, expiration).
- **EP GDPR** for consent logging.
- **EP Newsletter** for opt-in at checkout.
- **EP Passkeys** for auth-gated self-service.
- **EP Affiliate** for recurring commissions.

## Installation

1. Install EP Ecommerce, EP Ecommerce Products, and at least one payment extension (Stripe and/or PayPal).
2. Download `ep-ecommerce-subscriptions.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

## Creating a subscription product

1. Open **Plugin Settings → EP Ecommerce → Products**.
2. Click **Add Product** and pick **Subscription** as the type.
3. Fill in name, price, billing interval (monthly / yearly / custom).
4. Set the membership level this subscription grants.
5. Save.

On the product's checkout page, EP Ecommerce Products renders the checkout with the price, billing cycle, and cancellation rights notice. The customer can pay with any active provider.

## Cancellation policies

Two options, set globally in settings:

- **End-of-period.** Customer keeps access until the paid-through date, then loses access. Default, and what most users expect.
- **Immediate.** Access ends the moment cancel is clicked. Customer does not get a refund for unused time.

Set this based on your business model and pick the one your terms of service describe.

## Dunning

When a renewal payment fails:

1. Provider fires the failure webhook (`invoice.payment_failed` for Stripe, similar for PayPal).
2. Plugin marks the subscription as **past due** and the grace period begins.
3. EP Email sends the dunning email with a link to the self-service portal to update payment.
4. Provider retries according to its own dunning schedule (Stripe and PayPal both auto-retry).
5. If payment succeeds, subscription returns to Active, grace period ends.
6. If grace period expires without a successful retry, subscription moves to Unpaid, access is revoked.

Grace period is configurable: 0 (no grace, immediate revoke), 3, 7, or 14 days.

## Self-service shortcodes

Place on the customer's account page:

| Shortcode | Purpose |
|---|---|
| `[ep-my-subscriptions]` | Lists the current user's active subscriptions with cancel buttons and renewal dates. |
| `[ep-my-orders]` | Full order history, including subscription payments. |
| `[ep-my-downloads]` | Links to digital downloads the user has purchased. |

For auth, install **EP Passkeys** and gate the page. The shortcodes identify the current user from the authenticated session.

## UK/EU compliance

The plugin adds compliance boilerplate to checkout:

- **VAT display** inclusive or exclusive based on settings and customer country.
- **Cancellation rights notice** — the statutory text about the 14-day cooling-off period for digital services (with an opt-out if the customer consents to immediate delivery).
- **Consent-to-immediate-delivery checkbox** waiving the cooling-off period, required for digital products delivered instantly.

These comply with the UK Consumer Rights Act and EU Consumer Rights Directive defaults. Adjust language per your own terms if your product falls under a different regime.

## Integrations in detail

- **EP Affiliate** fires a commission event on every renewal, not just the first sale. If configured, affiliates earn recurring revenue.
- **EP GDPR** receives consent data on subscription signup, stored in EP GDPR's consent log.
- **EP Newsletter** can add an opt-in checkbox to the checkout; customers who tick are auto-added to the selected list.
- **EP Passkeys** gates the self-service shortcodes. Without Passkeys (or equivalent auth), the shortcodes show a login prompt.

## Troubleshooting

### "Subscription activated but access wasn't granted"

Check the membership-level mapping on the product. If the product doesn't map to a membership level, the plugin doesn't know what to grant.

### "Cancelled subscriptions still have access"

Cancellation policy is probably End-of-period. Access stays until paid-through. If you want Immediate, change the policy setting.

### "Failed payments aren't triggering dunning emails"

Check EP Email is installed, configured, and queuing emails correctly. Also check the webhook is being received — if the provider can't notify you of the failure, the plugin never knows.

### "Customer paid via PayPal and never activated"

Check PayPal webhook is receiving events. `BILLING.SUBSCRIPTION.ACTIVATED` is the one that flips the subscription to Active. Event history is in the PayPal Developer Dashboard.

### "I want to extend a subscription by N days manually"

Edit the subscription row's paid-through date via SQL, or through EP Assistant with a prompt like "extend subscription ID 42 by 30 days". No built-in admin UI for this yet.

### "Affiliate didn't get credit for the renewal"

EP Affiliate's recurring commission setting must be enabled. If it's off, only first-time conversions trigger commissions.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
