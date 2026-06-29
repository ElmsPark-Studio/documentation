---
title: "EP Ecommerce — Printify"
description: "The Printify connector for EP Ecommerce — POD. Adds your Printify account (API token + Store ID) to the print-on-demand engine; the engine syncs your catalogue, takes payment, routes orders, and returns tracking."
---

EP Ecommerce — Printify is the **Printify connector** for [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/), the print-on-demand engine. It is deliberately thin: it holds your [Printify](https://printify.com/) credentials and a Test Connection check, and it teaches the engine how to talk to Printify's API. Everything else — syncing your catalogue, the storefront, checkout, shipping quotes, order routing, and tracking — lives in the engine.

Published by [ElmsPark Studio](https://elmspark.com).

## What this plugin does

- Stores your **Printify API Token** and **Store ID**.
- Provides the **Test Connection** button that confirms the link and fills in your Store ID.
- Connects the POD engine to Printify so the engine can sync products, quote shipping, route paid orders, and pull back tracking.

On its own it does nothing visible. It is one half of a pair: the engine does the work, this connector supplies the Printify account. Other print-on-demand providers can be added as sibling connectors in the same way.

## Requirements

- **PageMotor 0.7 or later**
- **EP Ecommerce 0.1.22 or later** — adds the generic `pod` product type the engine uses.
- **EP Ecommerce — POD** — the engine that does the actual work.
- **EP Ecommerce — Stripe** — for taking card payment.
- A **Printify account** and a **Personal Access Token**.

## Installation

Install in this order, activating each before the next:

1. **EP Ecommerce** (0.1.22+).
2. **EP Ecommerce — POD** (the engine).
3. **EP Ecommerce — Printify** (this connector).
4. **EP Ecommerce — Stripe** (card payment).

Download each from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest). Database tables are created automatically on first load.

## Setup

1. Open **Plugin Settings → EP Ecommerce — Printify**.
2. Paste your **Printify API Token**. Generate one on your [Printify API & Connections page](https://printify.com/app/account/api).
3. Click **Test Connection**. It confirms the link and fills in your **Store ID** automatically (most accounts have one store). It works from the token you have just typed, so there is no need to Save first.
4. Click **Save**.

That is all you do here. Everything else — enabling print-on-demand, syncing products, delivery pricing, and fulfilment — happens on the [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/) settings page.

## Troubleshooting

### Test Connection fails

Check the token is a current **Personal Access Token** from your [Printify API & Connections page](https://printify.com/app/account/api) and that it has not been revoked. Generate a fresh one and try again.

### Everything is connected here, but nothing syncs

Syncing lives in the engine, not in this connector. Open **EP Ecommerce — POD**, tick **Enable print-on-demand**, then click **Sync products**. See the [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/) page.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours.
