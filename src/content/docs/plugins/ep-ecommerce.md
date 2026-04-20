---
title: "EP Ecommerce"
description: "Information product ecommerce for PageMotor. Memberships, digital downloads, license keys, and subscriptions, with Stripe and PayPal via separate extensions."
sidebar:
  order: 18
---

EP Ecommerce is the base plugin in a five-plugin family for selling information products from your PageMotor site. Memberships, digital downloads, license keys, bundles, and subscriptions. Payment providers (Stripe, PayPal) and checkout styling ship as separate extension plugins that hook into the same core.

Published by [ElmsPark Studio](https://elmspark.com).

## The ecommerce family

EP Ecommerce is built as a base plus four extensions. Install only the ones you need:

| Plugin | Role | Required? |
|---|---|---|
| **EP Ecommerce** | Base. Product CRUD, orders, memberships, license keys, download tokens. | Yes |
| **EP Ecommerce Products** | Styled checkout UI. | Yes, for visible checkout |
| **EP Ecommerce Stripe** | Stripe payment provider. | Only if using Stripe |
| **EP Ecommerce PayPal** | PayPal payment provider. | Only if using PayPal |
| **EP Ecommerce Subscriptions** | Recurring billing. | Only if selling subscriptions |

Each extension is documented separately. This page covers the base.

## What EP Ecommerce does

### Five product types

| Type | What it is |
|---|---|
| **Membership** | Grants ongoing access to gated content. |
| **Download** | Time-limited secure URL to a file (PDF, ZIP, MP3). |
| **License** | Generates a unique license key the customer can use to activate software. |
| **Bundle** | Combines multiple products into one purchase. |
| **Subscription** | Recurring billing. Requires EP Ecommerce Subscriptions. |

### Orders

Every purchase creates an order row. Orders track status (Pending / Paid / Failed / Refunded), customer details, and which product(s) were purchased.

### Memberships

Membership products grant access for a fixed period or forever. Access checks are plugin-level so any plugin (like EP Membership) can ask "does this email have active access to membership level X".

### License keys

Three generation formats:

- **UUID** — `f47ac10b-58cc-4372-a567-0e02b2c3d479`.
- **Segmented** — `ABCD-EFGH-IJKL-MNOP`.
- **Alphanumeric** — `A3F9X7Q2K8L1V6N4`.

Licenses can have expiry dates, activation limits, and be validated via a simple API for software to phone home and check.

### Secure downloads

For Download products, the customer gets a time-limited tokenised URL in their confirmation email. Tokens expire after a configurable window and honour a maximum download count, so a leaked URL can't be mass-abused.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[ep-checkout product=my-product]` | Checkout form for a specific product. |
| `[ep-membership-content level=premium]...content...[/ep-membership-content]` | Gate content to members of a given level. Non-members see nothing (or a custom message). |
| `[ep-download product=my-download]` | Download button, checks the current user's purchase history and redirects to a valid secure URL. |

## Requirements

- **PageMotor 0.7b or later**
- **EP Suite base class**
- **EP Ecommerce Products** for the checkout UI.
- **At least one payment extension**: EP Ecommerce Stripe or EP Ecommerce PayPal (or both).

## Installation

1. Download `ep-ecommerce.zip` plus the extensions you need from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
2. Upload and activate **EP Ecommerce** first.
3. Upload and activate **EP Ecommerce Products**.
4. Upload and activate your payment provider(s): **EP Ecommerce Stripe** and/or **EP Ecommerce PayPal**.
5. If selling subscriptions, also install **EP Ecommerce Subscriptions**.
6. Database tables are created automatically on first load.

## Setting up your first product

1. Open **Plugin Settings → EP Ecommerce → Products**.
2. Click **Add Product**.
3. Pick a product type (membership, download, license, bundle, subscription).
4. Fill in name, description, price, status.
5. Type-specific fields appear:
   - **Membership:** access level, duration.
   - **Download:** file URL, max downloads, link expiry.
   - **License:** format, expiry, activation limit.
6. Save.
7. Add `[ep-checkout product=my-product-slug]` to a page.

The payment buttons render inside the `.ep-ecommerce-payment-slot` div in the checkout. Whichever payment extensions are active fill the slot with their buttons.

## Database tables

- `{prefix}ep_ecommerce_products` — product catalogue.
- `{prefix}ep_ecommerce_orders` — every purchase.
- `{prefix}ep_ecommerce_memberships` — active membership records.
- `{prefix}ep_ecommerce_licenses` — license keys with validation records.
- `{prefix}ep_ecommerce_downloads` — download tokens.

## Extension API

Plugins extend EP Ecommerce by subclassing `EP_Ecommerce_Extension` and registering themselves. Available hooks:

| Hook | Purpose |
|---|---|
| `checkout_head($product)` | Inject scripts or config before the checkout form. |
| `render_checkout($product)` | Provide custom checkout HTML. |
| `process_payment($product, $data)` | Handle the actual payment. |
| `after_fulfillment($product, $order_id, $data)` | Post-purchase actions. |
| `product_types()` | Register a custom product type. |
| `render_product_admin($product)` | Admin fields for custom types. |
| `check_access($email, $level)` | Override membership access checks. |
| `on_membership_granted(...)` | React to membership grants. |
| `filter_license_validation($license, $response)` | Modify license API responses. |
| `settings_fields()` | Add settings to the EP Ecommerce settings page. |

Same pattern as `EP_Email_Extension`. See the Stripe and PayPal extensions for reference implementations.

## Troubleshooting

### "Checkout renders but no payment buttons appear"

You need at least one payment extension installed and configured. Install EP Ecommerce Stripe or EP Ecommerce PayPal, paste API keys on their settings page, and the buttons render.

### "Orders appear as Paid but no membership / download was granted"

Check the payment extension's webhook is configured correctly and reaching your site. Stripe / PayPal push async notifications; without webhooks, orders show as paid from the frontend flow but fulfilment doesn't fire.

### "Download URLs expire too quickly"

Configure per-product download token lifetime and max download count in the product's admin. Default is usually 24 hours and 3 downloads, which is deliberately conservative.

### "License keys I generate aren't validating"

Validation requires the software to call your site's license API with the key. If the software isn't coded to check, keys are cosmetic. This is about what the customer-facing software expects.

### "I want to sell a custom product type that isn't one of the five"

Build a small EP Suite plugin that extends `EP_Ecommerce_Extension` and implements `product_types()` and `render_product_admin()`. Ask on the support forum for the current reference signatures.

## Feedback and corrections

Open an issue at [the documentation repo](https://github.com/ElmsPark-Studio/documentation/issues).
