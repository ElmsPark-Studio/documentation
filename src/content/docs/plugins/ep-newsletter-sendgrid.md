---
title: "EP Newsletter SendGrid"
description: "SendGrid delivery driver for EP Newsletter. High-volume sending with automatic bounce and complaint handling via SendGrid webhooks."
sidebar:
  order: 40
---

EP Newsletter SendGrid is a delivery driver for [EP Newsletter](/plugins/ep-newsletter/). When installed and selected, campaigns send through SendGrid instead of your general SMTP. Better for high-volume campaigns, with automatic bounce and complaint handling through SendGrid's webhooks.

Published by [ElmsPark Studio](https://elmspark.com).

## Why use SendGrid

General SMTP providers rate-limit per-connection (often 14 per second or 100 per minute). For a campaign to 50,000 subscribers, that's at least 8 hours of SMTP activity. Even well-configured SMTP providers start flagging reputation after a few thousand emails per day.

SendGrid is designed for high-volume campaigns:

- **Higher rate limits** — hundreds of emails per second on paid plans.
- **Built-in bounce and complaint handling** — no DIY webhook infrastructure.
- **Dedicated IPs** available for large senders.
- **Reputation monitoring** in your SendGrid dashboard.

If you send fewer than 1,000 emails a month and your SMTP provider is happy, you don't need this. If you're sending tens of thousands per campaign, this is the right tool.

## Requirements

- **PageMotor 0.8.2b or later**
- **EP Newsletter** (required)
- **EP Suite base class**
- **A SendGrid account** with an API key

## Installation

1. Install **EP Newsletter** first.
2. Download `ep-newsletter-sendgrid.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP Newsletter → Email delivery**.
5. Select **SendGrid** as the driver.

## Setting up SendGrid

### Step 1 — Get an API key

1. Log in to your [SendGrid account](https://app.sendgrid.com/).
2. Go to **Settings → API Keys → Create API Key**.
3. Name it (e.g. "PageMotor newsletter").
4. Permissions: **Full Access** is easiest; **Restricted** with Mail Send and Tracking scopes is more secure.
5. Copy the key (shown once; store in a password manager).

### Step 2 — Verify your sender

SendGrid requires sender verification:

- **Single Sender Verification** (quick) — verify one email address you'll send from.
- **Domain Authentication** (recommended) — add DNS records (DKIM, SPF) so emails come from `@yoursite.com`.

Follow SendGrid's setup wizard under **Settings → Sender Authentication**.

### Step 3 — Configure the plugin

Open **Plugin Settings → EP Newsletter SendGrid**.

- **API key.** Paste from step 1.
- **Default from-name and from-email.** Must match your verified sender.
- **Categories.** Optional SendGrid tags for campaign tracking (e.g. "weekly-digest", "product-launch").

### Step 4 — Test

Use the **Test connection** button. If green, you're ready.

### Step 5 — Set up the webhook

SendGrid pushes bounce and complaint events to your site via webhook.

1. In SendGrid, go to **Settings → Mail Settings → Event Webhook**.
2. URL: copy from the EP Newsletter SendGrid settings page.
3. Select events: **Bounced, Dropped, Spam Report, Unsubscribe** at minimum.
4. Save.
5. Click **Test your integration** from SendGrid to verify.

From this point on, SendGrid events auto-update your subscriber list.

## How campaigns send

1. You send a campaign from EP Newsletter.
2. EP Newsletter batches the recipients.
3. For each batch, EP Newsletter SendGrid calls SendGrid's Mail Send API with the personalised payload.
4. SendGrid delivers. Events (delivered, bounced, opened, clicked) are tracked on the SendGrid side.
5. Bounce and spam-report events fire the webhook. EP Newsletter marks those addresses as bad automatically.

## Bounce handling

Two types:

- **Soft bounce** (mailbox full, temporary issue). EP Newsletter retries in a subsequent campaign. After 3 soft bounces, treated as a hard bounce.
- **Hard bounce** (address doesn't exist). Address is immediately marked as bad and excluded from all future campaigns.

Complaints (spam reports) immediately disable the subscriber's marketing consent.

## Troubleshooting

### "Test connection fails"

API key is wrong, expired, or has insufficient permissions. Regenerate in SendGrid and paste again. Check the API key has at least Mail Send permission.

### "Campaign sends but emails don't arrive"

Check SendGrid's own activity log at **Activity → Activity Feed**. SendGrid knows exactly why an email was dropped. Common reasons:

- Sender not verified.
- Recipient on your suppression list (previously bounced).
- Content triggering spam filters.

### "Bounces aren't being flagged"

The event webhook isn't configured or isn't reaching your site. In SendGrid, go to the webhook settings and check recent activity — failed deliveries show status codes. Fix URL, firewall, or HTTPS cert issues.

### "I'm being charged more than expected"

SendGrid charges by email sent. Check your Stats page to see actual volume. Verify you're on the plan matching your volume.

### "I want to switch back to regular SMTP"

In EP Newsletter settings, change Delivery driver from SendGrid to EP Email. Campaigns from that point on route through SMTP. Past campaign history stays intact.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger — a bug report, a feature request, or a "how do I..." that needs a real reply — open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
