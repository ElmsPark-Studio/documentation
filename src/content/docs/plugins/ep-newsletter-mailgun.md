---
title: "EP Newsletter Mailgun"
description: "Mailgun delivery driver for EP Newsletter. Free 100/day tier, EU region support for GDPR-clean routing, batch sending to 1,000 per request, HMAC-signed webhook bounce handling."
---

EP Newsletter Mailgun is a delivery driver for [EP Newsletter](/plugins/ep-newsletter/). When installed and selected, campaigns send through Mailgun's HTTP API instead of your general SMTP, with batch sending up to 1,000 recipients per request and real-time bounce and complaint handling via signed webhooks.

Published by [ElmsPark Studio](https://elmspark.com).

## Why use Mailgun

Mailgun is one of the longest-running transactional email providers, with a strong deliverability reputation particularly into corporate inboxes. The free tier is genuinely card-free at 100 emails/day forever, with 1 custom sending domain included.

For EP Newsletter campaigns, the Mailgun driver gives you:

- **HTTP API delivery** rather than per-connection SMTP rate limits.
- **Batch sending** of up to 1,000 recipients per API call via Mailgun's recipient-variables.
- **EU region support** for GDPR-clean routing of audience data.
- **HMAC-signed webhooks** for real-time bounce, complaint, and unsubscribe processing.
- **Free 100/day tier** with no credit card required, suitable for small newsletter lists.

If your campaign volume sits comfortably under 100 emails/day, Mailgun's free plan covers you without any cost. Above that, paid plans scale linearly with volume.

## Requirements

- **PageMotor 0.6 or later**
- **EP Newsletter** (required)
- **EP Suite base class** (bundled)
- **A Mailgun account** with a sending key and verified domain

## Installation

1. Install **EP Newsletter** first.
2. Download `ep-newsletter-mailgun.zip` from the [EP Suite downloads page](https://updates.elmspark.com/download.php?plugin=ep-newsletter-mailgun).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Configure the plugin (see below).
5. Open **Plugin Settings → EP Newsletter → Email Delivery**.
6. Select **Mailgun** as the driver.

## Setting up Mailgun

### Step 1 — Sign up and pick your region

Sign up at [mailgun.com](https://signup.mailgun.com/new/signup). During signup, choose your **Region**:

- **US** (`api.mailgun.net`) for North American audiences.
- **EU** (`api.eu.mailgun.net`) for European/UK audiences and GDPR-clean routing.

Region is locked per domain for life. You cannot move a verified domain between US and EU later. Pick correctly first time.

### Step 2 — Verify your sending domain

On the Mailgun dashboard, go to **Send → Sending → Domains** and add your domain (for example `mg.yoursite.com`). Follow Mailgun's DNS instructions: a TXT record for SPF, two CNAME records for DKIM, and an MX record pair for receiving bounces.

The Free plan includes 1 custom verified domain. You can also use the auto-provisioned `sandboxXXXXX.mailgun.org` domain for testing, but sandbox sending is restricted to authorised recipients only.

#### Critical DNS rule: one SPF, one DMARC per domain

Mail receivers treat multiple SPF records at the same DNS name as a PermError. The same applies to DMARC. If two SPF records exist at the same domain, **all senders fail authentication**, not just the new one. This is the single most common way email setups get accidentally broken during ESP setup.

**The good news for this Mailgun setup**: all the records we're adding live on the `mg.<your-domain>` subdomain, **not the apex**. That means any existing SPF or DMARC at the apex (Google Workspace, Microsoft 365, IONOS Mail, etc.) is completely untouched. You can't accidentally break existing email setups by following these instructions.

**If you ever do need to combine SPF includes** (e.g. you already have `v=spf1 include:_spf.google.com ~all` at the apex and want to also send `From: <addr>@apex-domain` via Mailgun), merge into ONE record:

```
v=spf1 include:_spf.google.com include:mailgun.org ~all
```

Not as two separate records. Watch the 10-DNS-lookup SPF limit too — each `include:` uses one or more lookups.

For DMARC: there is only ever one record per DNS name. If a DMARC already exists at the location you need to set, **edit the existing one**, don't add a second.

### Step 3 — Create a sending key

In **Domain settings → Sending keys**, click **Add sending key** and give it a descriptive name (for example `ep-newsletter-mailgun`). Copy the key value the moment it appears, as Mailgun only shows it once.

Sending keys are domain-scoped and have permission to call the `/messages` endpoint for their specific domain. This is the secure modern approach compared to account-level master keys.

#### Don't confuse the Sending Key with other Mailgun credentials

Mailgun has three different credential types that look similar but go in different places:

- **Sending Key** — this one, for the plugin's "Sending Key" field. Long hex string with dashes, in the format `<32 hex characters>-<8 hex>-<8 hex>`. Found at Domain settings → Sending keys.
- **SMTP password** — for SMTP-based integrations (different plugin path). Found at Domain settings → SMTP credentials. **Don't paste this into the Sending Key field — the plugin uses the HTTP API, not SMTP, and will fail authentication.**
- **HTTP Webhook Signing Key** — for verifying inbound webhook signatures (Step 6). Found at Settings → API Security. **Different field, different purpose.**

Pasting the wrong credential is the most common Mailgun setup mistake. If your Test Connection comes back with a 401 or "unauthorized" error, double-check you've got the right credential type for each field.

### Step 4 — Configure the plugin

Open **Plugin Settings → EP Newsletter Mailgun**.

- **Sending Key.** Paste from step 3. NOT the SMTP password and NOT the Webhook Signing Key (see the warning under step 3 if you're not sure which credential you've got).
- **Sending Domain.** Your verified Mailgun domain (e.g. `mg.yoursite.com`).
- **Region.** US or EU, matching the region you picked at signup.
- **HTTP Webhook Signing Key.** From **Settings → API Security → HTTP Webhook Signing Key** on your Mailgun account. Optional but recommended for production. Note: Mailgun shows the same value in two places in its UI (also under Sending → Webhooks → Configuration). Both are the same key — paste either.

Click **Save**.

### Step 5 — Test

Use the **Test Connection** button. A green confirmation means the sending key, domain, and region all check out.

### Step 6 — Set up the webhook (recommended)

For real-time bounce handling, configure a Mailgun Events Webhook.

1. In Mailgun, go to **Sending → Webhooks**.
2. Click **Add webhook**.
3. **URL** field: paste this URL pattern, substituting your real site URL:

   ```
   https://YOUR-SITE-URL/?ep_newsletter_webhook=mailgun
   ```

   The plugin settings page also displays this URL pre-filled with your actual site URL — copy it directly from there to avoid typos.
4. **Event types**: select **failed**, **complained**, and **unsubscribed** at minimum. (Optionally add **delivered** and **opened** if you want EP Newsletter to record those too.)
5. Save the webhook.
6. Click **Test webhook** in Mailgun to verify your site responds with `200 OK`.

From this point on, Mailgun events automatically update your EP Newsletter subscriber list. The plugin verifies every incoming webhook against the HTTP Webhook Signing Key using HMAC-SHA256, with a 5-minute replay-protection window.

## How campaigns send

1. You send a campaign from EP Newsletter.
2. EP Newsletter batches the recipients into chunks of up to 1,000.
3. For each chunk, the plugin POSTs to `/v3/{your-domain}/messages` with a comma-separated recipient list and a `recipient-variables` JSON object so each recipient only sees their own address in the To header.
4. Mailgun delivers each message. Events (delivered, opened, clicked, failed, complained) are recorded in your Mailgun dashboard.
5. Failure and complaint events fire the webhook. EP Newsletter marks those addresses as bad automatically.

## Bounce handling

Two types:

- **Soft bounce** (temporary failure like a full mailbox). Mailgun event `failed` with severity `temporary`. EP Newsletter retries on the next campaign; after repeated soft bounces it treats the address as hard-bounced.
- **Hard bounce** (address does not exist). Mailgun event `failed` with severity `permanent`. Address is marked bad immediately and excluded from future campaigns.

Spam complaints (Mailgun event `complained`) and unsubscribes (event `unsubscribed`) immediately remove marketing consent.

## EU region note

If your audience is in the EU/UK and you need GDPR-clean routing, choose the EU region during Mailgun signup. The region selection is locked per domain. To switch regions you would have to create a new domain in the new region and re-verify DNS, then update the plugin's Sending Domain and Region settings.

## Troubleshooting

### "Test connection fails with 401 or 403"

The sending key is invalid, expired, or belongs to a different domain. Regenerate in Mailgun (Domain settings → Sending keys) and paste again. Watch for leading/trailing whitespace.

### "Test connection fails with 404 (Sending domain not found)"

Two common causes. Either the domain spelling is wrong, or the domain is in a different region than the plugin is configured for. Mailgun's US and EU regions are separate accounts internally. Make sure the Region setting matches where the domain was created.

### "Campaign sends but emails don't arrive"

Check Mailgun's own log at **Send → Logs**. Mailgun records every delivery attempt and Gmail/Outlook/etc's response. Common reasons emails fail:

- Domain not DNS-verified (DKIM, SPF, DMARC records missing or wrong).
- Recipient on your Mailgun suppression list (previously bounced).
- Content triggering recipient-side spam filters.

### "Emails go to spam from a sandbox domain"

Expected. Sandbox domains don't have proper DMARC alignment and most receivers (Gmail especially) quarantine them. Verify a custom domain and use that as the Sending Domain. Sandbox is for testing only.

### "Webhook events not arriving"

Check Mailgun's webhook delivery log at **Sending → Webhooks → \[your webhook\] → Logs**. Each delivery attempt shows status codes. Common issues:

- Webhook URL wrong (must point to `?ep_newsletter_webhook=mailgun` on your live site).
- Site firewall blocking Mailgun's webhook IPs.
- HTTPS certificate invalid.
- Webhook Signing Key in the plugin doesn't match Mailgun's. Bad signatures cause the plugin to drop events silently.

### "I want to switch from SendGrid to Mailgun"

In EP Newsletter settings, change Delivery driver from SendGrid to Mailgun. New campaigns from that point on route through Mailgun. Past campaign history stays intact. You may want to import your SendGrid suppression list into Mailgun first to preserve bounce records.

## Pairs with EP Email Mailgun

For unified sender reputation across newsletters and transactional email, install [EP Email Mailgun](/plugins/ep-email-mailgun/) too. Both plugins can share the same Mailgun account, sending key, and verified domain. Every email leaving your site flows through the same authenticated sender, building deliverability reputation faster.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger such as a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
