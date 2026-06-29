---
title: "EP Email Mailgun"
description: "Mailgun transactional transport for EP Email. Routes all transactional email (contact forms, password resets, system notifications) through Mailgun's HTTP API with EU region support."
---

EP Email Mailgun is a transport driver for [EP Email](/plugins/ep-email/). When selected as the active transport, all transactional email from your site (contact form notifications, password resets, opt-in confirmations, system alerts) routes through Mailgun's HTTP API instead of PHP `mail()` or a generic SMTP server.

Published by [ElmsPark Studio](https://elmspark.com).

## Why route transactional email through Mailgun

PHP `mail()` is the default for transactional sends on most hosts, but it has serious deliverability problems:

- No DKIM signing of outbound mail.
- Sender domain often does not match SPF records.
- Hosts share IP reputation with whoever else is on the same server.

The result: password reset emails land in spam, contact form replies never arrive, and users start ringing you up to ask why.

Routing transactional through a known-good ESP fixes this. Mailgun specifically gives you:

- **Domain-authenticated sending** (DKIM, SPF, DMARC alignment) so receivers trust your mail.
- **EU region** for GDPR-clean routing of user-data-bearing emails.
- **Free 100/day tier** with no credit card, suitable for low-volume transactional traffic.
- **Pairs cleanly with EP Newsletter Mailgun** so newsletter and transactional sends share one Mailgun account and one verified domain.

## Requirements

- **PageMotor 0.6 or later**
- **EP Email** (required; this is a transport driver for EP Email)
- **EP Suite base class** (bundled)
- **A Mailgun account** with a sending key and verified domain

## Installation

1. Install **EP Email** first.
2. Download `ep-email-mailgun.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP Email Mailgun**.
5. Paste your Sending Key, Sending Domain, and Region.
6. In **EP Email → SMTP**, set the Transport dropdown to **Mailgun**.

All outbound transactional mail now routes through Mailgun.

## Setting up Mailgun

If you already set up Mailgun for [EP Newsletter Mailgun](/plugins/ep-newsletter-mailgun/), reuse the same credentials. Otherwise:

### Step 1 — Sign up and pick your region

Sign up at [mailgun.com](https://signup.mailgun.com/new/signup). During signup, choose your **Region**:

- **US** (`api.mailgun.net`) for North American audiences.
- **EU** (`api.eu.mailgun.net`) for European/UK audiences and GDPR-clean routing.

Region is locked per domain for life.

### Step 2 — Verify your sending domain

Add your sending domain at **Send → Sending → Domains**. Follow Mailgun's DNS instructions (TXT for SPF, CNAME for DKIM, MX for bounce returns). The Free plan includes 1 custom verified domain.

**Critical DNS rule: only one SPF record and one DMARC record per DNS name.** Mail receivers treat multiple SPF or DMARC records at the same name as a PermError and all senders fail authentication, not just the new one. The standard setup here avoids that trap automatically because every record lives on the `mg.<your-domain>` subdomain, not the apex. Existing SPF / DMARC at the apex (Google Workspace, Microsoft 365, IONOS Mail, etc.) stays untouched. See the [EP Newsletter Mailgun docs](/plugins/ep-newsletter-mailgun/#step-2--verify-your-sending-domain) for the full rule, including SPF merge syntax for cases where you do need to combine includes.

### Step 3 — Create a sending key

In **Domain settings → Sending keys**, click **Add sending key**, name it (e.g. `ep-email-mailgun`), and copy the value when shown. Mailgun only displays it once.

If you already set up EP Newsletter — Mailgun and have a sending key from that, you can re-use the same value here. One sending key works for both plugins.

**Don't confuse the Sending Key with the SMTP password.** Mailgun has separate credentials for SMTP-based plugins (at Domain settings → SMTP credentials) and for the HTTP API (Domain settings → Sending keys). This plugin uses the HTTP API and needs the Sending Key, not the SMTP password. See the [EP Newsletter Mailgun docs Step 3](/plugins/ep-newsletter-mailgun/#dont-confuse-the-sending-key-with-other-mailgun-credentials) for the full credential rundown.

### Step 4 — Configure the plugin

Open **Plugin Settings → EP Email Mailgun**.

- **Sending Key.** From step 3. NOT the SMTP password.
- **Sending Domain.** Your verified Mailgun domain.
- **Region.** US or EU.

Click **Save**.

### Step 5 — Test

Use the **Test Connection** button. Green means the sending key, domain, and region are all valid.

### Step 6 — Activate as the EP Email transport

Go to **Plugin Settings → EP Email → SMTP Configuration** and change the **Transport** dropdown to **Mailgun**. From this point, all EP Email sends (contact forms, password resets, system notifications, double opt-in, etc.) route through Mailgun.

## Delivery behaviour

- Each EP Email message is submitted to Mailgun's `/v3/{your-domain}/messages` endpoint as a form-encoded HTTP POST.
- Mailgun queues, signs (DKIM), and delivers via its outbound mail servers.
- EP Email's delivery log records every send with status.
- Mailgun's own log at **Send → Logs** records the SMTP-level delivery outcome (delivered, deferred, bounced) for every recipient.

## What the settings page shows

- **Sending Key** input (masked).
- **Sending Domain** input.
- **Region** selector (US/EU).
- **Setup guide** with links straight to the relevant Mailgun screens.

## Pairs with EP Newsletter Mailgun

If you also run [EP Newsletter Mailgun](/plugins/ep-newsletter-mailgun/), both plugins can share the same Mailgun account, sending key, verified domain, and region. Doing so means every email leaving your site, whether transactional or campaign, flows through one consistent authenticated sender. Recipient mail providers build reputation on the domain over time, improving deliverability for both flows.

To share configuration, simply paste the same Sending Key, Sending Domain, and Region values in both plugins.

## Troubleshooting

### "Test connection fails with 401 or 403"

Sending key is invalid or expired. Regenerate at **Domain settings → Sending keys** in Mailgun. Watch for whitespace.

### "Test connection fails with 404"

Either the Sending Domain is misspelled, or the Region setting doesn't match where the domain was created in Mailgun. Mailgun's US and EU regions are separate.

### "EP Email shows Mailgun in the Transport dropdown but mail still goes through PHP mail()"

The Transport setting at **EP Email → SMTP** must be set to **Mailgun**. Activating this plugin only registers Mailgun as available; selecting it as the active transport makes it the live path.

### "Transactional emails land in spam"

Almost always a DNS-verification issue. Confirm your domain shows as **active** in Mailgun's domain list. If it does and you still hit spam, verify:

- The from-address in EP Email matches the verified Mailgun sending domain.
- Your domain has a DMARC record at the top level.
- The content is not triggering recipient-side filters (excessive caps, suspicious link patterns).

Sandbox domains will always go to spam due to lack of DMARC alignment. Use a real verified custom domain for production.

### "I want to switch back to SMTP or PHP mail()"

In **EP Email → SMTP**, change the Transport setting to **SMTP** or **PHP mail()**. The change is instant. No data migration needed.

## Feedback and corrections

For a quick question about this plugin, **EP Support** inside your admin is the fastest option. The chat widget sits on every EP plugin settings page and knows which one you're on, with starter questions and links preloaded for that exact screen.

For anything bigger such as a bug report, a feature request, or a "how do I..." that needs a real reply, open a ticket at [help.elmspark.com](https://help.elmspark.com). A real person, helped by AI, writes the reply. Usually within a few hours. Tickets don't disappear into the void.
