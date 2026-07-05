---
title: "EP Ecommerce — Prodigi"
description: "The Prodigi connector for EP Ecommerce — POD. Adds your Prodigi account (API key) to the print-on-demand engine. Prodigi has no catalogue API, so you list your products by SKU; the engine takes payment, routes orders, and returns tracking."
---

EP Ecommerce — Prodigi is the **Prodigi connector** for [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/), the print-on-demand engine. It is deliberately thin: it holds your [Prodigi](https://www.prodigi.com/) API keys, your product list, and a Test Connection check, and it teaches the engine how to talk to Prodigi's API. Everything else (the storefront, checkout, shipping quotes, order routing, and tracking) lives in the engine.

Published by [ElmsPark Studio](https://elmspark.com).

## What this plugin does

- Stores your Prodigi **sandbox and live API keys**, your chosen **environment**, your **currency**, and your **product list**.
- Provides the **Test Connection** button, which confirms the key works against the selected environment.
- Connects the POD engine to Prodigi so the engine can quote shipping, route paid orders, and pull back tracking.

On its own it does nothing visible. It is one half of a pair: the engine does the work, this connector supplies the Prodigi account and your product list.

## Requirements

- **PageMotor 0.7 or later**
- **EP Ecommerce 0.1.22 or later** — adds the generic `pod` product type the engine uses.
- **EP Ecommerce — POD** — the engine that does the actual work.
- **EP Ecommerce — Stripe** — for taking card payment.
- A **Prodigi account** and an **API key** (sandbox and/or live).

## Sandbox and live keys

Prodigi gives you two separate API keys: one for **sandbox** (test, no real charges) and one for **live** (real, charged orders). The keys are environment-scoped, so a sandbox key only works against the sandbox, and a live key only against live.

You paste both keys into the settings and choose which one is active with the **Environment** dropdown. Start in **Sandbox** so you can rehearse the whole flow (sync, storefront, checkout, a test order) for free, then switch to **Live** when you are ready to sell.

## How products work: list them by SKU

Prodigi has no catalogue API and no templates, so there is nothing to sync from your account. Instead, you list the products you want to sell directly in the settings, **one per line**, using a simple pipe-delimited format:

```
SKU | retail_price | asset_url | Title | attr=val,attr=val | sizing
```

- **SKU** (required) — the Prodigi product code, for example `GLOBAL-CAN-10x10`. Find it in your Prodigi dashboard.
- **retail_price** (required) — the selling price, for example `24.99`.
- **asset_url** (required) — a publicly reachable URL to your print-file image.
- **Title** (optional) — the storefront product name. Falls back to the SKU.
- **attributes** (optional) — a comma list of `attr=val` pairs, for example `wrap=ImageWrap`.
- **sizing** (optional) — one of `fillPrintArea`, `fitPrintArea` or `stretchToPrintArea`. Defaults to `fillPrintArea`.

Only the first three fields are required. Blank lines, and lines that start with `#`, are ignored, so you can leave yourself comments.

Example:

```
GLOBAL-CAN-10x10 | 24.99 | https://cdn.example.com/art/owl.png | Owl Canvas | wrap=ImageWrap | fillPrintArea
```

To sell the same SKU in more than one variant (different attributes or sizing), add a line for each, and the connector keeps them as distinct products. Once your list is in, open **EP Ecommerce — POD** and click **Sync**.

## How orders are handled, and why they wait

One difference worth knowing: Prodigi charges as soon as an order is created. It has no "draft" or "on hold" state like some other providers, where creating the order is free until you confirm it.

To protect you from accidental charges, the engine holds each paid Prodigi order on your own site, and only sends it to Prodigi when you choose: either by turning on **auto-submit** in EP Ecommerce — POD (a background task then drains held orders), or by sending an order explicitly. So your customer pays at checkout as normal and the order is captured safely, but Prodigi is only charged at the moment of production. Test the whole path in Sandbox first.

## Installation

Install in this order, activating each before the next:

1. **[EP Ecommerce](/plugins/ep-ecommerce/)** (0.1.22+).
2. **[EP Ecommerce — POD](/plugins/ep-ecommerce-pod/)** (the engine).
3. **[EP Ecommerce — Prodigi](/plugins/ep-ecommerce-prodigi/)** (this connector).
4. **[EP Ecommerce — Stripe](/plugins/ep-ecommerce-stripe/)** (card payment).

Database tables are created automatically on first load.

## Setup

1. Open **Plugin Settings → EP Ecommerce — Prodigi**.
2. Set **Environment** to **Sandbox** to begin.
3. Paste your **Sandbox API Key** (and your **Live API Key** too, ready for later). Create keys in the [Prodigi dashboard](https://dashboard.prodigi.com/).
4. Set your **Currency** (for example USD, EUR or GBP). It defaults to USD.
5. In **Products**, list your products one per line (see above).
6. Click **Save**, then **Test Connection**. It confirms the key authenticates against the selected environment.

Then open [EP Ecommerce — POD](/plugins/ep-ecommerce-pod/) and click **Sync**.

## Troubleshooting

### Test Connection fails

Make sure the key matches the selected **Environment**: a sandbox key only works in Sandbox, a live key only in Live. A 401 usually means the key is for the wrong environment, or is invalid or expired. Copy the right key from the [Prodigi dashboard](https://dashboard.prodigi.com/) and try again.

### Sync finds no products

Prodigi has no catalogue, so the engine builds your catalogue from the **Products** list in these settings. Add at least one valid line (SKU, price and asset URL are required), Save, then Sync. Lines with a missing SKU, missing price, missing asset URL, or a price of zero are skipped.

### An order has not reached Prodigi

That is by design until you send it (see "How orders are handled" above). Turn on **auto-submit** in EP Ecommerce — POD to drain held orders automatically, or send the order explicitly. Remember Prodigi charges at that point, so confirm you are in the right environment first.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on.

For anything bigger, like a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply, usually within a few hours.
