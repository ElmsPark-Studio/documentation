---
title: "EP Ecommerce PayPal"
description: PayPal payment provider for EP Ecommerce. Orders API v2, client-side approve via PayPal Buttons, webhook verification, sandbox and live modes.
sidebar:
  order: 21
---

EP Ecommerce PayPal handles PayPal payments for [EP Ecommerce](/plugins/ep-ecommerce/) using the PayPal REST API v2 (Orders). Implements the standard server-create, client-approve, server-capture flow, with OAuth2 access token management, webhook verification, and optional PayPal Subscriptions for recurring billing.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **PayPal Orders API v2** with a proper server-side create and capture, not the legacy Express Checkout.
- **PayPal JS SDK buttons** on the frontend with configurable colour and shape.
- **Sandbox and live credential pairs** with mode switching.
- **OAuth2 access token** managed internally with request-level caching.
- **Webhook verification** via PayPal's `verify-webhook-signature` API.
- **Admin refunds** via the Captures API.
- **Coexists with EP Ecommerce Stripe** — both render into the same payment slot, so customers can pick their preferred method.
- **PayPal Subscriptions** support when EP Ecommerce Subscriptions is active.

## Requirements

- **PageMotor 0.7 or later**
- **EP Ecommerce** (base plugin)
- **EP Suite base class**
- **EP Ecommerce Products** for the checkout UI
- **A PayPal Developer account** with REST API credentials
- **EP Ecommerce Subscriptions** (optional, for recurring billing via PayPal)

## Setting up PayPal

### Step 1 — Create the PayPal app

1. Log in to the [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/).
2. Under **Apps & Credentials**, click **Create App**.
3. Name it (e.g. "PageMotor ecommerce"), pick **Merchant**, click **Create App**.
4. Copy the **Client ID** and **Secret** for both the **Sandbox** and **Live** environments.

### Step 2 — Configure the plugin

Open **Plugin Settings → EP Ecommerce PayPal**.

- **Enable PayPal payments.** Toggle on.
- **Mode.** Sandbox for testing, Live for production.
- **Sandbox credentials.** Client ID and secret.
- **Live credentials.** Client ID and secret for production.

### Step 3 — Set up the webhook

1. Back in the PayPal Developer Dashboard, open your app.
2. Scroll to **Webhooks**, click **Add Webhook**.
3. Webhook URL: copy from the plugin settings page (displayed in the **Webhook** section).
4. Event types to subscribe to:
   - `PAYMENT.CAPTURE.COMPLETED`
   - `PAYMENT.CAPTURE.DENIED`
   - If using subscriptions, also: `BILLING.SUBSCRIPTION.ACTIVATED`, `BILLING.SUBSCRIPTION.CANCELLED`, `BILLING.SUBSCRIPTION.EXPIRED`, `PAYMENT.SALE.COMPLETED`.
5. Save. Copy the generated **Webhook ID**.
6. Paste the Webhook ID into the plugin's **Webhook ID** setting for signature verification.

## How the payment flow works

1. Customer clicks the PayPal button on your site.
2. Plugin exchanges Client ID + Secret for an OAuth2 access token (cached per request).
3. Plugin creates a PayPal **Order** with the product amount and purchase details.
4. PayPal JS SDK renders the button, customer approves in a PayPal popup.
5. Frontend receives the approved order ID, sends it to the plugin's capture endpoint.
6. Plugin calls PayPal's Capture API to finalise the payment.
7. PayPal fires `PAYMENT.CAPTURE.COMPLETED` to your webhook.
8. Plugin verifies the webhook signature, marks the order paid, triggers fulfilment.
9. Customer sees success message, receives EP Email confirmation.

## Subscription flow (with EP Ecommerce Subscriptions)

When subscription products are purchased via PayPal:

1. Plugin creates a PayPal **Subscription** object via the Subscriptions API.
2. Customer approves the subscription in PayPal's popup.
3. PayPal fires `BILLING.SUBSCRIPTION.ACTIVATED` — plugin grants initial access.
4. On each renewal, PayPal fires `PAYMENT.SALE.COMPLETED` — plugin extends access.
5. On cancel or expire, PayPal fires `BILLING.SUBSCRIPTION.CANCELLED` or `BILLING.SUBSCRIPTION.EXPIRED` — plugin revokes access according to your cancellation-policy setting.

## Refunds

From the EP Ecommerce orders list, any paid PayPal order has a **Refund** button:

- **Full refund.** Refunds the entire capture.
- **Partial refund.** Enter an amount.
- Refund is submitted to PayPal's Captures API. Status updates when PayPal confirms.
- As with Stripe, fulfilment reversal is business-rule dependent and not automatic.

## Coexistence with Stripe

Both payment providers render into the same `.ep-ecommerce-payment-slot` div in the checkout. If both are active, the customer sees both options and picks their preferred method. Each provider independently tracks its own orders, so there's no cross-contamination.

## Payment description

What appears on the customer's PayPal account as the purchase description. Defaults to the product name; supports `{product_name}` placeholder. PayPal has no strict length limit like Stripe, but keep it readable.

## Troubleshooting

### "PayPal buttons don't appear on the checkout"

Check the browser console. Common causes:

- Client ID is wrong or empty.
- Mode is set to Live but you're using sandbox credentials, or vice versa.
- PayPal JS SDK is being blocked by an ad-blocker or CSP header. Loosen CSP if needed.

### "Webhook signature verification fails"

The Webhook ID saved in the plugin doesn't match the one in PayPal. Rotate in PayPal, paste the new ID, try again.

### "Sandbox works, Live fails with authentication error"

Live credentials must come from the live side of your PayPal app (same dashboard, different toggle). Mixing sandbox Client ID with live Secret is a common trip-up.

### "Orders stay in Pending forever"

The webhook isn't reaching your site, or is being rejected. Check PayPal Developer Dashboard → Webhooks → your webhook → event history. Failed deliveries show status codes. Common causes: firewall blocking PayPal IPs, HTTPS certificate issues, wrong URL path.

### "I get a refund error 'Capture not found'"

The payment was authorised but not captured, or was captured through a different flow (direct Express Checkout instead of Orders API). These cases happen on very old orders. Refund through PayPal directly.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
