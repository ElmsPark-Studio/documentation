---
title: "EP Ecommerce — POD"
description: "Provider-agnostic print-on-demand for EP Ecommerce. Sell physical products on PageMotor: design at your provider, sync to your pages, take card payment with a live shipping quote, route paid orders for printing, and return tracking to the customer."
---

EP Ecommerce — POD is the **print-on-demand engine** for [EP Ecommerce](/plugins/ep-ecommerce/). It lets you sell physical products from your PageMotor site: apparel, mugs, prints, and so on. You design the products at a print-on-demand provider, sync them into PageMotor, and they sell as normal products with their own pages. When a customer pays, the order is routed to the provider for printing and shipping, and tracking is returned to the customer automatically.

The engine is **provider-agnostic**. It does not talk to any one print house directly; a small **connector** plugin supplies the account credentials and the API mapping for a given provider. [EP Ecommerce — Printify](/plugins/ep-ecommerce-printify/) is the first connector. Others can follow without changing the engine.

Published by [ElmsPark Studio](https://elmspark.com).

## The print-on-demand family

| Plugin | Role | Required? |
|---|---|---|
| **EP Ecommerce** | Base. Products, orders, fulfilment hooks. | Yes (0.1.22+) |
| **EP Ecommerce — POD** | This engine. Sync, storefront, checkout, routing, tracking. | Yes |
| **EP Ecommerce — Printify** | Printify connector (API token + Store ID). | One connector required |
| **EP Ecommerce — Stripe** | Card payment. | Yes |

This page covers the engine. The connector is documented separately.

## How it works

1. **Design at your provider.** Build your products in your print-on-demand account as usual (for example, in Printify).
2. **Sync.** In PageMotor, click **Sync products**. Each provider product is pulled in (enabled variants, retail price, mockup image) and becomes an EP Ecommerce product with its own checkout page.
3. **Customer buys.** On the product page the customer picks a variant (size / colour), enters their delivery address, and sees a **live shipping quote**. They pay by card through EP Ecommerce — Stripe; the chosen delivery cost is added to the total. If the provider's quote is slow or unavailable, the engine falls back to your configured flat rate so checkout never stalls.
4. **Order is routed.** The paid order is created at the provider as an **on-hold** order (no charge), carrying the variant and the full delivery address.
5. **Fulfilment.** You review and send the order to production from the provider's dashboard (or switch on auto-send). Tracking comes back automatically, and the customer is emailed their tracking link.

## Requirements

- **PageMotor 0.7 or later**
- **EP Ecommerce 0.1.22 or later** — adds the generic `pod` product type the engine uses. Older versions will reject the synced products.
- **A connector** — currently [EP Ecommerce — Printify](/plugins/ep-ecommerce-printify/). Without a connector the engine has no provider to talk to.
- **EP Ecommerce — Stripe** — for taking card payment.
- An **external cron service** (such as cron-job.org) to call the background-sync URL shown in settings. PageMotor has no scheduler of its own; the cron is what drives retries and tracking updates.

## Installation

Install in this order, activating each before the next:

1. **[EP Ecommerce](https://updates.elmspark.com/download.php?plugin=ep-ecommerce)** (0.1.22+).
2. **[EP Ecommerce — POD](https://updates.elmspark.com/download.php?plugin=ep-ecommerce-pod)** (this engine).
3. Your connector — **[EP Ecommerce — Printify](https://updates.elmspark.com/download.php?plugin=ep-ecommerce-printify)**.
4. **[EP Ecommerce — Stripe](https://updates.elmspark.com/download.php?plugin=ep-ecommerce-stripe)**.

Database tables are created automatically on first load.

## Setup

1. Connect your provider first. For Printify, open **EP Ecommerce — Printify**, paste your token, run **Test Connection**, and Save. (See the [connector page](/plugins/ep-ecommerce-printify/).)
2. Open **Plugin Settings → EP Ecommerce — POD**.
3. Under **Print-on-Demand**, tick **Enable print-on-demand**.
4. Under **Products**, click **Sync products**. Your products are imported and a checkout page is created for each one. Re-sync any time to pick up price, image, or availability changes.
5. Set your **Delivery pricing** fallback and your **Fulfilment** preference (below), and copy the **background-sync URL** into your external cron.

## Settings

| Setting | Section | What it does |
|---|---|---|
| **Enable print-on-demand** | Print-on-Demand | Master switch. Orders only route to the provider when this is on and a connector is connected. |
| **Sync products** | Products | Imports the connected provider's catalogue and creates a checkout page per product. |
| **Flat-rate fallback** | Delivery pricing | If on, and the live shipping quote is slow or unavailable, checkout uses your flat rate so it never stalls. |
| **Flat rate** | Delivery pricing | The fallback delivery cost in major units (for example, `4.99`). |
| **Flat-rate label** | Delivery pricing | The customer-facing name for the fallback method (defaults to "Standard delivery"). |
| **Auto-send paid orders to production** | Fulfilment | Off by default. When on, paid orders are sent to production automatically (this charges your provider balance). When off, orders are held for your review. |

## Fulfilment: on-hold vs auto-send

Every paid order is first created at the provider as **on hold**, which does not charge you. From there:

- **Hold for review (default).** Orders wait in your provider dashboard. You open each one and click **Send to production** when you are ready. Nothing is charged or printed until you do.
- **Auto-send to production.** Tick **Auto-send paid orders to production** under **Fulfilment** to have orders sent automatically once payment clears. This charges your provider balance and prints the item, so only switch it on when you are confident in your setup.

:::caution
Printify has no sandbox or test mode. The only way to test the final "send to production" step is to place one small real order, which prints a real item and charges your provider balance. The engine ships with auto-send **off** so nothing reaches production without your say-so. Place one real order yourself first to watch it go all the way through before switching auto-send on.
:::

## Background sync (retries and tracking)

PageMotor has no built-in scheduler, so the engine exposes a secret URL on its settings page of the form:

```
https://your-site.example/?ep_pod_cron=<secret>
```

Point a free cron service (cron-job.org, or your server's crontab) at this URL every 5 to 10 minutes. It:

- retries any order submissions to the provider that failed (with backoff), and
- polls the provider for order status and tracking, updating the order and emailing the customer their tracking link when the parcel ships.

Keep the URL private. Anyone with it can trigger background processing, though it cannot read or change your data.

## Shortcode

| Shortcode | Purpose |
|---|---|
| `[ep-checkout product=my-product-slug]` | The print-on-demand checkout for a synced product. A page with this shortcode is created automatically for each product on sync. |

## Database tables

- `{prefix}ep_pod_product_map` — synced provider products (variants, price, mockup, links to the EP product + page).
- `{prefix}ep_pod_order_map` — one row per order routed to the provider (provider order id, status, tracking, retry state).

No change is made to the core EP Ecommerce orders table; the variant and delivery address for an order are stored in the order's metadata.

## Troubleshooting

### "Data truncated for column 'type'" when I sync

Your EP Ecommerce is older than 0.1.22. Update **EP Ecommerce** to 0.1.22 or later, which adds the generic `pod` product type, then sync again.

### Nothing syncs

Check that a connector is installed and connected. For Printify, open **EP Ecommerce — Printify** and confirm **Test Connection** succeeds. Then, on this engine's page, make sure **Enable print-on-demand** is ticked before clicking **Sync products**.

### Orders are paid but nothing reaches the provider

Make sure **Enable print-on-demand** is ticked and that the connector's **Test Connection** succeeds. Orders only route when the engine is enabled and a connector is connected.

### Checkout hangs on the shipping step

The live shipping quote depends on the provider's API. Turn on **Flat-rate fallback** under **Delivery pricing** and set a flat rate; the engine then uses it whenever the live quote is slow or unavailable, so checkout never stalls.

### Tracking never updates / "your order has shipped" email never arrives

Tracking is pulled in by the background-sync cron. Make sure an external cron is calling the `?ep_pod_cron=` URL from the settings page every few minutes. Without it, statuses and tracking will not update on their own.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
