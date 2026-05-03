---
title: "EP Reviews"
description: "Product reviews for EP Ecommerce. Star ratings, verified-purchase badges, moderation, Schema.org Product + Review markup for rich search results."
sidebar:
  order: 45
---

EP Reviews adds product reviews to [EP Ecommerce](/plugins/ep-ecommerce/) products. Customers leave a star rating and written review, verified purchasers get a badge, admin moderates, and the structured data lets your products appear with star ratings in search results.

Published by [ElmsPark Studio](https://elmspark.com).

## Overview

- **Star ratings** (1-5) plus written review.
- **Verified purchase badge** auto-applied when the reviewer's email matches a completed order for the product.
- **Admin moderation** — new reviews queue for approval by default.
- **Response** — admin can post a public reply under any review.
- **Schema.org** `Review` and aggregate `AggregateRating` markup on product pages.
- **Vote helpfulness** — other visitors vote reviews up or down.
- **Sort and filter** — newest, highest-rated, lowest-rated, verified-only.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Ecommerce** (required — reviews attach to ecommerce products)
- **EP Suite base class**
- **EP Email** (for review notifications and reply alerts)

## Installation

1. Install **EP Ecommerce**.
2. Download `ep-reviews.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Add `[ep-reviews product=SLUG]` to any product page, or enable auto-injection in settings.

## Shortcodes

| Shortcode | Purpose |
|---|---|
| `[ep-reviews product=my-product]` | Full review section for the given product: aggregate rating, submission form, review list. |
| `[ep-reviews-summary product=my-product]` | Compact summary — star rating + review count. For use in product listings. |
| `[ep-reviews-form product=my-product]` | Submission form only. |

## Settings

- **Auto-inject** reviews into product pages (on by default).
- **Require approval** before reviews appear (on by default).
- **Verified purchase required** — lock reviews to verified buyers only (off by default, so everyone can review).
- **Minimum rating** before a review is flagged for extra attention (e.g. any 1-star triggers an alert to admin).
- **Helpful voting** — enable the up/down buttons under each review.
- **Review form fields** — star rating, review body, reviewer name, email.

## Verified purchase

When a review is submitted, the plugin checks the reviewer's email against orders for that product. If found, the review is tagged verified and displayed with a badge.

## Moderation

Queue of pending reviews visible in **Plugin Settings → EP Reviews → Pending**:

- Approve, reject, mark as spam.
- View reviewer history.
- Search by product, by rating, by text.

## Schema.org

When the `[ep-reviews]` shortcode renders, it emits:

- `AggregateRating` on the product page (e.g. "4.7 from 23 reviews").
- Individual `Review` schema for each approved review.

Google uses this to show star ratings in search results. Check in the [Google Rich Results Test](https://search.google.com/test/rich-results) after publishing a few reviews.

## Responding to reviews

Admin can click any review and post a public reply. Replies render inline under the review with an "Owner response" label. Good for thanking positive reviewers and addressing concerns in negative ones.

## Helpful voting

Under each review, thumbs-up / thumbs-down buttons. Visitors vote whether the review helped them. Aggregate counts display under the review. Cookies prevent repeat voting.

Reviews sortable by helpfulness, so the most-helpful bubbles to the top.

## Troubleshooting

### "Star rating doesn't appear in Google search results"

Rich result eligibility depends on meeting Google's criteria beyond just valid schema: at least 5 reviews, review body must be substantive, product needs to be a real e-commerce product. Schema being right is necessary but not sufficient.

### "Verified purchase badge isn't showing for genuine buyers"

The reviewer's email must match the email on their completed order exactly. If they used a different email to order vs review, no match. Consider requiring login-based reviews if this matters.

### "Reviews are being spammed"

Enable **Require approval**. Also enable the honeypot (already on by default). Consider **Verified purchase required** to block non-buyers entirely.

### "A 1-star review is unfair — can I delete it?"

You can, but think twice. Deleting legitimate negative reviews damages trust if customers notice. A public **Owner response** showing you addressed the concern is usually better PR.

### "Helpful vote count reset to 0"

Cookie-based voting means votes are tied to the visitor's browser. If cookies clear or the visitor switches browsers, they can vote again. Aggregate counts should be stable though.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
