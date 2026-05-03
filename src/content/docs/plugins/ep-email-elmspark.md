---
title: "EP Email ElmsPark"
description: "ElmsPark Email managed delivery service for EP Email. One API key, proper SMTP via AWS SES, no server config. Drop-in alternative to configuring SMTP yourself."
sidebar:
  order: 26
---

EP Email ElmsPark is a transport driver for [EP Email](/plugins/ep-email/). Instead of configuring SMTP against Mailgun, SendGrid, or your own mail server, you paste an ElmsPark Email API key and your outbound mail routes through ElmsPark's managed delivery service, backed by AWS SES.

Published by [ElmsPark Studio](https://elmspark.com).

## Why use it

Configuring SMTP correctly is fiddly. You need:

- An SMTP provider account (often separate from your hosting).
- Correct SPF, DKIM, and DMARC DNS records for your domain.
- Careful handling of from-addresses to avoid spam triggers.
- Monitoring of bounces and complaints.

Most sites get at least one of these wrong at launch and end up in spam folders for weeks.

ElmsPark Email bundles all of that behind a single API key. Sign up at [send.elmspark.com](https://send.elmspark.com), verify your domain with a couple of DNS records, paste the key into this plugin, and delivery works.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Email** (required; this is a transport driver for EP Email)
- **EP Suite base class**
- **An ElmsPark Email account** from [send.elmspark.com](https://send.elmspark.com)

## Installation

1. Install **EP Email** first.
2. Download `ep-email-elmspark.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → ElmsPark Email**.
5. Paste your API key.
6. In **EP Email → SMTP**, set the transport dropdown to **ElmsPark Email**.

All outbound mail now routes through ElmsPark.

## Setting up at send.elmspark.com

1. Create an account at [send.elmspark.com](https://send.elmspark.com).
2. Add your sending domain (e.g. `yoursite.com`).
3. Follow the DNS instructions — typically one CNAME (or two TXT) records for DKIM, and a TXT record for SPF.
4. Wait for domain verification (usually minutes, sometimes up to an hour).
5. Create an API key. Copy it.
6. Paste into the plugin settings.

## Delivery behaviour

- Email is submitted to ElmsPark's API over HTTPS.
- ElmsPark forwards to AWS SES for actual delivery.
- Bounces and complaints are tracked on your ElmsPark dashboard.
- EP Email's own delivery log records every send with status.

## What the settings page shows

- **API key** input.
- **Status indicator**: green if the key validates and the domain is verified.
- **Today's send count**: how many emails have gone out today.
- **Monthly quota**: if your plan has a cap, shows usage against it.

## Troubleshooting

### "API key rejected"

Copy the key again carefully from [send.elmspark.com](https://send.elmspark.com). Watch for leading/trailing whitespace.

### "Emails not delivering despite a valid key"

Check your sending domain's verification status on [send.elmspark.com](https://send.elmspark.com). If DNS records are wrong, ElmsPark won't deliver. Fix the DNS, wait for re-verification.

### "Emails go to spam"

Domain verification usually fixes this. If you've verified and still hit spam, check:
- Your from-address matches your verified sending domain.
- SPF and DMARC are configured correctly on the top-level domain.
- Your subject lines and content aren't spam-triggering (all-caps subjects, excessive link density).

### "EP Email shows ElmsPark as an option but nothing sends through it"

The dropdown in EP Email → SMTP needs to be set to **ElmsPark Email**. Just activating this plugin registers the driver as available; selecting it makes it active.

### "I want to switch away from ElmsPark"

Open **EP Email → SMTP**, change transport to SMTP or another driver. Configure the alternative. No data migration needed — switch happens instantly.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
