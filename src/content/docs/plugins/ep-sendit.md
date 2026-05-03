---
title: "EP SendIt"
description: "ElmsPark Email (send.elmspark.com) transport driver for EP Email. Managed delivery powered by AWS SES. Single-API-key setup."
sidebar:
  order: 49
---

EP SendIt is a transport driver for [EP Email](/plugins/ep-email/) that routes mail through [send.elmspark.com](https://send.elmspark.com) — ElmsPark's managed delivery service, backed by AWS SES. Single API key, no SMTP config, no bounces to handle manually.

Published by [ElmsPark Studio](https://elmspark.com).

## Is this the same as EP Email ElmsPark?

Yes, nearly. Both plugins are transport drivers for the same send.elmspark.com service. Use whichever ships with your current EP Suite download — they do the same job. This guide covers EP SendIt's version of the integration.

## Why use it

Configuring SMTP well is fiddly. Getting into inboxes reliably requires SPF, DKIM, DMARC set up correctly, plus ongoing monitoring for bounces and complaints. ElmsPark Email handles all of that behind a single API key.

- **One API key**, no SMTP credentials to rotate.
- **AWS SES reliability** under the hood.
- **Domain verification** via DNS, guided setup.
- **Bounce and complaint handling** automatic.
- **Usage dashboard** at send.elmspark.com.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required)
- **EP Suite base class**
- **A send.elmspark.com account**

## Installation

1. Install **EP Email**.
2. Download `ep-sendit.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP SendIt**.
5. Paste your send.elmspark.com API key.
6. In **EP Email → SMTP**, set transport to **ElmsPark Email**.

## Setting up at send.elmspark.com

1. Create an account at [send.elmspark.com](https://send.elmspark.com).
2. Add your sending domain (e.g. `yoursite.com`).
3. Add the DNS records shown — usually one CNAME (or two TXT) for DKIM and one TXT for SPF.
4. Wait for domain verification.
5. Create an API key. Copy it into EP SendIt.

## Status dashboard

The settings page shows:

- API key status (green if valid and domain verified).
- Today's send count.
- Monthly quota if your plan has one.

## Troubleshooting

### "API key rejected"

Copy the key again from send.elmspark.com. Check for whitespace.

### "Emails not delivering"

Domain verification is probably incomplete. Check status on send.elmspark.com. Fix DNS if records are missing.

### "I have both EP SendIt and EP Email ElmsPark — which wins?"

EP Email lets you pick one transport at a time in its SMTP settings. Pick whichever is configured. They don't conflict if only one is selected.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
