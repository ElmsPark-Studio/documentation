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

1. **[EP Ecommerce](/plugins/ep-ecommerce/)** (0.1.22+).
2. **[EP Ecommerce — POD](/plugins/ep-ecommerce-pod/)** (the engine).
3. **[EP Ecommerce — Printify](/plugins/ep-ecommerce-printify/)** (this connector).
4. **[EP Ecommerce — Stripe](/plugins/ep-ecommerce-stripe/)** (card payment).

Database tables are created automatically on first load.

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

## Changelog

### 1.1.8

- **Fixes stored keys and passwords reading as empty after a PageMotor 0.11.3 or 0.11.4 update.** After the core update, every secret this plugin had encrypted at rest came back blank, so anything that needed it failed with an authentication error until the value was typed in again. Nothing was deleted: the encrypted value was still in the settings row, but PageMotor 0.11.3 moved the site secret that opens it, and this plugin was still looking in the old place. It now finds the secret in both places, so an existing value opens again without re-entry, and a value that was re-entered in the meantime keeps working and is moved back under the site secret.
- If you updated PageMotor and then re-entered a key or password, there is nothing to do. If you updated and have not re-entered it, this release restores it on the next page load.

### 1.1.7

- **Your Printify API key is now stored encrypted.** Until this release it sat in plain text in the plugin's settings, where anyone holding an API or MCP connection to your site with permission to configure plugins could read it straight back out. Your site's visitors were never able to see it.
- Existing sites convert themselves the next time the plugin loads, once. There is nothing to re-enter and no key to replace.
- Reading your settings over the API now returns a placeholder rather than the value, and writing that placeholder back leaves the stored secret untouched. Clearing it by submitting an empty value still works as before.
- On hosting without encryption support the previous behaviour is kept and the reason is written to the log, because quietly discarding a working key would be worse than the exposure this closes.
