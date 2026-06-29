---
title: "EP Newsletter Brevo"
description: "Brevo (formerly Sendinblue) delivery driver for EP Newsletter. 300/day forever-free tier, no credit card, batch sending to 1,000 per request, optional HMAC-signed webhooks."
---

EP Newsletter Brevo is a delivery driver for [EP Newsletter](/plugins/ep-newsletter/). When installed and selected, campaigns send through Brevo's transactional email API instead of your general SMTP. Brevo's forever-free plan is 300 emails/day with no credit card required, making it the strongest free-tier option for small to mid-size newsletter lists.

Published by [ElmsPark Studio](https://elmspark.com).

## Why use Brevo

Brevo (formerly Sendinblue) is one of very few transactional email providers to retain a genuine card-free forever-free tier. The free plan offers:

- **300 emails/day forever** with no expiry and no card on file
- **100,000 contacts allowed** in your Brevo account
- **Full API access** including transactional sending, webhooks, suppression list management
- **Both EU and global infrastructure** with privacy-conscious routing

For EP Newsletter campaigns, the Brevo driver gives you:

- HTTP API delivery, no per-connection SMTP rate limits
- Batch sending via Brevo's `messageVersions` parameter (up to 1,000 recipients per request, each with their own To: header)
- Connection test, bounce polling, and optional HMAC-SHA256 webhook signature verification

## Requirements

- **PageMotor 0.6 or later**
- **EP Newsletter** (required)
- **EP Suite base class** (bundled)
- **A Brevo account** with a verified sender email

## Installation

1. Install EP Newsletter first.
2. Download `ep-newsletter-brevo.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Configure the plugin (see below).
5. Open **Plugin Settings → EP Newsletter → Email Delivery**.
6. Select **Brevo** as the driver.

## Setting up Brevo

### Step 1 — Sign up

Sign up at [brevo.com](https://onboarding.brevo.com/account/register). No credit card required for the free tier.

### Step 2 — Verify a sender

Brevo will not let you send any email until at least one sender is verified. Go to **Senders, Domains & Dedicated IPs → Senders** and add an email address you control. Brevo emails a confirmation link; click it to verify.

For higher deliverability, also verify your full sending domain (DKIM, SPF, DMARC records). Domain verification is optional for the free tier but recommended for any production volume.

### Step 3 — Create an API v3 key

Go to **Account → SMTP & API → API keys** (or directly at [app.brevo.com/settings/keys/api](https://app.brevo.com/settings/keys/api)). Click **Generate a new API key**, name it something descriptive (e.g. `ep-newsletter-brevo`), and copy the value when shown. The key format is `xkeysib-...` (long alphanumeric).

**Important: do NOT enable IP blocking** on the API keys page unless your PageMotor host has a static public IP and you've added it to **Security → Authorized IPs** in Brevo. Most shared hosting environments have dynamic egress IPs that will cause all API calls to fail with 401 if blocking is on.

### Step 4 — Configure the plugin

Open **Plugin Settings → EP Newsletter Brevo**.

- **API v3 Key.** From step 3.
- **Verified Sender Email.** The email you verified in step 2.
- **Sender Display Name.** What recipients see in their inbox From: column.

Click **Save**.

### Step 5 — Test

Use the **Test Connection** button. A green confirmation means the API key is valid and the connection works. The result also shows your Brevo plan type.

### Step 6 — Set up the webhook (optional but recommended)

For real-time bounce, complaint, and unsubscribe processing:

1. In Brevo, go to **Transactional → Settings → Webhooks**.
2. Add a webhook URL: copy from the EP Newsletter Brevo settings page (format `https://yoursite.com?ep_newsletter_webhook=brevo`).
3. Select events: `hardBounce`, `softBounce`, `spam`, and `unsubscribed`.
4. Optional: set a shared secret. Paste the same secret value into the **Webhook Signing Secret** field in the plugin settings. The plugin will verify every incoming webhook against the secret using HMAC-SHA256.

## How campaigns send

1. You send a campaign from EP Newsletter.
2. EP Newsletter batches recipients into chunks of up to 1,000.
3. For each chunk, the plugin POSTs to `/v3/smtp/email` with a `messageVersions` array, each version targeting one recipient so they only see their own address in the To: header.
4. Brevo queues and delivers each version.
5. Webhook events update your EP Newsletter subscriber list in real time (if configured).
6. Periodic cron also polls Brevo's `blockedContacts` endpoint as a fallback.

## Pairs with EP Email Brevo

For unified sender reputation across newsletters and transactional email, install [EP Email Brevo](/plugins/ep-email-brevo/) too. Both plugins can share the same Brevo account, API key, and verified sender. Every email leaving your site, whether transactional or campaign, flows through the same authenticated sender.

## Troubleshooting

### "Test connection fails with 401"

The API key is invalid, or IP blocking is enabled and your server's egress IP is not in Brevo's Authorized IPs list. Easiest fix: turn off IP blocking in Brevo (Account → SMTP & API → API keys → "Block unauthorized IP addresses").

### "Campaign sends fail with 'sender not allowed'"

The sender email you've configured isn't verified in Brevo. Go to Senders, Domains & Dedicated IPs → Senders and confirm the address shows as Verified.

### "Hit the 300/day limit"

Brevo's free plan is hard-capped at 300 sends per UTC day. Upgrade to Starter (£21/month for 20k emails/month) or higher for larger volumes. Or split your newsletter into smaller segments scheduled across multiple days.

### "I want to switch from SendGrid to Brevo"

In EP Newsletter settings, change Delivery driver from SendGrid to Brevo. New campaigns from that point on route through Brevo. Past campaign history stays intact.

## Feedback

For a quick question, **EP Support** inside your admin is the fastest path. For anything bigger, open a ticket at [help.elmspark.com](https://help.elmspark.com).
