---
title: "EP Email Brevo"
description: "Brevo (formerly Sendinblue) transactional transport for EP Email. Routes contact forms, password resets, and system notifications through Brevo's API. 300/day free tier, no credit card."
---

EP Email Brevo is a transport driver for [EP Email](/plugins/ep-email/). When selected as the active transport, all transactional email from your site (contact form notifications, password resets, opt-in confirmations, system alerts) routes through Brevo's transactional API instead of PHP `mail()` or generic SMTP.

Published by [ElmsPark Studio](https://elmspark.com).

## Why route transactional email through Brevo

The default PHP `mail()` transport has serious deliverability problems on shared hosting: no DKIM signing, mismatched SPF, shared IP reputation with whoever else is on the server. Routing transactional sends through a known-good ESP fixes this. Brevo specifically gives you:

- **300 emails/day free tier** with no credit card required, enough for most low-volume transactional traffic
- **Domain-authenticated sending** when you verify your domain (DKIM, SPF, DMARC) so receivers trust your mail
- **Pairs cleanly with EP Newsletter Brevo** so newsletter and transactional sends share one Brevo account, one API key, one verified sender

## Requirements

- **PageMotor 0.6 or later**
- **EP Email** (required; this is a transport driver for EP Email)
- **EP Suite base class** (bundled)
- **A Brevo account** with a verified sender

## Installation

1. Install EP Email first.
2. Download `ep-email-brevo.zip` from the [EP Suite downloads page](https://github.com/ElmsPark-Studio/ep-suite-downloads/releases/latest).
3. Upload via **Plugins → Manage Plugins**. Activate.
4. Open **Plugin Settings → EP Email Brevo**.
5. Paste your API v3 key, sender email, and sender name.
6. In **EP Email → SMTP**, set the Transport dropdown to **Brevo**.

All outbound transactional mail now routes through Brevo.

## Setting up Brevo

If you've already set up Brevo for [EP Newsletter Brevo](/plugins/ep-newsletter-brevo/), reuse the same credentials.

1. Sign up at [brevo.com](https://onboarding.brevo.com/account/register). No card required.
2. Verify a sender email at **Senders, Domains & Dedicated IPs → Senders**. Brevo emails a confirmation link.
3. Create an API v3 key at [app.brevo.com/settings/keys/api](https://app.brevo.com/settings/keys/api). Copy the `xkeysib-...` value when shown. Do not enable IP blocking unless your server has a static IP you've whitelisted.
4. Paste the API key, sender email, and sender name into the plugin settings.
5. Use **Test Connection** to verify.
6. Set the EP Email transport to **Brevo**.

## Delivery behaviour

- Each EP Email message is submitted to `https://api.brevo.com/v3/smtp/email` as a JSON HTTP POST.
- Brevo queues, signs (DKIM if your domain is verified), and delivers via its outbound mail servers.
- EP Email's delivery log records every send.
- Brevo's own log at **Transactional → Logs** records each send with delivery status.

## Pairs with EP Newsletter Brevo

If you also run [EP Newsletter Brevo](/plugins/ep-newsletter-brevo/), both plugins can share the same Brevo account, API key, and verified sender. Every email leaving your site, whether transactional or campaign, flows through one consistent authenticated sender. Recipient mail providers build reputation on the domain over time.

## Troubleshooting

### "Test connection fails with 401"

The API key is invalid, or IP blocking is enabled in Brevo and your server's egress IP isn't whitelisted. Disable IP blocking in Brevo or add your server's static IP to **Security → Authorized IPs**.

### "Mail not delivering despite a valid key"

Confirm your sender email shows as **Verified** in Brevo. Unverified senders are silently rejected.

### "Transactional emails land in spam"

Verify your full sending domain in Brevo (not just a single sender email). Add DKIM, SPF, and DMARC records to DNS as Brevo instructs. This usually resolves spam routing within a few hours.

### "I want to switch back to SMTP or PHP mail()"

In EP Email → SMTP, change the Transport setting to **SMTP** or **PHP mail()**. The change is instant; no data migration needed.

## Feedback

For a quick question, **EP Support** inside your admin is the fastest path. For anything bigger, open a ticket at [help.elmspark.com](https://help.elmspark.com).
