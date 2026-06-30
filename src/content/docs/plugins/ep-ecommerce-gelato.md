---
title: "EP Ecommerce — Gelato"
description: "The Gelato connector for EP Ecommerce — POD. Adds your Gelato account (API key) to the print-on-demand engine. Design products as Gelato draft orders; the engine imports them, takes payment, routes orders, and returns tracking."
---

EP Ecommerce — Gelato is the **Gelato connector** for [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/), the print-on-demand engine. It is deliberately thin: it holds your [Gelato](https://www.gelato.com/) API key and a Test Connection check, and it teaches the engine how to talk to Gelato's API. Everything else (importing your products, the storefront, checkout, shipping quotes, order routing, and tracking) lives in the engine.

Published by [ElmsPark Studio](https://elmspark.com).

## What this plugin does

- Stores your **Gelato API Key** and your preferred **currency**.
- Provides the **Test Connection** button, which confirms the key authenticates.
- Connects the POD engine to Gelato so the engine can import your products, quote shipping, route paid orders, and pull back tracking.

On its own it does nothing visible. It is one half of a pair: the engine does the work, this connector supplies the Gelato account.

## Requirements

- **PageMotor 0.7 or later**
- **EP Ecommerce 0.1.22 or later** — adds the generic `pod` product type the engine uses.
- **EP Ecommerce — POD** — the engine that does the actual work.
- **EP Ecommerce — Stripe** — for taking card payment.
- A **Gelato account** and an **API key**.

## How products work: design them as draft orders

Gelato is different from a catalogue-style provider. It does not expose your products over its API, so there is nothing to "browse and import" in the usual sense. Instead, you build each product as a **draft order** in Gelato, and this connector reads your saved drafts and turns each one into a product on your PageMotor store, with its design, price and preview image.

The flow:

1. In the Gelato dashboard, design your product and **save it as a draft order**. Do not place the order.
2. To offer several sizes or colours of one design, add them as **separate items in the same draft**. Each draft becomes one product, and its items become the size / colour options.
3. Set the retail price on the draft. That is the price your customer pays.
4. In PageMotor, open **EP Ecommerce — POD** and click **Sync**. Your drafts arrive as products.

Your artwork travels with the draft (Gelato keeps it against the design), so the engine has everything it needs to place the real order later. Orders that have actually been placed, and orders your live store creates for customers, are deliberately skipped, so only your hand-built drafts become products.

## Installation

Install in this order, activating each before the next:

1. **[EP Ecommerce](https://updates.elmspark.com/download.php?plugin=ep-ecommerce)** (0.1.22+).
2. **[EP Ecommerce — POD](https://updates.elmspark.com/download.php?plugin=ep-ecommerce-pod)** (the engine).
3. **[EP Ecommerce — Gelato](https://updates.elmspark.com/download.php?plugin=ep-ecommerce-gelato)** (this connector).
4. **[EP Ecommerce — Stripe](https://updates.elmspark.com/download.php?plugin=ep-ecommerce-stripe)** (card payment).

Database tables are created automatically on first load.

## Setup

1. Open **Plugin Settings → EP Ecommerce — Gelato**.
2. Paste your **Gelato API Key**. Create one on the [Gelato API keys page](https://dashboard.gelato.com/keys/manage) (Settings, API keys).
3. Set your **Currency** (for example USD, EUR or GBP). It defaults to USD. Gelato may quote in a different currency, and the engine trusts whatever Gelato returns.
4. Click **Save**, then **Test Connection**. Gelato has no store id, so nothing is auto-filled; a green result simply confirms the key works.

Then design your products as draft orders (above), open [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/), and click **Sync**.

## Troubleshooting

### Test Connection fails

Check the key is current on your [Gelato API keys page](https://dashboard.gelato.com/keys/manage). A 401 means the key is invalid or expired. Create a fresh one and try again.

### Sync finds no products

This connector imports your Gelato **draft orders**, not your order history or a catalogue. In Gelato, make sure you have saved at least one **draft order** (designed but not placed), then open EP Ecommerce — POD and click Sync. Orders you have already placed, and orders created by your live store for customers, are skipped by design.

### A product is missing its design, or shows "not connected"

Each draft needs a finished design attached in Gelato, because the connector carries the design through to the real order. Re-open the draft in Gelato, confirm the design is applied, save it again, then re-Sync.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger, like a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply, usually within a few hours.
