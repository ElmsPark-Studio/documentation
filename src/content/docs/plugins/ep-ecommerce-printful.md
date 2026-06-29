---
title: "EP Ecommerce — Printful"
description: "The Printful connector for EP Ecommerce — POD. Adds your Printful account (API token + Store ID) to the print-on-demand engine; the engine syncs your catalogue, takes payment, routes orders, and returns tracking."
---

EP Ecommerce — Printful is the **Printful connector** for [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/), the print-on-demand engine. It is deliberately thin: it holds your [Printful](https://www.printful.com/) credentials and a Test Connection check, and it teaches the engine how to talk to Printful's API. Everything else (syncing your catalogue, the storefront, checkout, shipping quotes, order routing, and tracking) lives in the engine.

Published by [ElmsPark Studio](https://elmspark.com).

## What this plugin does

- Stores your **Printful API Token** and **Store ID**.
- Provides the **Test Connection** button, which confirms the link, lists your stores, and fills in your Store ID.
- Connects the POD engine to Printful so the engine can sync products, quote shipping, route paid orders, and pull back tracking.

On its own it does nothing visible. It is one half of a pair: the engine does the work, this connector supplies the Printful account. Other print-on-demand providers can be added as sibling connectors in the same way.

## Requirements

- **PageMotor 0.7 or later**
- **EP Ecommerce 0.1.22 or later** — adds the generic `pod` product type the engine uses.
- **EP Ecommerce — POD** — the engine that does the actual work.
- **EP Ecommerce — Stripe** — for taking card payment.
- A **Printful account** with a **Manual order / API store**, and an **API token** for that store.

## Important: you need a "Manual order / API" store

This is the one thing that catches people out. Printful only opens its products and orders API on a store of type **Manual order platform / API**. A Printful store that is already linked to Shopify, WooCommerce, Etsy or similar will refuse the connection with a message like "applies only to Manual Order / API platform".

The reason is simple: PageMotor is your shopfront here, and Printful is fulfilment only. So in Printful, open **Stores**, add a store, choose **Manual order platform / API**, then create the token for that store.

The **Test Connection** button checks this for you. It lists every store on your account, marks which are usable, and warns you clearly if none of them is a Manual order / API store.

## Installation

Install in this order, activating each before the next:

1. **EP Ecommerce** (0.1.22+).
2. **EP Ecommerce — POD** (the engine).
3. **EP Ecommerce — Printful** (this connector).
4. **EP Ecommerce — Stripe** (card payment).

Download each from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest). Database tables are created automatically on first load.

## Setup

1. Open **Plugin Settings → EP Ecommerce — Printful**.
2. Paste your **Printful API Token**. Create one on the [Printful Developers page](https://www.printful.com/dashboard/settings/api) (Settings, Developers, add a private token with store scopes).
3. Click **Test Connection**. It works from the token you have just typed, so there is no need to Save first. It confirms the link, lists your stores, and fills in the **Store ID** of your Manual order / API store automatically (most accounts have one usable store).
4. Click **Save**.

That is all you do here. Everything else (enabling print-on-demand, syncing products, delivery pricing, and fulfilment) happens on the [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/) settings page.

## Troubleshooting

### Test Connection says none of your stores is a "Manual order / API" store

Your token is valid, but the store it points at is linked to another platform (Shopify, WooCommerce and so on), which Printful does not open to this API. In Printful, open **Stores**, add a store, choose **Manual order platform / API**, then generate a token for that store and paste it here.

### Test Connection fails outright

Check the token is current and has not been revoked, and that it carries store scopes. Generate a fresh one on the [Printful Developers page](https://www.printful.com/dashboard/settings/api) and try again. A 401 means the token is invalid or expired.

### Everything is connected here, but nothing syncs

Syncing lives in the engine, not in this connector. Open **EP Ecommerce — POD**, tick **Enable print-on-demand**, then click **Sync products**. See the [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/) page.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger, like a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply, usually within a few hours.
