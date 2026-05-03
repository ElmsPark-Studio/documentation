---
title: "EP Ecommerce Products"
description: "Styled checkout UI for EP Ecommerce. Three layout options (card, inline, modal), configurable price placement, purchase confirmation emails tailored to each product type."
sidebar:
  order: 19
---

EP Ecommerce Products is the checkout-UI layer of [EP Ecommerce](/plugins/ep-ecommerce/). The base plugin handles data and logic; this plugin handles what the customer sees. Install it alongside EP Ecommerce whenever you want a polished checkout form with a styled button, good price placement, and proper confirmation emails.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

Three checkout layouts:

- **Card** — the full product card with description, price, and buy button in a bordered container. Good for standalone checkout pages.
- **Inline** — buy button with price inline, no card. Good for inserting mid-content.
- **Modal** — clickable trigger that opens the checkout in a popup. Good for upgrade prompts or multiple products on the same page.

Plus:

- **Configurable success message** and optional **redirect URL** after a completed purchase.
- **Price position** control: above the button, inside the button, or below the title.
- **Type-aware confirmation emails** via EP Email: downloads get a secure time-limited link, memberships get access details, licenses get the generated key, subscriptions get billing schedule, and so on.
- **Secure time-limited download links** inside the download confirmation email.
- **Admin sale notifications** fired through EP Email.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Ecommerce** (base plugin, required)
- **EP Suite base class** (bundled)
- **EP Email** (for confirmation emails)

## Installation

1. Install **EP Ecommerce** first.
2. Download `ep-ecommerce-products.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.

Once installed, `[ep-checkout]` uses the styled layout instead of the bare base-plugin rendering.

## Settings

### Checkout

- **Form style.** Card / Inline / Modal.
- **Success message.** Shown on the page after a successful purchase. Default is generic; override to match your tone.
- **Success redirect URL.** Optional. If set, the browser jumps to this URL after purchase (good for a "thank you" page with upsells).

### Product Catalog

- **Show description on checkout.** Toggle the product description rendering.
- **Price position.** Above button, inside button, or below title.

## Confirmation emails

Per product type:

- **Download:** email with a tokenised secure URL to the file. Token expires per your EP Ecommerce settings.
- **Membership:** email with access details and a link to the gated content.
- **License:** email with the generated key and installation instructions if you've configured them.
- **Bundle:** email listing each component with its own download link or access details.
- **Subscription:** email with billing schedule, renewal date, and cancellation link. Requires EP Ecommerce Subscriptions.

Every email template uses EP Email's placeholder system, so you can customise copy and branding in one place.

## Troubleshooting

### "My checkout looks unstyled"

This plugin must be active. Check **Plugins → Manage Plugins** and confirm EP Ecommerce Products is on.

### "The modal layout doesn't open"

Modal requires JavaScript. Check your browser console for errors that might be breaking the bundle.

### "Confirmation emails show raw placeholders like {product_name}"

The email template is missing context. Check your EP Email template has the placeholders matched and that the fulfilment flow completed (not just the payment). Placeholders only substitute when the order has a known product attached.

### "Admin sale notifications aren't arriving"

Check the admin notification email address is set in EP Ecommerce base settings, and that EP Email's SMTP is working.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
