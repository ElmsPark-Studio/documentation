---
title: "EP Ecommerce"
description: "Information product ecommerce for PageMotor. Memberships, digital downloads, license keys, and subscriptions, with Stripe and PayPal via separate extensions."
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

The plugin's own gate, `[ep-membership-content]`, is an **exact match** on the level. A buyer of a product whose level is `course-a` passes the `course-a` gate and no other. There is no ranking between levels here; ranking is [EP Membership](/plugins/ep-membership/)'s job, and only its gates use it. That makes one-off products (a single course, a single download bundle with ongoing access) simple: give each product its own level slug and wrap each product's content in its own gate.

Two things happen around a level since 0.1.40:

- **Every active grant is also a permission key** on the buyer's PageMotor account, named `EP_Ecommerce.grant.<level>`, one per product, flat, no ranking. Revoking or expiring the membership removes the key. No gate consumes these keys yet, so nothing changes on a site today; they exist so a page-level exact-match gate can be built without a schema change.
- **Saving a product warns** when its membership level is not one that EP Membership defines. The save still succeeds, because that level is perfectly valid for the exact-match gate above. The warning tells you that EP Membership's ladder will ignore it.

Memberships past their expiry date are marked expired once a day, from an admin page load. Access already lapsed on the date regardless; this keeps the stored status honest and lets extensions hear about it.

### Buyer accounts (0.1.37)

A membership or subscription is gated on being signed in, so a buyer without a PageMotor account could pay, receive a valid grant, and then be told to log in to an account that never existed. Since 0.1.37 the plugin creates the account itself.

When a membership is granted to an email address that has no account:

1. A PageMotor user is created for it, of the type set in **Buyer Account Type** (default `learner`, which is what EP Membership's own registration form creates, so buyers appear in its member list).
2. The buyer is emailed a single-use link to the **Set Password** page. The link lives for 7 days.
3. Setting a password signs them in and sends them to the **After Setup** address, or to the login page if that is blank.

The Set Password page is created for you the first time it is needed, at the path in **Set Password Page** (default `set-password`), carrying the `[ep-set-password]` shortcode. If a page at that path already exists it is left alone.

An email that already owns an account is a no-op: renewals, webhook retries and repeat purchases never create a second account or resend the welcome email. With EP Membership active, the new account is marked email-verified, because the address has already proved itself by paying and by receiving the link.

Downloads and licence keys are unchanged. They are delivered by email and need no login, so no account is created for them.

The switch is **Settings → Membership → Buyer Accounts**: create automatically (the default) or do not create.

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
| `[ep-set-password]` | The form a new buyer lands on from their welcome email (0.1.37). Placed for you on the Set Password page; only needed by hand if you move that page. |

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Suite base class**
- **EP Ecommerce Products** for the checkout UI.
- **At least one payment extension**: EP Ecommerce Stripe or EP Ecommerce PayPal (or both).

## Installation

1. `ep-ecommerce.zip` comes with an EP Suite licence — ElmsPark supplies it directly (see [EP Suite plugins](https://elmspark.com/suite/)); after install it updates through your site's **Updates** screen.
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

## Managing products over the API and MCP (0.1.38)

Products can be listed, created, updated and deleted through PageMotor's API and through an MCP connection, using the same validation as the admin screen. All four actions require admin access.

| Action | What it does |
|---|---|
| `list-product` | Every product, with its type-specific fields. |
| `create-product` | Create one. Same required fields and type rules as the admin form. |
| `update-product` | Change any fields on an existing product. |
| `delete-product` | Remove one. |

A slug you supply by hand is normalised the same way the admin screen normalises a typed name, so `My Slug` is stored as `my-slug`. Create and update return the same level warning described under Memberships when a membership level is not one EP Membership defines.

## Database tables

- `{prefix}ep_ecommerce_products` — product catalogue.
- `{prefix}ep_ecommerce_orders` — every purchase.
- `{prefix}ep_ecommerce_memberships` — active membership records.
- `{prefix}ep_ecommerce_licenses` — license keys with validation records.
- `{prefix}ep_ecommerce_downloads` — download tokens.
- `{prefix}ep_ecommerce_account_tokens` holds the single-use set-password links for new buyer accounts (0.1.37).

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
| `on_membership_revoked($user_email, $product_id, $order_id, $level, $reason)` | React to a grant going away (0.1.40). Fires once per revocation, with `$reason` of `revoked`, `expired`, or whatever the caller passed (a refund passes `refund`). |
| `filter_license_validation($license, $response)` | Modify license API responses. |
| `settings_fields()` | Add settings to the EP Ecommerce settings page. |

Same pattern as `EP_Email_Extension`. See the Stripe and PayPal extensions for reference implementations.

## Troubleshooting

### “Checkout renders but no payment buttons appear”

You need at least one payment extension installed and configured. Install EP Ecommerce Stripe or EP Ecommerce PayPal, paste API keys on their settings page, and the buttons render.

### “Orders appear as Paid but no membership / download was granted”

Check the payment extension's webhook is configured correctly and reaching your site. Stripe / PayPal push async notifications; without webhooks, orders show as paid from the frontend flow but fulfilment doesn't fire.

### “Download URLs expire too quickly”

Configure per-product download token lifetime and max download count in the product's admin. Default is usually 24 hours and 3 downloads, which is deliberately conservative.

### “A buyer paid for a membership but is told to log in”

Before 0.1.37 no account was created for a buyer, so this was every first-time buyer's experience. Update, then check **Settings → Membership → Buyer Accounts** is set to create automatically. For a buyer who paid before the update, create their account from EP Membership's Members panel or ask them to register with the same email address they paid with; the grant is keyed on that address and attaches on login.

### “The welcome email's set-password link gives a 404”

The Set Password page is created on first use since 0.1.39. On a site that installed 0.1.37 or 0.1.38 and never opened the settings, create a page at the path in **Set Password Page** carrying `[ep-set-password]`, or update and let the next purchase create it.

### “License keys I generate aren't validating”

Validation requires the software to call your site's license API with the key. If the software isn't coded to check, keys are cosmetic. This is about what the customer-facing software expects.

### “I want to sell a custom product type that isn't one of the five”

Build a small EP Suite plugin that extends `EP_Ecommerce_Extension` and implements `product_types()` and `render_product_admin()`. Ask on the support forum for the current reference signatures.

## Changelog

### 0.1.42

- **Corrects the PageMotor 0.11.3 preparation shipped in 0.1.41.** That release grouped this plugin's API and MCP actions into families, but in a shape PageMotor 0.11.3 does not accept. On 0.11.3 the plugin would have registered none of its actions, and nothing on screen would have said so.
- This version uses the shape 0.11.3 expects, and keeps the earlier shape for sites still on an older PageMotor. One build serves both, so there is no order you have to update things in.
- Safe to install now. Nothing you can see changes.

### 0.1.41

- **Prepares the plugin for PageMotor 0.11.3, which requires every plugin to group its API and MCP actions into named families.** On that release an action declaring no family is refused silently, so without this update the plugin's actions would stop being offered with nothing on screen to say why.
- Families exist so that an AI working on your site sees the related actions together instead of stopping at the first one it tries.
- Safe to install on your current PageMotor. No behaviour changed.

### 0.1.40

7 September 2026. Every active grant becomes a flat `EP_Ecommerce.grant.<level>` permission key on the buyer's account. Saving a product warns when its membership level is not one EP Membership defines. Extensions hear about revocations through `on_membership_revoked()`, and expired memberships are now marked expired daily rather than only lapsing.

### 0.1.39

2 September 2026. The Set Password page is created on first use, so the welcome email never points at a missing page. Buyer emails are lowercased at the boundary. A buyer who registered before purchasing and never verified gets the verified flag on purchase.

### 0.1.38

1 September 2026. Products can be managed over the API and MCP, through the same validation as the admin screen. Hand-typed slugs are normalised.

### 0.1.37

1 September 2026. Buyer accounts: a membership or subscription purchase creates a PageMotor account for the buyer and emails a single-use set-password link. Settings under Membership control it.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
